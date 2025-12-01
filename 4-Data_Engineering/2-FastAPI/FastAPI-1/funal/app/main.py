from enum import Enum

from fastapi import Body, FastAPI, HTTPException, Path, Query, Request, status

app = FastAPI()


@app.get("/")
async def hello_world():
    return {"hello": "world"}


@app.get("/books/{id}")
async def get_book(
    id: int,
):  # the underscore is changed for a space in the swagger docs
    # get_book --> get book

    return {"id": id}


@app.get("/books/{type}/{id}")
async def get_book_type(type: str, id: int):
    return {"type": type, "id": id}


class BookType(str, Enum):  # Inheritance!
    REGULAR = "regular"
    BESTSELLER = "bestseller"


@app.get("/books-limited/{type}/{id}")
async def get_book_using_type(type: BookType, id: int):
    return {"type": type, "id": id}


@app.get("/books-greater-or-equals/{id}")
async def get_book_ge(id: int = Path(..., ge=1)):
    return {"id": id}


@app.get("/book-author/{author}")
async def get_book_author(author: str = Path(..., min_length=3, max_length=10)):
    return {"author": author}


@app.get("/books-by-query")
async def get_book_by_query(page: int = 1, size: int = 10):
    return {"page": page, "size": size}


class BooksFormat(str, Enum):
    SHORT = "short"
    FULL = "full"


@app.get("/books-format")
async def get_book_format(format: BooksFormat):
    return {"format": format}


@app.get("/books-query")
async def get_book_query(page: int = Query(1, gt=0), size: int = Query(10, le=100)):
    return {"page": page, "size": size}


@app.post("/books-body")
async def create_book(title: str = Body(...), pages: int = Body(...)):
    return {"title": title, "pages": pages}


@app.get("/home-request")
async def get_request_object(request: Request):
    return {"path": request.url.path}


@app.post("/check-id")
async def check_id(id: str = Body(...), validated_id: str = Body(...)):
    if id != validated_id:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="The id's do not match",
        )
    return {"message": "Id's match."}
