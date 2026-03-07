def search_questions(query: str):
    print("🔄 Using mock search (no SerpAPI key)")
    return [
        "https://example.com/page1",
        "https://example.com/page2"
    ]







# Need to use this when we have API key for SerpAPI. For now, we will return empty list from search_questions function.

# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()

# SERPAPI_KEY = os.getenv("SERPAPI_KEY")


# def search_questions(query: str):
#     """
#     Search Google using SerpAPI and return list of URLs.
#     """

#     if not SERPAPI_KEY:
#         print("⚠️ SERPAPI_KEY not found. Returning empty result.")
#         return []

#     url = "https://serpapi.com/search"

#     params = {
#         "q": query,
#         "api_key": SERPAPI_KEY,
#         "engine": "google",
#     }

#     try:
#         response = requests.get(url, params=params, timeout=10)
#         response.raise_for_status()
#     except Exception as e:
#         print(f"❌ Search request failed: {e}")
#         return []

#     data = response.json()

#     results = []
#     for result in data.get("organic_results", []):
#         link = result.get("link")
#         if link:
#             results.append(link)

#     return results
