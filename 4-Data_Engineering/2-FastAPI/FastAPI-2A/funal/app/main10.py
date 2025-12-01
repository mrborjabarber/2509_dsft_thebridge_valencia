from pydantic import BaseModel

from fastapi import FastAPI

app = FastAPI()

# Inheritance!


class PostBase(BaseModel):
    title: str
    content: str

    def fragment(self) -> str:
        return f"{self.content[:200]}..."  # First 200 characters


class MakeAPost(PostBase):
    pass


class ReadAPost(PostBase):
    id: int


class JustPost(ReadAPost):
    nb_views: int = 0
