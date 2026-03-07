from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clean_and_categorize(raw_questions):

    prompt = f"""
    Clean duplicates and categorize into:
    SQL, Python, Statistics, ML, ETL, BI, Scenario, Behavioral.

    Return JSON list like:
    [
        {{
            "question": "...",
            "category": "SQL"
        }}
    ]

    Questions:
    {raw_questions}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
