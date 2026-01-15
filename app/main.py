from typing import Annotated
from fastapi import FastAPI, Form, status, HTTPException, Response
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
import url_store

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = url_store.initialise_redis()
    yield

app = FastAPI(lifespan=lifespan)

@app.put("/", status_code = status.HTTP_200_OK)
def create(url: Annotated[str, Form()]):
    return url_store.create(url, app.state.redis)

@app.get("/{short_id}")
def resolve(short_id: str, response: Response):
    url = url_store.resolve_url(short_id, app.state.redis)
    if url is not None:
        return RedirectResponse(url = url, status_code = status.HTTP_302_FOUND)
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "url not found")

@app.get("/preview/{short_id}", status_code = status.HTTP_200_OK)
def preview(short_id: str):
    url = url_store.resolve_url(short_id, app.state.redis)
    if url is not None:
        return url
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "url not found")

@app.delete("/{short_id}", status_code = status.HTTP_200_OK)
def delete(short_id: str):
    url = url_store.resolve_url(short_id, app.state.redis)
    if url is not None:
        url_store.delete(short_id, app.state.redis)
        return "deleted: " + short_id
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "url not found")
