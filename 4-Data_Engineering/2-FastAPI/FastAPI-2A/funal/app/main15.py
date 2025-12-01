from pydantic import BaseModel

from fastapi import FastAPI, status

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


class DummyBookDatabase:
    posts: dict[int, JustPost] = {}


db = DummyBookDatabase()


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# This endpoint post /posts receives a Data Model with title and content
# calculates the id_new
# creates a ReadAPost Data Model
# which has an id and title and content
# ** deconstructs the object of type MakeAPost (like a dictionary)


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=ReadAPost)
async def create(
    create_post: MakeAPost,
):  # MakeAPost is a Data Model with title and content
    id_new = max(db.posts.keys() or (0,)) + 1  # The tuple is to make it iterable

    posted = ReadAPost(
        id=id_new, **create_post.model_dump()
    )  # id = id_new, title = ..., content = ...

    db.posts[id_new] = posted
    return posted
