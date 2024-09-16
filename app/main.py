from .model import model_inference
from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post('/ask')
def ask(instruction: str, input: Optional[str] = ""):
    result = model_inference(instruction, input)
    return result
