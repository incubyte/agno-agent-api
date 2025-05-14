import pytest
from unittest.mock import MagicMock, patch, ANY
import os
import sys
import importlib.util

sys.modules['core'] = MagicMock()
sys.modules['core.settings'] = MagicMock()

# Mock the app modules to avoid circular imports
sys.modules['app.main'] = MagicMock()
sys.modules['app.core'] = MagicMock()
sys.modules['app.service.agent_service'] = MagicMock()
# Import EmailService using importlib.util to properly locate the module
spec = importlib.util.spec_from_file_location(
    "email_service",
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../app/service/email_service.py'))
)
email_service_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(email_service_module)
EmailService = email_service_module.EmailService


class TestEmailService:
    def setup_method(self):
        """Setup method run before each test"""
        self.mock_smtp_server = "test.smtp.server"
        self.mock_port = 123
        self.mock_sender_email = "test@example.com"
        self.mock_sender_password = "test_password"        
        with patch.object(email_service_module, 'smtplib'):
            self.email_service = EmailService(
                smtp_server=self.mock_smtp_server,
                smtp_port=self.mock_port,
                sender_email=self.mock_sender_email,
                sender_password=self.mock_sender_password
            )    
    
    @patch.object(email_service_module, 'smtplib')
    def test_init(self, mock_smtp):
        """Test that EmailService initializes with correct parameters"""
        email_service = EmailService(
            smtp_server=self.mock_smtp_server,
            smtp_port=self.mock_port,
            sender_email=self.mock_sender_email,
            sender_password=self.mock_sender_password
        )
        
        assert email_service.smtp_server == self.mock_smtp_server
        assert email_service.smtp_port == self.mock_port
        assert email_service.sender_email == self.mock_sender_email
        assert email_service.sender_password == self.mock_sender_password
        assert email_service.server is None  

    @patch.object(email_service_module, 'smtplib')
    def test_connect(self, mock_smtp):
        """Test connect method establishes connection and logs in"""
        mock_smtp_instance = MagicMock()
        mock_smtp.SMTP.return_value = mock_smtp_instance
        self.email_service.connect()
        
        mock_smtp.SMTP.assert_called_once_with(self.mock_smtp_server, self.mock_port)
        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_once_with(
            self.mock_sender_email, 
            self.mock_sender_password
        )
        
        assert self.email_service.server == mock_smtp_instance    
      
    @patch.object(email_service_module, 'os')
    @patch.object(email_service_module, 'open')
    @patch.object(email_service_module, 'smtplib')
    def test_send_email_basic(self, mock_smtp, mock_open, mock_os):
        """Test sending a basic email without attachments"""
        mock_smtp_instance = MagicMock()
        mock_smtp.SMTP.return_value = mock_smtp_instance
        self.email_service.server = mock_smtp_instance
        
        to_email = "recipient@example.com"
        subject = "Test Subject"
        body = "Test body content"
        
        self.email_service.send_email(to_email, subject, body)
        
        mock_smtp_instance.send_message.assert_called_once()
        
        sent_msg = mock_smtp_instance.send_message.call_args[0][0]
        assert sent_msg['From'] == self.mock_sender_email
        assert sent_msg['To'] == to_email
        assert sent_msg['Subject'] == subject
        
        mock_os.path.isfile.assert_not_called()
        mock_open.assert_not_called()    
    
    @patch.object(email_service_module, 'os')
    @patch.object(email_service_module, 'open')
    @patch.object(email_service_module, 'MIMEImage')
    @patch.object(email_service_module, 'smtplib')
    def test_send_email_with_logo(self, mock_smtp, mock_mime_image, mock_open, mock_os):
        """Test sending an email with a logo attachment"""
        mock_smtp_instance = MagicMock()
        mock_smtp.SMTP.return_value = mock_smtp_instance
        self.email_service.server = mock_smtp_instance
        
        mock_os.path.isfile.return_value = True
        
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        mock_mime_image_instance = MagicMock()
        mock_mime_image.return_value = mock_mime_image_instance
        
        to_email = "recipient@example.com"
        subject = "Test Subject"
        body = "Test body content"
        logo_path = "/path/to/logo.png"
        
        self.email_service.send_email(to_email, subject, body, logo_path=logo_path)
        mock_smtp_instance.send_message.assert_called_once()
        
        mock_os.path.isfile.assert_called_with(logo_path)
        mock_open.assert_called_with(logo_path, 'rb')
        
        mock_mime_image.assert_called_once()
        mock_mime_image_instance.add_header.assert_called_with('Content-ID', '<logo>')
    
    @patch.object(email_service_module, 'os')
    @patch.object(email_service_module, 'open')
    @patch.object(email_service_module, 'MIMEApplication')
    @patch.object(email_service_module, 'smtplib')
    def test_send_email_with_pdf(self, mock_smtp, mock_mime_app, mock_open, mock_os):
        """Test sending an email with a PDF attachment"""
        mock_smtp_instance = MagicMock()
        mock_smtp.SMTP.return_value = mock_smtp_instance
        self.email_service.server = mock_smtp_instance
        
        mock_os.path.isfile.return_value = True
        
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        mock_mime_app_instance = MagicMock()
        mock_mime_app.return_value = mock_mime_app_instance
        
        to_email = "recipient@example.com"
        subject = "Test Subject"
        body = "Test body content"
        pdf_path = "/path/to/document.pdf"
        pdf_filename = "document.pdf"
        
        self.email_service.send_email(to_email, subject, body, pdf_path=pdf_path)
        mock_smtp_instance.send_message.assert_called_once()
        
        mock_os.path.isfile.assert_called_with(pdf_path)
        mock_open.assert_called_with(pdf_path, 'rb')
        
        mock_mime_app.assert_called_once_with(mock_file.read(), _subtype="pdf")
        mock_mime_app_instance.add_header.assert_called_with(
            'Content-Disposition',
            'attachment',
            filename=ANY
        )
    
    @patch.object(email_service_module, 'os')
    @patch.object(email_service_module, 'open')
    @patch.object(email_service_module, 'MIMEImage')
    @patch.object(email_service_module, 'MIMEApplication')
    @patch.object(email_service_module, 'smtplib')
    def test_send_email_with_both_attachments(self, mock_smtp, mock_mime_app, mock_mime_image,
                                            mock_open, mock_os):
        """Test sending an email with both logo and PDF attachments"""
        mock_smtp_instance = MagicMock()
        mock_smtp.SMTP.return_value = mock_smtp_instance
        self.email_service.server = mock_smtp_instance
        
        mock_os.path.isfile.return_value = True
        
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        mock_mime_image_instance = MagicMock()
        mock_mime_image.return_value = mock_mime_image_instance
        
        mock_mime_app_instance = MagicMock()
        mock_mime_app.return_value = mock_mime_app_instance
        
        to_email = "recipient@example.com"
        subject = "Test Subject"
        body = "Test body content"
        logo_path = "/path/to/logo.png"
        pdf_path = "/path/to/document.pdf"
        
        self.email_service.send_email(to_email, subject, body, logo_path=logo_path, pdf_path=pdf_path)
        mock_smtp_instance.send_message.assert_called_once()
        
        assert mock_os.path.isfile.call_count >= 2
        assert mock_open.call_count >= 2
        mock_mime_image.assert_called_once()
        mock_mime_app.assert_called_once()
    
    @patch.object(email_service_module, 'smtplib')
    def test_disconnect(self, mock_smtp):
        """Test disconnect method closes the connection"""
        mock_smtp_instance = MagicMock()
        self.email_service.server = mock_smtp_instance
        
        self.email_service.disconnect()
        
        mock_smtp_instance.quit.assert_called_once()
