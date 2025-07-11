from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.routes import ask_Q

app = FastAPI()

app.include_router(ask_Q.router, prefix="/Q", tags=["ask Question"])


@app.get("/")
def homepage():
    return JSONResponse(
        content={
            "message": "Welcome to Lexi backend test home page.",
            "instruction": "To test the API, add the URL extension '/docs'.",
            "example": "http://127.0.0.1:8000/docs",
        }
    )
