import markdown
from weasyprint import HTML,CSS


class PdfService:  
        
    def convert_markdown_to_html(self, markdown_text):
        self.html_content = markdown.markdown(markdown_text, extensions=['tables', 'fenced_code'])
       
        
    def save_pdf_file(self):
        HTML(string=self.html_content).write_pdf("output.pdf", stylesheets=[CSS('styles.css')])



