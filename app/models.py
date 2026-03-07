# # from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
# from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, Boolean
# from sqlalchemy.orm import relationship
# from app.database import Base
# import uuid
# from datetime import datetime


# # =============================
# # 👤 USER TABLE
# # =============================
# class User(Base):
#     __tablename__ = "users"

#     id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
#     name = Column(String, nullable=False)
#     email = Column(String, unique=True, nullable=False)
#     password = Column(String, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)

#     answers = relationship("UserAnswer", back_populates="user")


# # =============================
# # ❓ QUESTION TABLE
# # =============================
# class Question(Base):
#     __tablename__ = "questions"

#     id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
#     question_text = Column(Text, nullable=False)
#     category = Column(String)
#     difficulty = Column(String)
#     source = Column(String)
#     created_at = Column(DateTime, default=datetime.utcnow)

#     answers = relationship("UserAnswer", back_populates="question")


# # =============================
# # 📝 USER ANSWERS TABLE
# # =============================
# class UserAnswer(Base):
#     __tablename__ = "user_answers"

#     id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
#     user_id = Column(String, ForeignKey("users.id"))
#     question_id = Column(String, ForeignKey("questions.id"))

#     user_answer = Column(Text)
#     score = Column(Integer)
#     feedback = Column(Text)   # ✅ NEW COLUMN ADDED
#     is_weak = Column(Boolean, default=False)   # ✅ ADD HERE
#     created_at = Column(DateTime, default=datetime.utcnow)

#     user = relationship("User", back_populates="answers")
#     question = relationship("Question", back_populates="answers")




from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from datetime import datetime


# =============================
# 👤 USER TABLE
# =============================
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    answers = relationship(
        "UserAnswer",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# =============================
# ❓ QUESTION TABLE
# =============================
class Question(Base):
    __tablename__ = "questions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    question_text = Column(Text, nullable=False)
    category = Column(String, index=True)
    difficulty = Column(String)  # Easy / Medium / Hard
    source = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    answers = relationship(
        "UserAnswer",
        back_populates="question",
        cascade="all, delete-orphan"
    )


# =============================
# 📝 USER ANSWERS TABLE
# =============================
class UserAnswer(Base):
    __tablename__ = "user_answers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    question_id = Column(String, ForeignKey("questions.id"), nullable=False)

    user_answer = Column(Text, nullable=False)
    score = Column(Integer)  # 0–10 scoring
    feedback = Column(Text)  # AI evaluation feedback
    is_weak = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="answers")
    question = relationship("Question", back_populates="answers")
