from pydantic import BaseModel

from fastapi import FastAPI


class Book(BaseModel):
    title: str
    shop: str | None = None
    anonymous: bool = True


app = FastAPI()

book = Book(title="MacBeth")
print(book)
