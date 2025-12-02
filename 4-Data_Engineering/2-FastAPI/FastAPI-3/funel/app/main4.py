from fastapi import Depends, FastAPI, Query

# Dependency Injection: Depends and Query

app = FastAPI()


async def pagination(
    skip: int = Query(0, ge=0),  # skip >= 0 , default 0
    limit: int = Query(25, ge=0),  # limit >= 0 , default 25
) -> tuple[int, int]:
    excerpt_limit = min(200, limit)
    return (skip, excerpt_limit)


# Depends uses pagination
# pagination uses Query


@app.get("/items")
async def list_items(p: tuple[int, int] = Depends(pagination)):
    skip, limit = p
    return {"skip": skip, "limit": limit}


@app.get("/things")
async def list_things(p: tuple[int, int] = Depends(pagination)):
    skip, limit = p
    return {"skip": skip, "limit": limit}
