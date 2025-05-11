from fastapi import FastAPI
from routes.index import router  # Import the router object explicitly

app = FastAPI()

app.include_router(router)  


def main():
    print("Hello from agno-ai-api!")


if __name__ == "__main__":
    main()
