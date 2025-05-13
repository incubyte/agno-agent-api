import os
import unittest
from unittest.mock import patch, Mock, mock_open
import markdown
from service.pdf_service import PdfService

class TestPdfService(unittest.TestCase):
    def setUp(self):
        self.pdf_service = PdfService()
        
        self.sample_markdown = "# Test Heading\n\n* Item 1\n* Item 2\n\n| Column 1 | Column 2 |\n|----------|----------|\n| Data 1   | Data 2   |\n\n```python\nprint('Hello World')\n```"
        
        self.expected_html = markdown.markdown(self.sample_markdown, extensions=['tables', 'fenced_code'])

    def test_convert_markdown_to_html(self):
        """Test the conversion of markdown to HTML"""
        self.pdf_service.convert_markdown_to_html(self.sample_markdown)
        
        self.assertEqual(self.pdf_service.html_content, self.expected_html)
        
        self.pdf_service.convert_markdown_to_html("")
        self.assertEqual(self.pdf_service.html_content, "")
    
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('service.pdf_service.HTML')
    def test_save_pdf_file_with_existing_directory(self, mock_html, mock_makedirs, mock_exists):
        """Test saving PDF when the directory already exists"""
        mock_exists.return_value = True
        mock_html_instance = Mock()
        mock_html.return_value = mock_html_instance
        
        self.pdf_service.html_content = self.expected_html
        
        self.pdf_service.save_pdf_file()
        
        mock_exists.assert_called_once_with('pdf')
        
        mock_makedirs.assert_not_called()
        
        mock_html.assert_called_once_with(string=self.expected_html)
        
        mock_html_instance.write_pdf.assert_called_once()
        args, kwargs = mock_html_instance.write_pdf.call_args
        self.assertEqual(args[0], "pdf/output.pdf")
        self.assertEqual(len(kwargs['stylesheets']), 1)
    
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('service.pdf_service.HTML')
    def test_save_pdf_file_without_existing_directory(self, mock_html, mock_makedirs, mock_exists):
        """Test saving PDF when the directory does not exist"""
        mock_exists.return_value = False
        mock_html_instance = Mock()
        mock_html.return_value = mock_html_instance
        
        self.pdf_service.html_content = self.expected_html
        
        self.pdf_service.save_pdf_file()
        
        mock_exists.assert_called_once_with('pdf')
        
        mock_makedirs.assert_called_once_with('pdf')
        
        mock_html.assert_called_once_with(string=self.expected_html)
        
        mock_html_instance.write_pdf.assert_called_once()
        args, kwargs = mock_html_instance.write_pdf.call_args
        self.assertEqual(args[0], "pdf/output.pdf")
        self.assertEqual(len(kwargs['stylesheets']), 1)
    
    @patch('service.pdf_service.CSS')
    @patch('service.pdf_service.HTML')
    def test_css_styling_applied(self, mock_html, mock_css):
        """Test that CSS styling is correctly applied to the PDF"""
        mock_html_instance = Mock()
        mock_html.return_value = mock_html_instance
        mock_css_instance = Mock()
        mock_css.return_value = mock_css_instance
        
        self.pdf_service.html_content = self.expected_html
        
        self.pdf_service.save_pdf_file()
        
        mock_css.assert_called_once_with('styles.css')
        
        mock_html_instance.write_pdf.assert_called_once()
        args, kwargs = mock_html_instance.write_pdf.call_args
        self.assertEqual(kwargs['stylesheets'], [mock_css_instance])

    def test_end_to_end_conversion(self):
        """Test the entire conversion process from markdown to PDF"""
        with patch('service.pdf_service.HTML') as mock_html:
            mock_html_instance = Mock()
            mock_html.return_value = mock_html_instance
            
            self.pdf_service.convert_markdown_to_html(self.sample_markdown)
            self.pdf_service.save_pdf_file()
            
            self.assertEqual(self.pdf_service.html_content, self.expected_html)
            
            mock_html.assert_called_once_with(string=self.expected_html)
            
            mock_html_instance.write_pdf.assert_called_once()