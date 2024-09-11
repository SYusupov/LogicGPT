from model import model_inference

from fastapi import FastAPI

from typing import Union

app = FastAPI()

@app.get("/")
# whenever smb does get request, do things below
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
# whenever smb does get request with /items/item_id where item_id is an integer, do things below
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post('/ask')
def ask(instruction: str, input: str):
    result = model_inference(instruction, input)
    return result