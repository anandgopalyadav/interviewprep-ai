from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from typing import List
import random
from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

from app.database import engine, Base, get_db
from app import models
from app.schemas import UserCreate, Token, AnswerSubmit
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)
from app.evaluator import evaluate_answer
from app.ai_generator import generate_questions


# =============================
# INITIAL SETUP
# =============================
Base.metadata.create_all(bind=engine)

app = FastAPI(title="InterviewPrep AI 🚀")
templates = Jinja2Templates(directory="templates")


# =============================
# ROOT
# =============================
@app.get("/")
def root():
    return {"message": "InterviewPrep AI is running 🚀"}


# =============================
# HTML PAGES
# =============================
@app.get("/login-page", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register-page", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/home", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/smart-test-page", response_class=HTMLResponse)
def smart_test_page(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


# =============================
# REGISTER
# =============================
@app.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token({"sub": new_user.email})

    return {"access_token": access_token, "token_type": "bearer"}


# =============================
# LOGIN
# =============================
@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(
        models.User.email == form_data.username
    ).first()

    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": db_user.email})

    return {"access_token": access_token, "token_type": "bearer"}


# =============================
# CURRENT USER
# =============================
@app.get("/me")
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }


# =============================
# SMART TEST
# =============================
# @app.get("/smart-test")
# def smart_test(db: Session = Depends(get_db),
#                current_user: models.User = Depends(get_current_user)):

#     distribution = {
#         "Python": 2,
#         "SQL": 2,
#         "Data Analysis": 2,
#         "Machine Learning": 2,
#         "ETL": 1,
#         "HR": 1
#     }

#     final_questions = []

#     for category, count in distribution.items():

#         db_questions = db.query(models.Question).filter(
#             models.Question.category == category
#         ).all()

#         if len(db_questions) >= count:
#             final_questions.extend(random.sample(db_questions, count))
#         else:
#             needed = count - len(db_questions)

#             generated = generate_questions(category, "Medium", needed)

#             for q in generated:
#                 new_q = models.Question(
#                     question_text=q["question_text"],
#                     category=q["category"],
#                     difficulty=q["difficulty"],
#                     source="AI"
#                 )
#                 db.add(new_q)
#                 db.commit()
#                 db.refresh(new_q)
#                 final_questions.append(new_q)

#             final_questions.extend(db_questions)

#     random.shuffle(final_questions)
#     return final_questions


# =============================
# SMART TEST
# =============================
@app.get("/smart-test")
def smart_test(db: Session = Depends(get_db),
               current_user: models.User = Depends(get_current_user)):

    distribution = {
        "Python": 2,
        "SQL": 2,
        "Data Analysis": 2,
        "Machine Learning": 2,
        "ETL": 1,
        "HR": 1
    }

    final_questions = []

    for category, count in distribution.items():

        db_questions = db.query(models.Question).filter(
            models.Question.category == category
        ).all()

        if len(db_questions) >= count:
            final_questions.extend(random.sample(db_questions, count))

        else:
            needed = count - len(db_questions)

            # FIX: pass db into generator
            generated = generate_questions(category, "Medium", db, needed)

            # Fetch newly generated questions from DB
            new_questions = db.query(models.Question).filter(
                models.Question.category == category
            ).order_by(models.Question.created_at.desc()).limit(needed).all()

            final_questions.extend(new_questions)
            final_questions.extend(db_questions)

    random.shuffle(final_questions)

    return final_questions




# =============================
# SUBMIT TEST
# =============================
@app.post("/submit-test")
def submit_test(answers: List[AnswerSubmit],
                db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):

    total_score = 0
    results = []

    for ans in answers:

        question = db.query(models.Question).filter(
            models.Question.id == ans.question_id
        ).first()

        if not question:
            continue

        score, feedback = evaluate_answer(
            question.question_text,
            ans.user_answer
        )

        is_weak = score <= 5
        total_score += score

        db.add(models.UserAnswer(
            user_id=current_user.id,
            question_id=question.id,
            user_answer=ans.user_answer,
            score=score,
            feedback=feedback,
            is_weak=is_weak
        ))

        results.append({
            "question": question.question_text,
            "score": score,
            "feedback": feedback
        })

    db.commit()

    avg = round(total_score / len(results), 2) if results else 0

    return {
        "total_score": total_score,
        "average_score": avg,
        "strong_answers": len([r for r in results if r["score"] > 5]),
        "weak_answers": len([r for r in results if r["score"] <= 5]),
        "results": results
    }


# =============================
# PERFORMANCE SUMMARY
# =============================
# @app.get("/performance-summary")
# def performance_summary(start_date: str = None,
#                         end_date: str = None,
#                         db: Session = Depends(get_db),
#                         current_user: models.User = Depends(get_current_user)):

#     query = db.query(models.UserAnswer).filter(
#         models.UserAnswer.user_id == current_user.id
#     )

#     if start_date:
#         start = datetime.strptime(start_date, "%Y-%m-%d")
#         query = query.filter(models.UserAnswer.created_at >= start)

#     if end_date:
#         end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
#         query = query.filter(models.UserAnswer.created_at < end)

#     attempts = query.order_by(models.UserAnswer.created_at).all()

#     total = len(attempts)
#     weak = sum(1 for a in attempts if a.is_weak)
#     strong = total - weak
#     avg = round(sum(a.score for a in attempts) / total, 2) if total else 0

#     return {
#         "total_attempts": total,
#         "strong_answers": strong,
#         "weak_answers": weak,
#         "average_score": avg,
#         "details": [
#             {
#                 "question_text": a.question.question_text,
#                 "score": a.score,
#                 "is_weak": a.is_weak,
#                 "attempted_at": a.created_at
#             }
#             for a in attempts
#         ]
#     }
@app.get("/performance-summary")
def performance_summary(start_date: str = None,
                        end_date: str = None,
                        db: Session = Depends(get_db),
                        current_user: models.User = Depends(get_current_user)):

    query = db.query(models.UserAnswer).filter(
        models.UserAnswer.user_id == current_user.id
    )

    if start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.filter(models.UserAnswer.created_at >= start)

    if end_date:
        end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        query = query.filter(models.UserAnswer.created_at < end)

    attempts = query.order_by(models.UserAnswer.created_at).all()

    total = len(attempts)
    weak = sum(1 for a in attempts if a.is_weak)
    strong = total - weak
    avg = round(sum(a.score for a in attempts) / total, 2) if total else 0

    # ================= Weekly Comparison =================
    today = datetime.utcnow()
    last_week = today - timedelta(days=7)
    previous_week = today - timedelta(days=14)

    this_week = db.query(models.UserAnswer).filter(
        models.UserAnswer.user_id == current_user.id,
        models.UserAnswer.created_at >= last_week
    ).all()

    prev_week = db.query(models.UserAnswer).filter(
        models.UserAnswer.user_id == current_user.id,
        models.UserAnswer.created_at >= previous_week,
        models.UserAnswer.created_at < last_week
    ).all()

    this_avg = (
        sum(a.score for a in this_week) / len(this_week)
        if this_week else 0
    )

    prev_avg = (
        sum(a.score for a in prev_week) / len(prev_week)
        if prev_week else 0
    )

    if prev_avg > 0:
        weekly_change = round(
            ((this_avg - prev_avg) / prev_avg) * 100, 2
        )
    else:
        weekly_change = 0

    return {
        "total_attempts": total,
        "strong_answers": strong,
        "weak_answers": weak,
        "average_score": avg,
        "weekly_change_percent": weekly_change,
        "weak_percentage": round((weak / total) * 100, 2) if total else 0,
        "details": [
            {
                "question_text": a.question.question_text,
                "score": a.score,
                "is_weak": a.is_weak,
                "attempted_at": a.created_at
            }
            for a in attempts
        ]
    }


@app.get("/category-summary")
def category_summary(start_date: str = None,
                     end_date: str = None,
                     db: Session = Depends(get_db),
                     current_user: models.User = Depends(get_current_user)):

    query = db.query(
        models.Question.category,
        func.count(models.UserAnswer.id).label("total"),
        func.sum(
            case((models.UserAnswer.is_weak == True, 1), else_=0)
        ).label("weak_count")
    ).join(
        models.UserAnswer,
        models.Question.id == models.UserAnswer.question_id
    ).filter(
        models.UserAnswer.user_id == current_user.id
    )

    if start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.filter(models.UserAnswer.created_at >= start)

    if end_date:
        end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        query = query.filter(models.UserAnswer.created_at < end)

    results = query.group_by(models.Question.category).all()

    return [
        {
            "category": r.category,
            "total_attempts": r.total,
            "weak_answers": r.weak_count or 0,
            "weak_percentage": round(
                ((r.weak_count or 0) / r.total) * 100, 2
            ) if r.total else 0
        }
        for r in results
    ]


# =============================
# DOWNLOAD REPORT (DATE FILTER ENABLED)
# =============================
@app.get("/download-report")
def download_report(
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    query = db.query(models.UserAnswer).filter(
        models.UserAnswer.user_id == current_user.id
    )

    # Date filtering
    if start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.filter(models.UserAnswer.created_at >= start)

    if end_date:
        end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        query = query.filter(models.UserAnswer.created_at < end)

    attempts = query.order_by(models.UserAnswer.created_at).all()

    if not attempts:
        raise HTTPException(status_code=404, detail="No data found for selected date range")

    total = len(attempts)
    strong = sum(1 for a in attempts if not a.is_weak)
    weak = sum(1 for a in attempts if a.is_weak)
    avg_score = round(sum(a.score for a in attempts) / total, 2)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph(
        f"InterviewPrep AI - Performance Report",
        styles["Title"]
    ))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph(
        f"Candidate: {current_user.name}",
        styles["Normal"]
    ))
    elements.append(Paragraph(
        f"Email: {current_user.email}",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph(f"Total Attempts: {total}", styles["Normal"]))
    elements.append(Paragraph(f"Strong Answers: {strong}", styles["Normal"]))
    elements.append(Paragraph(f"Weak Answers: {weak}", styles["Normal"]))
    elements.append(Paragraph(f"Average Score: {avg_score}", styles["Normal"]))
    elements.append(Spacer(1, 0.5 * inch))

    for a in attempts:
        elements.append(Paragraph(
            f"Q: {a.question.question_text}",
            styles["Normal"]
        ))
        elements.append(Paragraph(
            f"Score: {a.score}",
            styles["Normal"]
        ))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=Interview_Report.pdf"
        }
    )
