from fastapi import FastAPI
from typing import Optional
from enum import Enum

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/model/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name ": model_name, "message": "Deep Learning FTW"}
    if model_name == ModelName.resnet:
        return {"model_name ": model_name, "message": "LeCNN all the images"}
    return {"modem_name ": model_name, "message": "Have some residuals"}
