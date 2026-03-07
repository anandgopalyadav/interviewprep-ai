
from pydantic import BaseModel, EmailStr
from typing import Optional


# =============================
# 👤 USER SCHEMAS
# =============================

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# =============================
# ❓ QUESTION SCHEMA
# =============================

class QuestionResponse(BaseModel):
    id: str
    question_text: str
    category: Optional[str]
    difficulty: Optional[str]

    class Config:
        from_attributes = True


# =============================
# 📝 ANSWER SCHEMAS
# =============================

class AnswerSubmit(BaseModel):
    question_id: str
    user_answer: str


class AnswerResponse(BaseModel):
    score: int
    feedback: str
