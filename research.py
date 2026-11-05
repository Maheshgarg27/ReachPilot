import os
from dotenv import load_dotenv
from tavily import TavilyClient

# Load environment variables
load_dotenv()

# Initialize Tavily
api_key = os.getenv("TAVILY_API_KEY")

if not api_key:
    raise ValueError("TAVILY_API_KEY not found in .env")

tavily = TavilyClient(api_key=api_key)


def search_web(query, max_results=10):

    try:
        response = tavily.search(
            query=query,
            search_depth="advanced",
            max_results=max_results,
            topic="general"
        )

        results = []

        for item in response.get("results", []):

            results.append({
                "title": item.get("title"),
                "url": item.get("url"),
                "content": item.get("content")
            })

        return results

    except Exception as e:
        print(f"Search error: {e}")
        return []


# Test the research engine
if __name__ == "__main__":

    query = "AI startups in India and their founders or CEOs"

    results = search_web(query, max_results=5)

    for i, result in enumerate(results, 1):

        print(f"\n--- RESULT {i} ---")
        print("Title:", result["title"])
        print("URL:", result["url"])
        print("Content:", result["content"][:500])