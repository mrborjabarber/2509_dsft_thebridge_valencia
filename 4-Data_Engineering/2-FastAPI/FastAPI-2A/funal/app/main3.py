from datetime import date
from enum import Enum

from pydantic import BaseModel

from fastapi import FastAPI


class Gener(str, Enum):
    FANTASY = "FANTASY"
    MYSTERY = "MYSTERY"
    HORROR = "HORROR"


class Library(BaseModel):
    name: str
    postal_code: str
    city: str
    country: str


class BookForALibrary(BaseModel):
    title: str
    author: str
    price: int
    gener: Gener
    published: date
    awards: list[str]
    library: Library


app = FastAPI()

book6 = BookForALibrary(
    title="Hamlet",
    author="Shakespeare",
    price=15,
    gener=Gener("MYSTERY"),
    published=date(1603, 1, 1),
    awards=["best-selling", "most-recommended"],
    library=Library(
        name="Old Library", postal_code="123ABC", city="Madrid", country="Spain"
    ),
)
print(book6)

# Invalid library
try:
    book7 = BookForALibrary(
        title="Hamlet",
        author="Shakespeare",
        price=15,
        gener=Gener("MYSTERY"),
        published=date(1603, 1, 1),
        awards=["best-selling", "popular"],
        library=Library(name="Old Library", postal_code="123ABC", city="Madrid"),
    )
except ValueError as e:
    print(str(e))


book8 = BookForALibrary(
    title="Othello",
    author="Shakespeare",
    price=15,
    gener=Gener("MYSTERY"),
    published=date(1603, 1, 1),
    awards=["best-selling", "most-recommended"],
    library={
        "name": "New Library",
        "postal_code": "123ABC",
        "city": "Madrid",
        "country": "Spain",
    },
)
print(book8)
