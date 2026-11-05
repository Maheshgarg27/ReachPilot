
import os
import time
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def extract_founders(search_results, max_leads=20):

    if not search_results:
        return []

    research_data = json.dumps(search_results, indent=2)

    prompt = f"""
    You are an expert research assistant.

    Extract founders and CEOs of AI startups in India
    from the following web search results.

    SEARCH RESULTS:
    {research_data}

    RULES:
    1. Extract only people explicitly identified as founders,
       co-founders, CEOs or managing directors.
    2. Do not invent names or company information.
    3. Do not guess LinkedIn profile URLs.
    4. If information is missing, use null.
    5. Include the source URL supporting the information.
    6. Avoid duplicate people.
    7. Only include companies relevant to AI.

    Return ONLY valid JSON in this format:

    {{
        "leads": [
            {{
                "name": "Founder Name",
                "company": "Company Name",
                "designation": "Founder/CEO",
                "website": null,
                "linkedin_url": null,
                "source_url": "Source URL",
                "relevance": "Short explanation"
            }}
        ]
    }}
    """

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json"
                }
            )

            data = json.loads(response.text)

            leads = data.get("leads", [])

            # Remove duplicate founders
            unique_leads = []
            seen = set()

            for lead in leads:
                key = (
                    (lead.get("name") or "").strip().lower(),
                    (lead.get("company") or "").strip().lower()
                )

                if key[0] and key[1] and key not in seen:
                    seen.add(key)
                    unique_leads.append(lead)

            # Return limited unique leads
            return unique_leads[:max_leads]

        except Exception as e:
            error = str(e)

            if "503" in error or "UNAVAILABLE" in error:
                wait_time = 2 ** (attempt + 1)

                print(
                    f"Gemini temporarily unavailable. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:
                print("Gemini extraction error:", e)
                return []

    print("Gemini unavailable after 3 attempts.")
    return []
