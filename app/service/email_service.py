import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from app.core import settings
import os

class EmailService:
    def __init__(self, smtp_server='smtp.gmail.com', smtp_port=587, sender_email=settings.SENDER_EMAIL, sender_password=settings.SENDER_PASSWORD):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.server = None

    def connect(self):
        """Connect to the SMTP server and login"""
        self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        self.server.starttls()
        self.server.login(self.sender_email, self.sender_password)
        print("Connected to SMTP server successfully.")

    def send_email(self, to_email, subject, body, logo_path=None, pdf_path=None):
        """Send an email with optional embedded logo and PDF attachment"""
        msg = MIMEMultipart('related')
        msg['From'] = self.sender_email
        msg['To'] = to_email
        msg['Subject'] = subject

        html_body = f"""
        <html>
        <body>
            {'<img src="cid:logo" style="height:50px;"><br><br>' if logo_path else ''}
            <p>{body}</p>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_body, 'html'))

        if logo_path and os.path.isfile(logo_path):
            with open(logo_path, 'rb') as img:
                mime_image = MIMEImage(img.read())
                mime_image.add_header('Content-ID', '<logo>')
                msg.attach(mime_image)
            print("Logo attached.")

        if pdf_path and os.path.isfile(pdf_path):
            with open(pdf_path, 'rb') as pdf_file:
                pdf_attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")
                pdf_attachment.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=os.path.basename(pdf_path)
                )
                msg.attach(pdf_attachment)
            print("PDF attached.")

        self.server.send_message(msg)
        print(f"Email sent to {to_email}.")

    def disconnect(self):
        """Close the SMTP connection"""
        if self.server:
            self.server.quit()
            print("Disconnected from SMTP server.")

