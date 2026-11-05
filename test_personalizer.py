from personalizer import generate_message

lead = {
    "name": "Adit Jain",
    "company": "Leena AI",
    "designation": "Co-founder and CEO",
    "relevance": "AI-powered enterprise employee engagement platform."
}

template = """
Hi [name],

I'm Mahesh, a 3rd-year ECE student at IIT Bhilai.
I'm interested in AI/ML and have been exploring LLMs,
RAG and backend development.

I would love to explore internship opportunities
at [company].

Would love to connect!
"""

message = generate_message(lead, template)

print("\nGenerated Message:\n")
print(message)