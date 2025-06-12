from fastapi import APIRouter, Depends
from app.service  import AgentService
from fastapi import HTTPException

from pydantic import BaseModel
from fastapi_utils.cbv import cbv
from app.service import PdfService
from app.service import EmailService
from app.agents.marketing_agents import MarketingAgent
import textwrap
from app.db.repository.agent_repository import  AgentRepository
from app.db.models import Agent


router = APIRouter()

class AgentRequest(BaseModel):
    prompt: str
    user_email: str


class MarketingAgentRequest(BaseModel):
    url: str
    user_email: str


@cbv(router)
class AgentRouter: 

    agent_service: AgentService = Depends(AgentService)
    pdf_service: PdfService = Depends(PdfService)
    email_service: EmailService = Depends(EmailService)  
    marketing_agent: MarketingAgent = Depends(MarketingAgent)


    @router.get("/agents")
    def get_agents(self):
        agents = AgentRepository.get_all()
        if not agents:
            raise HTTPException(status_code=404, detail="No agents found")
        return agents
    
    @router.post("/create-agent")
    def create_agent(self, agent: Agent): 
        created_agent = AgentRepository.create(agent)
        return created_agent

    @router.post("/agent")
    def run_agent(self, request: AgentRequest):
        if not request.prompt:
            raise HTTPException(status_code=400, detail="prompt must not be empty")
        if not request.user_email:
            raise HTTPException(status_code=400, detail="user_email must not be empty")
        
        clean_response = "Hello"
        # use orm and get all agents 
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
    

