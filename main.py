from fastapi import FastAPI
from routes.index import router as index_router 
from routes.agent import router as agent_router 


app = FastAPI()

app.include_router(index_router)
app.include_router(agent_router)


def main():
    print("Hello from agno-ai-api!")


if __name__ == "__main__":
    main()
