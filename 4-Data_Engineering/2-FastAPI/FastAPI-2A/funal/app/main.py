from pydantic import BaseModel

from fastapi import FastAPI


class Book(BaseModel):
    title: str
    author: str
    year: int


app = FastAPI()

book = Book(title="Hamlet", author="Shakespeare", year=1623)
print(book)
