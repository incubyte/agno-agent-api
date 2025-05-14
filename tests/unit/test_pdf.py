from service.pdf_service import PdfService

# Create an instance of PdfService
pdf_service = PdfService()

# Test markdown to PDF conversion
markdown_text = """
# Test PDF Generation

This is a test of the PDF generation using pdfkit and wkhtmltopdf.

## Features

- Markdown to PDF conversion
- Custom styling
- PDF generation without WeasyPrint dependencies

"""

# Convert markdown to PDF
pdf_data = pdf_service.convert_markdown_to_pdf(markdown_text)

# Save the PDF to a file
with open("test_output.pdf", "wb") as f:
    f.write(pdf_data)

print("PDF generated successfully and saved as test_output.pdf")
