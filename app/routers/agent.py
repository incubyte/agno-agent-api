from fastapi import APIRouter, Depends
from app.agents.agent_factory import AgentFactory
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
        if not created_agent:
            raise HTTPException(status_code=400, detail="Failed to create agent")
        return created_agent
    

    @router.post("/run-agent/{agent_id}")
    def run_agent_by_id(self, agent_id: int, request: AgentRequest):
        if not request.prompt:
            raise HTTPException(status_code=400, detail="Url must not be empty")
        if not request.user_email:
            raise HTTPException(status_code=400, detail="user_email must not be empty")
        
        agent_data = AgentRepository.get_by_id(agent_id)
        if not agent_data:
            raise HTTPException(status_code=404, detail="Agent data not found")
        
        agent = AgentFactory.get_agent(agent_data.slug)
        response = agent.get_response(request.prompt)
        clean_response = textwrap.dedent(response).lstrip()
        return {"response": clean_response}



