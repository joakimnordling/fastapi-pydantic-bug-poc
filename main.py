from typing import Union, List

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get(
    "/items/{item_id}",
    response_model=Item,
)
def read_item(item_id: int):
    return Item(name=f"Item {item_id}")
