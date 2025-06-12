from fastapi import FastAPI
from app.routers import index_router
from app.routers import agent_router
from app.db.engine import engine
from sqlmodel import SQLModel


import asyncio
import sys

if sys.platform == "win32":
    print(sys.platform)
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


app = FastAPI()

SQLModel.metadata.create_all(bind=engine)

app.include_router(index_router)
app.include_router(agent_router)


def main():
    print("Hello from agno-ai-api!")


if __name__ == "__main__":
    main()
