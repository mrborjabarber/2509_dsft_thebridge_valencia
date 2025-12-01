from pydantic import BaseModel, EmailStr, HttpUrl, ValidationError

from fastapi import FastAPI

app = FastAPI()


class Client(BaseModel):
    email: EmailStr
    website: HttpUrl


# Invalid email
try:
    Client(email="xxxx", website="https://www.python.org")
except ValidationError as e:
    print(str(e))


# Invalid URL
try:
    Client(email="aromerov@faculty.ie.edu", website="wrongpage")
except ValidationError as e:
    print(str(e))


# Valid
client = Client(email="aromerov@faculty.ie.edu", website="https://www.python.org")

print(client)
