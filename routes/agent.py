from fastapi import APIRouter, Depends
from service.agent_service  import AgentService
from fastapi import HTTPException

from pydantic import BaseModel
from fastapi_utils.cbv import cbv
from service.pdf_service import PdfService
import textwrap


router = APIRouter()

class AgentRequest(BaseModel):
    prompt: str


@cbv(router)
class AgentRouter: 

    agent_service: AgentService = Depends(AgentService)
    pdf_service: PdfService = Depends(PdfService)

    @router.post("/agent")
    def run_agent(self, request: AgentRequest):
        if not request.prompt:
            raise HTTPException(status_code=401, detail="prompt must not be empty")
        response = self.agent_service.generate_response(request.prompt)
        clean_response = textwrap.dedent(response).lstrip()
        self.pdf_service.convert_markdown_to_html(clean_response)
        self.pdf_service.save_pdf_file()
        return {"response": clean_response}