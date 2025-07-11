from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from ..controllers.download import downloader
from ..controllers.ask import ask_question
from ..examples.request_example import ques
from ..examples.response_example import success_response,no_data,server_error,d_success_response,d_server_error
router = APIRouter()

class QueryInput(BaseModel):
    question: str = Field(
        default=ques, title="The description of the item",
    )
    
def get_values():
    global retriever,qa_pipeline
    retriever,qa_pipeline=downloader()

@router.get("/Download/",responses={
        200: {
            "description": "A successful response",
            "content": {
                "application/json": {
                    "example": 
                        d_success_response
                    
                }
            },
        },
        500: {
            "description": "internal server error",
            "content": {
                "application/json": {
                    "example": d_server_error
                }
            },
        },
        }
        )
async def download():
    try:
        get_values()
        return {"status": "Resources loaded"}
    
    except FileNotFoundError as fnf_error:
        return JSONResponse(
            status_code=404,
            content={"error": str(fnf_error)}
        )
    
    except ValueError as ve:
        return JSONResponse(
            status_code=400,
            content={"error": str(ve)}
        )
    
    except Exception as e:
        # Optional: log the exception with print(str(e))
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )

@router.post("/ask/",responses={
        200: {
            "description": "A successful response",
            "content": {
                "application/json": {
                    "example": 
                        success_response
                    
                }
            },
        },
        404: {
            "description": "Answer Not Found",
            "content": {
                "application/json": {
                    "example": no_data
                }
            },
        },
        500: {
            "description": "internal server error",
            "content": {
                "application/json": {
                    "example": server_error
                }
            },
        },
    },)
async def ask(query: QueryInput):
    try:
        global retriever, qa_pipeline

        if not retriever or not qa_pipeline:
            return JSONResponse(
                status_code=500,
                content={"error": "Run /Download first to initialize retriever and qa_pipeline"}
            )

        response = ask_question(query.question, retriever, qa_pipeline)

        if not response or "answer" not in response or not response["answer"].strip():
            return JSONResponse(
                status_code=404,
                content={"error": "No relevant answer found"}
            )

        return JSONResponse(
            status_code=200,
            content=response
        )

    except Exception as e:
        # For debugging (optional): print(str(e)) or log to file
        return JSONResponse(
            status_code=500,
            content={"error": "Run /Download first to initialize retriever and qa_pipeline"}
        )