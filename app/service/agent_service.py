from agno.agent import Agent, RunResponse
from agno.models.anthropic import Claude
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools
from app.core import settings


tools=[
        ReasoningTools(add_instructions=True),
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True,
        ),
    ]
instructions=[
    "Use tables to display data",
    "Only output the report, no other text",
]

class AgentService:
    def __init__(self, model_id='claude-3-7-sonnet-latest', tools=tools, instructions=instructions, markdown=True):
        self.agent = Agent(
            model=Claude(id=model_id, api_key=settings.ANTHROPIC_API_KEY,),
            tools=tools,
            instructions=instructions,
            markdown=markdown,
        )

    def generate_response(self, query):
        response: RunResponse = self.agent.run(
            query,
            markdown=self.agent.markdown,
        )
        return response.content



