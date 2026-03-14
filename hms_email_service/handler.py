import json
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
load_dotenv()
def send_email_handler(event, context):
    try:
        # data from the Django request
        body = json.loads(event.get("body", "{}"))
        recipient = body.get("email")
        subject = body.get("subject")
        message_text = body.get("message")

        if not recipient:
            return {"statusCode": 400, "body": json.dumps({"error": "No recipient"})}

        # 2. SMTP Configuration
        sender_email = 'muskantarafder357@gmail.com'
        sender_password = '16digit password'

        # 3. Create Email
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient
        message["Subject"] = subject
        message.attach(MIMEText(message_text, "plain"))

        # 4. Send Email via SSL
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, message.as_string())

        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"message": "Email sent successfully!"})
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }