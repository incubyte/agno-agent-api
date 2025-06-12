from sqlmodel import select
from app.db.models import Agent
from app.db.engine import session


class AgentRepository:

    @staticmethod
    def get_all():
        return session.exec(select(Agent)).all()

    @staticmethod
    def get_by_id(agent_id: int):
        return session.get(Agent, agent_id)

    @staticmethod
    def create(agent: Agent):
        session.add(agent)
        session.commit()
        session.refresh(agent)
        return agent
