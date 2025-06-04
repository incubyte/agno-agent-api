from fastapi import APIRouter, Depends
from app.service  import AgentService
from fastapi import HTTPException

from pydantic import BaseModel
from fastapi_utils.cbv import cbv
from app.service import PdfService
from app.service import EmailService
from app.agents.marketing_agents import MarketingAgent
from app.agents.homepage_generator import HomepageGeneratorAgent
import textwrap



router = APIRouter()

class AgentRequest(BaseModel):
    prompt: str
    user_email: str


class MarketingAgentRequest(BaseModel):
    url: str
    user_email: str


class HomepageGeneratorRequest(BaseModel):
    url: str
    output_format: str = "markdown"
    user_email: str


@cbv(router)
class AgentRouter: 

    agent_service: AgentService = Depends(AgentService)
    pdf_service: PdfService = Depends(PdfService)
    email_service: EmailService = Depends(EmailService)  
    marketing_agent: MarketingAgent = Depends(MarketingAgent)
    homepage_generator: HomepageGeneratorAgent = Depends(HomepageGeneratorAgent)

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
    

    
    @router.post("/run-marketing-agent")
    def run_marketing_agent(self, request: MarketingAgentRequest):
        if not request.url:
            raise HTTPException(status_code=400, detail="url must not be empty")
        if not request.user_email:
            raise HTTPException(status_code=400, detail="user_email must not be empty")
        marketing_agent = MarketingAgent()
        response = marketing_agent.run_marketing_agent(request.url)
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
        
    @router.post("/run-homepage-generator")
    def run_homepage_generator(self, request: HomepageGeneratorRequest):
        if not request.url:
            raise HTTPException(status_code=400, detail="url must not be empty")
        if not request.user_email:
            raise HTTPException(status_code=400, detail="user_email must not be empty")
        
        # Initialize the homepage generator agent
        homepage_agent = HomepageGeneratorAgent()
        
        try:
            # Run the homepage generator using the synchronous wrapper method
            # This handles the asyncio issues internally
            response = homepage_agent.run_homepage_generator(
                url=request.url,
                output_format=request.output_format
            )
            
            # Process the response
            clean_response = textwrap.dedent(response).lstrip()
            self.pdf_service.convert_markdown_to_html(clean_response)
            self.pdf_service.save_pdf_file()
            
            # Send email with the result
            self.email_service.connect()
            self.email_service.send_email(
                to_email=request.user_email,
                subject="Homepage Generator Results",
                body="Please find the attached homepage content PDF.",
                pdf_path="pdf/output.pdf"
            )
            print("Email sent successfully.")
            self.email_service.disconnect()
            
            return {"response": clean_response}
        except Exception as e:
            print(f"Error in homepage generator: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to generate homepage: {str(e)}")