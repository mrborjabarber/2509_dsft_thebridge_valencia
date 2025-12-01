from datetime import date

from pydantic import BaseModel, ValidationError, field_validator


class Book(BaseModel):
    title: str
    published: date

    @field_validator("published")
    def valid_published_book(cls, d: date):
        delta = date.today() - d
        age_of_the_book = delta.days / 365
        if age_of_the_book > 525:
            raise ValueError("You are an incunable!")
        return d


# Invalid age of a book
try:
    Book(title="What an old book!", published="1490-01-01")
except ValidationError as e:
    print(str(e))

# Valid
book = Book(title="A new book", published="2025-01-01")
print(book)
