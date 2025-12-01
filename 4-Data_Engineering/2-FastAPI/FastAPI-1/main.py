from fastapi import FastAPI
from enum import Enum # Se importa Enum
from fastapi import FastAPI, Path

app = FastAPI()

class BookType(str, Enum):  # ¡Herencia!
    REGULAR = "regular"
    BESTSELLER = "bestseller"

@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get("/books/{id}")
async def get_book(id: int):
    return {"id": id}


@app.get("/books/{type}/{id}")
async def get_book_type(type: str, id: int):
    return {"type": type, "id": id}


@app.get("/books-limited/{type}/{id}")
async def get_book_using_type(type: BookType, id: int):
    return {"type": type, "id": id}


@app.get("/books-greater-or-equals/{id}")
async def get_book_ge(id: int = Path(..., ge=1)):
    return {"id": id}

@app.get("/book-author/{author}")
async def get_book_author(author: str = Path(..., min_length=3, max_length=10)):
    return {"author": author}