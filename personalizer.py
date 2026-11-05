import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")


def generate_message(lead, template):

    prompt = f"""
    You are a professional LinkedIn outreach assistant.

    PERSONAL INFORMATION:
    Name: {lead.get('name')}
    Company: {lead.get('company')}
    Designation: {lead.get('designation')}
    Company Description: {lead.get('relevance')}

    USER'S MESSAGE TEMPLATE:
    {template}

    INSTRUCTIONS:

    1. Personalize the message for this specific founder.
    2. Replace [name] with the person's name.
    3. Replace [company] with the company name.
    4. Replace [designation] with their designation.
    5. Preserve the user's original intent and tone.
    6. Do not invent personal connections or achievements.
    7. Keep the message concise and professional.
    8. Return only the final message.
    """

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:

        print("Message generation error:", e)

        # Basic placeholder replacement as fallback
        message = template

        message = message.replace(
            "[name]", lead.get("name") or ""
        )

        message = message.replace(
            "[company]", lead.get("company") or ""
        )

        message = message.replace(
            "[designation]", lead.get("designation") or ""
        )

        return message