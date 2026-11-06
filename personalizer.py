def generate_message(lead, template):

    replacements = {
        "[name]": lead.get("name") or "",
        "[company]": lead.get("company") or "",
        "[designation]": lead.get("designation") or ""
    }

    message = template

    for placeholder, value in replacements.items():
        message = message.replace(placeholder, value)

    return message