from fastapi import APIRouter
from service.agent_service  import AgentService
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools
from pydantic import BaseModel

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
    ]

agent_service = AgentService(model_id="claude-3-7-sonnet-latest", tools=tools,instructions=[
  "Use tables to display data",
  "Only output the report, no other text",
],
                              markdown=True)

@router.post("/agent")
def run_agent(request: AgentRequest):
    response = agent_service.generate_response(request.prompt)
    return {"response": response, }