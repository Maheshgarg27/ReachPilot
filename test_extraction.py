from research import search_web
from extractor import extract_founders

query = "AI startup founders and CEOs in India"

print("Searching the web...")

results = search_web(query, max_results=10)

print(f"Found {len(results)} search results.")

print("\nExtracting founders using Gemini...")

leads = extract_founders(results,max_leads=20)

print(f"\nExtracted {len(leads)} leads.")

for i, lead in enumerate(leads, 1):

    print(f"\n--- LEAD {i} ---")

    for key, value in lead.items():
        print(f"{key}: {value}")