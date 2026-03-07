import re

# Try to import ollama (only works locally)
try:
    import ollama
except ImportError:
    ollama = None


def evaluate_answer(question: str, user_answer: str):
    """
    AI evaluation using Ollama locally.
    Fallback scoring when Ollama is unavailable (e.g. on Render).
    """

    # If Ollama not available (Render server)
    if ollama is None:
        score = 5
        feedback = "AI evaluation unavailable on cloud deployment."
        return score, feedback

    prompt = f"""
You are a strict technical interviewer.

Evaluate the candidate answer carefully.

Respond EXACTLY in this format.
Do NOT add extra text.

Score: <number between 1 and 10>
Feedback: <2-4 lines explaining strengths and missing concepts>

Question:
{question}

Candidate Answer:
{user_answer}
"""

    try:
        response = ollama.chat(
            model="phi",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response["message"]["content"]

        # Extract score safely
        score_match = re.search(r"Score:\s*(\d+)", result)
        if score_match:
            score = int(score_match.group(1))
            if score < 1 or score > 10:
                score = 5
        else:
            score = 5

        # Extract feedback safely
        feedback_match = re.search(r"Feedback:\s*(.*)", result, re.DOTALL)
        if feedback_match:
            feedback = feedback_match.group(1).strip()
        else:
            feedback = "AI evaluation completed."

        return score, feedback

    except Exception as e:
        print("Ollama Evaluation Error:", e)
        return 5, "AI evaluation failed."
    




    
# import ollama
# import re

# def evaluate_answer(question: str, user_answer: str):
#     """
#     Stable AI evaluation using Ollama (phi).
#     Safe structured extraction (no JSON parsing).
#     """

#     prompt = f"""
# You are a strict technical interviewer.

# Evaluate the candidate answer carefully.

# Respond EXACTLY in this format.
# Do NOT add extra text.

# Score: <number between 1 and 10>
# Feedback: <2-4 lines explaining strengths and missing concepts>

# Question:
# {question}

# Candidate Answer:
# {user_answer}
# """

#     try:
#         response = ollama.chat(
#             model="phi",   # Make sure this model is installed
#             messages=[{"role": "user", "content": prompt}]
#         )

#         result = response["message"]["content"]

#         # Extract score safely
#         score_match = re.search(r"Score:\s*(\d+)", result)
#         if score_match:
#             score = int(score_match.group(1))
#             if score < 1 or score > 10:
#                 score = 5
#         else:
#             score = 5

#         # Extract feedback safely
#         feedback_match = re.search(r"Feedback:\s*(.*)", result, re.DOTALL)
#         if feedback_match:
#             feedback = feedback_match.group(1).strip()
#         else:
#             feedback = "AI evaluation completed."

#         return score, feedback

#     except Exception as e:
#         print("Ollama Evaluation Error:", e)
#         return 5, "AI evaluation failed."




















# don't delete


# if you hve open AI api key then you can use below code for evaluation of answer using open AI api


# import re
# from openai import OpenAI

# client = OpenAI()

# def evaluate_answer(question: str, user_answer: str):

#     prompt = f"""
# You are a strict technical interviewer.

# Respond EXACTLY in this format.

# Score: <number between 1 and 10>
# Feedback: <2-4 lines explaining strengths and missing concepts>

# Question:
# {question}

# Candidate Answer:
# {user_answer}
# """

#     try:
#         response = client.chat.completions.create(
#             model="gpt-4.1",
#             messages=[
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.2,
#         )

#         result = response.choices[0].message.content

#         print("OpenAI Raw Response:", result)  # DEBUG

#         score_match = re.search(r"Score:\s*(\d+)", result)
#         score = int(score_match.group(1)) if score_match else 5

#         if score < 1 or score > 10:
#             score = 5

#         feedback_match = re.search(r"Feedback:\s*(.*)", result, re.DOTALL)
#         feedback = feedback_match.group(1).strip() if feedback_match else "AI evaluation completed."

#         return score, feedback

#     except Exception as e:
#         print("❌ OpenAI Error:", e)
#         return 5, "AI evaluation failed."
