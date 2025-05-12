from fastapi import APIRouter
from service.agent_service  import AgentService
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.googlesearch import GoogleSearchTools
from pydantic import BaseModel
from service.pdf_service import PdfService

router = APIRouter()

class AgentRequest(BaseModel):
    prompt: str


tools=[
        ReasoningTools(add_instructions=True),
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True,
        ),
        GoogleSearchTools(),
    ]

agent_service = AgentService(model_id="claude-3-7-sonnet-latest", tools=tools,instructions=[
  "Use tables to display data",
  "Only output the report, no other text",
],
                              markdown=True)

pdf_service = PdfService()

@router.post("/agent")
def run_agent(request: AgentRequest):
    response = agent_service.generate_response(request.prompt)
    pdf_binary =  pdf_service.convert_markdown_to_pdf(response)
    pdf_path = pdf_service.save_pdf_to_file(pdf_binary, "output.pdf")
    return {"response": response, }