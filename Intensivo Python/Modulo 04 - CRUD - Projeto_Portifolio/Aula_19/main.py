from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/jornada")
def read_jornada():
    return {"Nossa primeira": "API"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/dobro/{valor}")
def read_item(valor: int):
    return {"valor": valor, "dobro": valor * 2}