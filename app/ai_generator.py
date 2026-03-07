# # if we have chatgpt Token, we can use it to generate questions
# import os
# import json
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# def generate_questions(category: str, difficulty: str, count: int = 2):
#     prompt = f"""
#     Generate {count} interview questions for a {category} role.
#     Difficulty level: {difficulty}.
    
#     Return response strictly in JSON format like this:
#     [
#         {{
#             "question_text": "...",
#             "category": "{category}",
#             "difficulty": "{difficulty}"
#         }}
#     ]
#     """

#     response = client.chat.completions.create(
#         model="gpt-4.1-turbo",
#         messages=[
#             {"role": "system", "content": "You are an expert interview question generator."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.7
#     )

#     content = response.choices[0].message.content

#     try:
#         return json.loads(content)
#     except:
#         return []

# import requests

# OLLAMA_URL = "http://localhost:11434/api/generate"
# MODEL_NAME = "phi:latest"

# def generate_questions(category: str, difficulty: str, count: int = 2):

#     questions_list = []

#     for _ in range(count):

#         prompt = f"""
#         Generate ONE interview question for a {category} role.
#         Difficulty level: {difficulty}.
#         Return ONLY the question text.
#         Do not add numbering.
#         Do not add explanation.
#         """

#         response = requests.post(
#             OLLAMA_URL,
#             json={
#                 "model": MODEL_NAME,
#                 "prompt": prompt,
#                 "stream": False,
#                 "temperature": 0.9
#             }
#         )

#         # if response.status_code != 200:
#         #     continue
#         if response.status_code != 200:
#             print("Ollama Error:", response.text)
#             continue

#         data = response.json()
#         question_text = data.get("response", "").strip()

#         if question_text:
#             questions_list.append({
#                 "question_text": question_text,
#                 "category": category,
#                 "difficulty": difficulty
#             })

#     return questions_list




import requests
from sqlalchemy.orm import Session
from app import models

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi:latest"


def get_solved_questions(db: Session, category: str, difficulty: str):
    """
    Fetch questions already answered well (score >= 7)
    so we avoid repeating them.
    """

    results = (
        db.query(models.Question.question_text)
        .join(models.UserAnswer)
        .filter(
            models.Question.category == category,
            models.Question.difficulty == difficulty,
            models.UserAnswer.score >= 7
        )
        .all()
    )

    return [q[0] for q in results]


def generate_questions(category: str, difficulty: str, db: Session, count: int = 2):

    questions_list = []

    solved_questions = get_solved_questions(db, category, difficulty)

    avoid_text = "\n".join(solved_questions)

    attempts = 0
    max_attempts = count * 5

    while len(questions_list) < count and attempts < max_attempts:

        attempts += 1

        prompt = f"""
You are a technical interviewer.

Generate ONE interview question for a {category} role.

Difficulty: {difficulty}

IMPORTANT:
Do NOT generate questions similar to these:

{avoid_text}

Rules:
- Return ONLY the question text
- Do NOT add numbering
- Do NOT add explanation
"""

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.9
            }
        )

        if response.status_code != 200:
            print("Ollama Error:", response.text)
            continue

        data = response.json()
        question_text = data.get("response", "").strip()

        if not question_text:
            continue

        # Prevent duplicates in this batch
        if any(q["question_text"] == question_text for q in questions_list):
            continue

        # Prevent duplicates from solved questions
        if question_text in solved_questions:
            continue

        # Check if question already exists in DB
        existing = db.query(models.Question).filter(
            models.Question.question_text == question_text
        ).first()

        if not existing:

            new_question = models.Question(
                question_text=question_text,
                category=category,
                difficulty=difficulty
            )

            db.add(new_question)
            db.commit()

        questions_list.append({
            "question_text": question_text,
            "category": category,
            "difficulty": difficulty
        })

    return questions_list