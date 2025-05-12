from fastapi import APIRouter, Depends
from service.agent_service  import AgentService

from pydantic import BaseModel
from fastapi_utils.cbv import cbv

router = APIRouter()

class AgentRequest(BaseModel):
    prompt: str


@cbv(router=router)
class AgentRouter: 

    agent_service: AgentService = Depends(AgentService)

    @router.post("/agent")
    def run_agent(self, request: AgentRequest):
        response = self.agent_service.generate_response(request.prompt)
        return {"response": response}