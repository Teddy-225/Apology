from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Email credentials (stored securely in .env file)
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


@app.route('/api/send-email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()
        recipient = data.get("to", "default@example.com")  # Default recipient
        subject = data.get("subject", "No Subject")
        message = data.get("message", "No message provided.")

        # Create email content
        email_body = f"Subject: {subject}\n\n{message}"

        # Send email using SMTP
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient, email_body)

        return jsonify({"status": "success", "message": "Email sent successfully!"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
