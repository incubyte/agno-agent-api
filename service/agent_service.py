from agno.agent import Agent, RunResponse
from agno.models.anthropic import Claude


class AgentService:
    def __init__(self, model_id, tools, instructions, markdown=True):
        self.agent = Agent(
            model=Claude(id=model_id),
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



