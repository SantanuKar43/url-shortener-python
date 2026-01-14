from typing import Annotated
from fastapi import FastAPI, Form, status, HTTPException, Response
import url_store

app = FastAPI()

@app.put("/", status_code = status.HTTP_200_OK)
def create(url: Annotated[str, Form()]):
    return url_store.create(url)

@app.get("/{short_id}")
def resolve(short_id: str, response: Response):
    url = url_store.get(short_id)
    if url is not None:
        response.headers["Location"] = url
        response.status_code = status.HTTP_302_FOUND
        return
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "url not found")

@app.get("/preview/{short_id}", status_code = status.HTTP_200_OK)
def preview(short_id: str):
    url = url_store.get(short_id)
    if url is not None:
        return url
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "url not found")

@app.delete("/{short_id}", status_code = status.HTTP_200_OK)
def delete(short_id: str):
    url = url_store.get(short_id)
    if url is not None:
        url_store.delete(short_id)
        return "deleted: " + short_id
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "url not found")
