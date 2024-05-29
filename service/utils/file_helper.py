import extract_msg


class FileHelper:

    def load_txt_file(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content

    def load_email_json(self, file):
        msg = extract_msg.Message(file)

        subject = msg.subject
        sender = msg.sender
        to = msg.to
        date = msg.date
        body = msg.body
        email_content = {
            'Subject': f'{subject}',
            'From': f'{sender}',
            'To': f'{to}',
            'Date': f'{date}',
            'Body': f'{body}',

        }
        return email_content

    def load_email(self, file):
        msg = extract_msg.Message(file)

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
