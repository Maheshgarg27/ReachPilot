from research import search_web
from extractor import extract_founders
from enrichment import enrich_leads

query = "AI startup founders and CEOs in India"

print("Searching for founders...")

results = search_web(query, max_results=10)

leads = extract_founders(results, max_leads=3)

print(f"\nExtracted {len(leads)} founders.")

print("\nStarting enrichment...")

enriched_leads = enrich_leads(leads)

for i, lead in enumerate(enriched_leads, 1):

    print(f"\n{'='*40}")
    print(f"LEAD {i}")
    print(f"{'='*40}")

    print("Name:", lead.get("name"))
    print("Company:", lead.get("company"))
    print("Designation:", lead.get("designation"))
    print("Website:", lead.get("website"))
    print("LinkedIn:", lead.get("linkedin_url"))
    print("LinkedIn Status:", lead.get("linkedin_status"))
    print("Source:", lead.get("source_url"))
    print("Website Evidence:", lead.get("website_evidence"))