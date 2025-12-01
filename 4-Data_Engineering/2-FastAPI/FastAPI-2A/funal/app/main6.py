from pydantic import BaseModel, Field, ValidationError

from fastapi import FastAPI

app = FastAPI()


class Book(BaseModel):
    title: str = Field(..., min_length=2)
    pages: int | None = Field(None, ge=0, le=2000)


# Invalid title
try:
    Book(title="A", pages=500)
except ValidationError as e:
    print(str(e))


# Invalid pages
try:
    Book(title="Learning Python!", pages=200000)
except ValidationError as e:
    print(str(e))


# Valid
book = Book(title="We learn Python!", pages=100)
print(book)
