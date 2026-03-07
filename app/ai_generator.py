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

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi:latest"

def generate_questions(category: str, difficulty: str, count: int = 2):

    questions_list = []

    for _ in range(count):

        prompt = f"""
        Generate ONE interview question for a {category} role.
        Difficulty level: {difficulty}.
        Return ONLY the question text.
        Do not add numbering.
        Do not add explanation.
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

        # if response.status_code != 200:
        #     continue
        if response.status_code != 200:
            print("Ollama Error:", response.text)
            continue

        data = response.json()
        question_text = data.get("response", "").strip()

        if question_text:
            questions_list.append({
                "question_text": question_text,
                "category": category,
                "difficulty": difficulty
            })

    return questions_list