# import requests
# from bs4 import BeautifulSoup


# def scrape_questions_from_url(url: str):
#     """
#     Scrapes interview questions from a webpage.
#     Returns list of question strings.
#     """

#     try:
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
#     except Exception as e:
#         print(f"❌ Failed to fetch {url}: {e}")
#         return []

#     soup = BeautifulSoup(response.text, "html.parser")
#     questions = []

#     # Extract potential questions from list items
#     for li in soup.find_all("li"):
#         text = li.get_text(strip=True)

#         if (
#             "?" in text
#             and len(text) > 20
#             and len(text) < 300
#         ):
#             questions.append(text)

#     # Remove duplicates
#     return list(set(questions))


# for testing purposes, we will return a static list of questions instead of scraping from the web.

def scrape_questions_from_url(url: str):
    print(f"Scraping mock data from {url}")

    return [
        "What is the difference between WHERE and HAVING?",
        "Explain normalization in SQL.",
        "What is bias vs variance?",
        "What is ETL process?",
        "Explain INNER JOIN vs LEFT JOIN?"
    ]
