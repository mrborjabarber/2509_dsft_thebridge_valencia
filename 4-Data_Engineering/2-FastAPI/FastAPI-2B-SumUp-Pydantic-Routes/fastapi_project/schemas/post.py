# Importamos BaseModel, la clase base de Pydantic.
# Pydantic permite validar y estructurar datos fácilmente.
from pydantic import BaseModel


# Este modelo se usa cuando el cliente QUIERE CREAR un nuevo post.
# No incluye 'id' porque el servidor es el encargado de generarlo.
class PostCreate(BaseModel):
    # ID del usuario dueño del post
    user: int

    # Título del post
    title: str


# Este modelo representa un post COMPLETO almacenado en la base de datos.
# Incluye 'id', que identifica de manera única a cada post.
class Post(BaseModel):
    # Identificador único del post
    id: int

    # ID del usuario que creó el post
    user: int

    # Título del post
    title: str
