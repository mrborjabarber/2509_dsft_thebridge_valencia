from pydantic import BaseModel

from fastapi import FastAPI

app = FastAPI()

# How repetitive!


class MakeAPost(BaseModel):
    title: str
    content: str


class ReadAPost(BaseModel):
    id: int
    title: str
    content: str


class JustPost(BaseModel):
    id: int
    title: str
    content: str
    nb_views: int = 0
