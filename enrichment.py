import re
from urllib.parse import urlparse
from research import search_web


def is_linkedin_profile(url):
    """Check whether URL points to an individual LinkedIn profile."""

    if not url:
        return False

    parsed = urlparse(url)

    return (
        parsed.netloc.lower().endswith("linkedin.com")
        and parsed.path.lower().startswith("/in/")
    )

def find_company_website(company):

    query = f"{company} official website"

    results = search_web(query, max_results=5)

    excluded_domains = [
        "linkedin.com",
        "facebook.com",
        "instagram.com",
        "crunchbase.com",
        "tracxn.com",
        "wikipedia.org",
        "tavily.com",
        "indianstartuptimes.com"
    ]

    for result in results:

        url = result.get("url", "")
        content = result.get("content") or ""
        title = result.get("title") or ""

        # First, extract an explicitly listed company website
        match = re.search(
            r"Website:\s*(?:https?://)?(?:www\.)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
            content,
            re.IGNORECASE
        )

        if match:

            domain = match.group(1)

            website = f"https://{domain}"

            if not any(x in domain.lower() for x in excluded_domains):

                return {
                    "website": website,
                    "source_url": url,
                    "evidence": content[:500]
                }

        # Otherwise, consider the search result URL
        domain = urlparse(url).netloc.lower()

        if not domain:
            continue

        if any(x in domain for x in excluded_domains):
            continue

        return {
            "website": url,
            "source_url": url,
            "evidence": content[:500]
        }

    return {
        "website": None,
        "source_url": None,
        "evidence": None
    }

def find_linkedin_profile(name, company):
    """Discover a possible LinkedIn profile and check supporting evidence."""

    query = f'"{name}" "{company}" founder LinkedIn profile'

    results = search_web(query, max_results=10)

    for result in results:

        url = result.get("url", "")
        title = result.get("title") or ""
        content = result.get("content") or ""

        if not is_linkedin_profile(url):
            continue

        combined_text = f"{title} {content}".lower()

        name_parts = name.lower().split()

        # Require the full name and company to appear in the evidence.
        name_match = name.lower() in combined_text
        company_match = company.lower() in combined_text

        if name_match and company_match:

            return {
                "linkedin_url": url,
                "linkedin_source": url,
                "linkedin_status": "candidate_needs_manual_review"
            }

    return {
        "linkedin_url": None,
        "linkedin_source": None,
        "linkedin_status": "not_found"
    }


def enrich_lead(lead):

    name = lead.get("name")
    company = lead.get("company")

    if not name or not company:
        return lead

    print(f"\nResearching: {name} - {company}")

    # Find company website
    company_data = find_company_website(company)

    # Find LinkedIn profile
    linkedin_data = find_linkedin_profile(name, company)

    # Update lead
    lead.update({
        "website": company_data["website"],
        "website_source": company_data["source_url"],
        "website_evidence": company_data["evidence"],
        **linkedin_data
    })

    return lead


def enrich_leads(leads):

    enriched_leads = []

    for lead in leads:

        try:
            enriched = enrich_lead(lead)
            enriched_leads.append(enriched)

        except Exception as e:

            print(f"Error enriching {lead.get('name')}: {e}")

            lead.update({
                "website": None,
                "linkedin_url": None,
                "linkedin_status": "error"
            })

            enriched_leads.append(lead)

    return enriched_leads