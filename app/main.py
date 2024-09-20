from fastapi import FastAPI, Query, Body
from typing import Optional
from pydantic import BaseModel
from model import model_inference

app = FastAPI()

# Pydantic model for JSON request
class QueryModel(BaseModel):
    instruction: str
    input: Optional[str] = ""

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Accept both JSON body and query parameters
@app.post("/ask")
def ask(
    instruction: Optional[str] = Query(None),  # query parameter
    input: Optional[str] = Query(""),  # query parameter
    body: Optional[QueryModel] = Body(None)  # JSON body
):
    # If a body is provided (JSON), prioritize it
    if body:
        instruction = body.instruction
        input = body.input
    
    if not instruction:
        return {"error": "Instruction is required!"}
    
    result = model_inference(instruction, input)
    return result
