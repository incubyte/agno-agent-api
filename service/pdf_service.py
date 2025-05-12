from agno.agent import Agent, RunResponse
from agno.models.anthropic import Claude
import markdown
import pdfkit


class PdfService:    
    def __init__(self):
        # Configuration for wkhtmltopdf with correct Windows path
        self.config = pdfkit.configuration(wkhtmltopdf='D:\\tools\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
        
        # Default options for PDF generation
        self.options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None
        }    
    def convert_markdown_to_pdf(self, markdown_text):
        html = markdown.markdown(markdown_text)
        # Convert HTML to PDF using pdfkit with explicit configuration
        pdf = pdfkit.from_string(html, False, options=self.options, configuration=self.config)
        return pdf
        
    def save_pdf_to_file(self, pdf_binary, output_path):
        """
        Save binary PDF data to a file
        
        Args:
            pdf_binary (bytes): Binary PDF data
            output_path (str): Path where the PDF should be saved
            
        Returns:
            str: The path to the saved PDF file
        """
        with open(output_path, 'wb') as file:
            file.write(pdf_binary)
        return output_path



