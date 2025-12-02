# Importamos APIRouter para crear un conjunto de rutas.
# Importamos HTTPException y status para manejar errores y códigos HTTP.
from fastapi import APIRouter, HTTPException, status

# Importamos la base de datos en memoria (DummyDatabase).
from fastapi_project.db import db

# Importamos los modelos Pydantic para posts.
from fastapi_project.schemas.post import Post, PostCreate

# Creamos un router específico para las rutas relacionadas con posts.
router = APIRouter()


# -----------------------------
#       RUTA: GET /posts/
# -----------------------------
@router.get("/")
async def all() -> list[Post]:
    # Retornamos todos los posts convertidos en una lista.
    # db.posts es un diccionario → tomamos solo los valores.
    return list(db.posts.values())


# -----------------------------
#     RUTA: GET /posts/{id}
# -----------------------------
@router.get("/{id}")
async def get(id: int) -> Post:
    try:
        # Intentamos retornar el post con el ID indicado.
        return db.posts[id]
    except KeyError:
        # Si el ID no existe, devolvemos 404 (Not Found).
        raise HTTPException(status.HTTP_404_NOT_FOUND)


# ---------------------------------
#     RUTA: POST /posts/
# ---------------------------------
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(post_create: PostCreate) -> Post:
    # Antes de crear un post, verificamos que el usuario exista.
    try:
        db.users[post_create.user]
    except KeyError:
        # Si el usuario no existe, devolvemos un error 400 (Bad Request).
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f"User with id {post_create.user} doesn't exist.",
        )

    # Generamos un nuevo ID para el post.
    # max(...) obtiene el ID más alto; si está vacío, usamos 0.
    new_id = max(db.posts.keys() or (0,)) + 1

    # Creamos el objeto Post, agregando el nuevo ID
    # y los campos de PostCreate mediante .model_dump().
    post = Post(id=new_id, **post_create.model_dump())

    # Guardamos el post en la "base de datos" en memoria.
    db.posts[new_id] = post

    # Retornamos el post recién creado.
    return post


# ------------------------------------
#     RUTA: DELETE /posts/{id}
# ------------------------------------
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int) -> None:
    try:
        # Eliminamos el post por ID.
        db.posts.pop(id)
    except KeyError:
        # Si el ID no existe, retornamos un error 404 (Not Found).
        raise HTTPException(status.HTTP_404_NOT_FOUND)
