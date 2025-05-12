import markdown
from weasyprint import HTML,CSS
import os



class PdfService:  
        
    def convert_markdown_to_html(self, markdown_text):
        self.html_content = markdown.markdown(markdown_text, extensions=['tables', 'fenced_code'])
       
        
    def save_pdf_file(self):
        # check if the out directory exists, if not create it   
        if not os.path.exists('pdf'):
            os.makedirs('pdf')
        HTML(string=self.html_content).write_pdf("pdf/output.pdf", stylesheets=[CSS('styles.css')])



