# Importamos APIRouter para agrupar rutas relacionadas.
# Importamos HTTPException y status para manejar errores HTTP.
from fastapi import APIRouter, HTTPException, status

# Importamos la base de datos en memoria (DummyDatabase).
from fastapi_project.db import db

# Importamos los modelos de usuario (Pydantic).
from fastapi_project.schemas.user import User, UserCreate

# Creamos un router para las rutas del recurso "users".
router = APIRouter()


# --------------------------------
#      RUTA: GET /users/
# --------------------------------
@router.get("/")
async def all() -> list[User]:
    # Retornamos todos los usuarios almacenados.
    # db.users es un diccionario, por lo que convertimos los valores en lista.
    return list(db.users.values())


# ---------------------------------------
#      RUTA: GET /users/{id}
# ---------------------------------------
@router.get("/{id}")
async def get(id: int) -> User:
    try:
        # Intentamos obtener el usuario mediante su ID.
        return db.users[id]
    except KeyError:
        # Si no existe, devolvemos un error 404 (Not Found).
        raise HTTPException(status.HTTP_404_NOT_FOUND)


# ----------------------------------------
#      RUTA: POST /users/
# ----------------------------------------
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(user_create: UserCreate) -> User:
    # Generamos un nuevo ID secuencial:
    # - Si hay usuarios, tomamos el ID más alto.
    # - Si no hay usuarios, comenzamos en 1.
    new_id = max(db.users.keys() or (0,)) + 1

    # Creamos un nuevo usuario con ese ID y los datos enviados por el cliente.
    user = User(id=new_id, **user_create.model_dump())

    # Guardamos el usuario en la "base de datos" en memoria.
    db.users[new_id] = user

    # Retornamos el usuario creado.
    return user


# -----------------------------------------
#      RUTA: DELETE /users/{id}
# -----------------------------------------
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int) -> None:
    try:
        # Intentamos eliminar el usuario por su ID.
        db.users.pop(id)
    except KeyError:
        # Si el usuario no existe, devolvemos un 404.
        raise HTTPException(status.HTTP_404_NOT_FOUND)
