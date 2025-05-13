from fastapi import APIRouter, Depends
from service.agent_service  import AgentService
from fastapi import HTTPException

from pydantic import BaseModel
from fastapi_utils.cbv import cbv
from service.pdf_service import PdfService
from service.email_service import EmailService
import textwrap


router = APIRouter()

class AgentRequest(BaseModel):
    prompt: str
    user_email: str


@cbv(router)
class AgentRouter: 

    agent_service: AgentService = Depends(AgentService)
    pdf_service: PdfService = Depends(PdfService)
    email_service: EmailService = Depends(EmailService)  

    @router.post("/agent")
    def run_agent(self, request: AgentRequest):
        if not request.prompt:
            raise HTTPException(status_code=400, detail="prompt must not be empty")
        if not request.user_email:
            raise HTTPException(status_code=400, detail="user_email must not be empty")
        response = self.agent_service.generate_response(request.prompt)
        clean_response = textwrap.dedent(response).lstrip()
        self.pdf_service.convert_markdown_to_html(clean_response)
        self.pdf_service.save_pdf_file()
        try:
            self.email_service.connect()
            self.email_service.send_email(
                to_email=request.user_email,
                subject="Test Email",
                body="Please find the attached PDF.",
                pdf_path="pdf/output.pdf"
            )
            print("Email sent successfully.")
            self.email_service.disconnect()
        except Exception as e:
            print(f"Failed to send email: {e}")
            raise HTTPException(status_code=500, detail="Failed to send email")

        return {"response": clean_response}