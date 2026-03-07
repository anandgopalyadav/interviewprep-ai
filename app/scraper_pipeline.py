# from search import search_questions
# from scraper import scrape_questions_from_url

# def run_pipeline():
#     links = search_questions("Data Analyst interview questions 2024")

#     for link in links[:5]:
#         questions = scrape_questions_from_url(link)
#         print(questions)

# if __name__ == "__main__":
#     run_pipeline()

from app.search import search_questions
from app.scraper import scrape_questions_from_url


def run_pipeline():
    query = "Data Analyst interview questions 2024"
    links = search_questions(query)

    print(f"🔎 Found {len(links)} links")

    for link in links[:5]:
        print(f"\nScraping: {link}")
        questions = scrape_questions_from_url(link)

        for q in questions[:5]:  # print first 5 per link
            print("-", q)


if __name__ == "__main__":
    run_pipeline()

