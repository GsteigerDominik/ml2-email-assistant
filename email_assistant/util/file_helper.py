import extract_msg


def load_txt_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def load_email(path):
    msg = extract_msg.Message(path)

    subject = msg.subject
    sender = msg.sender
    to = msg.to
    date = msg.date
    body = msg.body

    email_content = f"Subject: {subject}\n"
    email_content += f"From: {sender}\n"
    email_content += f"To: {to}\n"
    email_content += f"Date: {date}\n\n"
    email_content += f"Body:\n{body}"
    return email_content
