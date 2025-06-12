import markdown
from weasyprint import HTML,CSS
import os



class PdfService:  
        
    def convert_markdown_to_html(self, markdown_text):
        self.html_content = markdown.markdown(markdown_text, extensions=['tables', 'fenced_code'])
       
        
    def save_pdf_file(self):
        if not os.path.exists('pdf'):
            os.makedirs('pdf')

        base_dir = os.path.dirname(os.path.abspath(__file__)) 
        css_path = os.path.join(base_dir, '..', 'static', 'css', 'styles.css')
        HTML(string=self.html_content).write_pdf("pdf/output.pdf", stylesheets=[CSS(css_path)])



