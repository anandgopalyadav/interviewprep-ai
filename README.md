
# 🚀 InterviewPrep AI

AI-powered **Interview Practice Platform** that simulates real technical interviews using AI evaluation, analytics dashboards, and performance tracking.

This platform helps users practice interviews, analyze their weaknesses, and improve over time using data insights.

---

# 🎯 Project Goal

The goal of this platform is to create a **realistic AI interview environment** where candidates can:

- Practice technical interview questions
- Receive AI-based evaluation
- Track their strengths and weaknesses
- Improve weak areas automatically through adaptive questions

---

# 🧠 How The System Works

1. User logs into the system
2. Platform generates interview questions
3. User submits answers
4. AI evaluates the answers
5. Results are saved in the database
6. Dashboard shows performance insights
7. Future tests focus more on weak areas

---

# 📝 Smart Interview Test

Each interview test generates **10 questions** from different categories:

- Python
- SQL
- Data Analysis
- Machine Learning
- ETL
- HR

The system first checks the **database question bank**.

If there are not enough questions:

1. AI generates new questions
2. Questions are saved in the database
3. They are reused for future tests

---

# 🤖 AI Answer Evaluation

When a user submits an answer:

The AI evaluates the answer and returns:

- Score
- Feedback
- Strong / Weak classification

Example:

Score: 8/10  
Feedback: Good explanation but missing indexing concept.

---

# 💾 Data Stored in Database

All interview interactions are saved in the database.

## Users Table

Stores user information

Fields:

- user_id
- name
- email
- password
- created_at

## Questions Table

Stores interview questions

Fields:

- question_id
- question_text
- category
- difficulty
- source (AI / Manual)

## User Answers Table

Stores user responses and evaluation

Fields:

- answer_id
- user_id
- question_id
- user_answer
- score
- feedback
- is_weak
- created_at

This allows the system to **track user performance over time**.

---

# 📊 Performance Dashboard

The dashboard analyzes stored data and shows:

### Strength vs Weakness

- Strong answers
- Weak answers

### Category Performance

Example:

Python: 85%  
SQL: 60%  
Machine Learning: 40%

This clearly shows **which skills need improvement**.

---

# 📈 Analytics Features

Dashboard includes:

- Strong vs weak answers
- Category performance chart
- Score trend over time
- Recent attempts
- Improvement indicators

Charts are created using **Chart.js**.

---

# 🔄 Adaptive Learning (Weak Area Improvement)

The system automatically detects weak categories.

Example:

Previous performance:

Python → Strong  
SQL → Weak  
ML → Average

Next test will generate:

Python Questions → 2  
SQL Questions → 5  
ML Questions → 3

This helps users **focus more on weak areas and become stronger.**

---

# 📄 PDF Interview Report

Users can download a **complete interview performance report**.

The report includes:

- Candidate information
- Total attempts
- Average score
- Question summaries
- AI feedback
- Weak areas

Generated using **ReportLab**.

---

# 🔐 Authentication

The platform uses **JWT authentication**.

Flow:

User Login → JWT Token Generated → Token stored in browser → Secure API access

Benefits:

- Secure login
- Multi-user support
- Protected dashboards

---

# 🧰 Tech Stack

## Backend

- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication
- Ollama (Local LLM)
- OpenAI API
- ReportLab

## Frontend

- HTML
- CSS

---

# ▶ Run The Project

Clone the repository

git clone https://github.com/anandgopalyadav/interviewprep-ai.git

Create virtual environment

python -m venv venv

Activate

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

Install dependencies

pip install fastapi uvicorn sqlalchemy passlib python-jose reportlab ollama openai

Run server

uvicorn app.main:app --reload

Open in browser

http://127.0.0.1:8000

---

# 🚀 Future Improvements

- Resume-based interview questions
- Voice AI interviewer
- AI interview coaching
- Difficulty-based adaptive testing

---

# 👨‍💻 Author

Anand Yadav  
AI / Data Analytics Developer

⭐ If you like this project, give it a star on GitHub!
