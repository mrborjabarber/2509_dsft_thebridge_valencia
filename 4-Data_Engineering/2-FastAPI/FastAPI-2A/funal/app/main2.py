from datetime import date
from enum import Enum

from pydantic import BaseModel

from fastapi import FastAPI

app = FastAPI()


class Gener(str, Enum):
    FANTASY = "FANTASY"
    MYSTERY = "MYSTERY"
    HORROR = "HORROR"


class BiggerBook(BaseModel):
    title: str
    author: str
    price: int
    gener: Gener
    published: date
    awards: list[str]


book2 = BiggerBook(
    title="Hamlet",
    author="Shakespeare",
    price=15,
    gener=Gener("MYSTERY"),
    published=date(1603, 1, 1),
    awards=["best-selling", "most-recommended"],
)
print(book2)

# Invalid gener
try:
    book3 = BiggerBook(
        title="Hamlet",
        author="Shakespeare",
        price=15,
        gener=Gener("MISTAKEN"),
        published=date(1603, 1, 1),
        awards=["best-selling", "popular"],
    )
except ValueError as e:
    print(str(e))


# Invalid published
try:
    book4 = BiggerBook(
        title="Hamlet",
        author="Shakespeare",
        gener=Gener("MYSTERY"),
        price=15,
        published=date(1603, 1, 51),
        awards=["best-selling", "popular"],
    )
except ValueError as e:
    print(str(e))


# Valid
book5 = BiggerBook(
    title="Hamlet",
    author="Shakespeare",
    gener=Gener("MYSTERY"),
    price=15,
    published=date(1603, 1, 1),
    awards=["best-selling", "popular"],
)
print(book5)
