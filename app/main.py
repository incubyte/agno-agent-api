from fastapi import FastAPI
from app.routers import index_router
from app.routers import agent_router



import asyncio
import sys

if sys.platform == "win32":
    print(sys.platform)
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


app = FastAPI()

app.include_router(index_router)
app.include_router(agent_router)


def main():
    print("Hello from agno-ai-api!")


if __name__ == "__main__":
    main()
