from fastapi import FastAPI
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
from src.routes import ask_Q

app = FastAPI()

app.include_router(ask_Q.router, prefix="/Q", tags=["ask Question"])

@app.get("/")
def homepage():
    return "lexi backend test home page"

handler = Mangum(app)
