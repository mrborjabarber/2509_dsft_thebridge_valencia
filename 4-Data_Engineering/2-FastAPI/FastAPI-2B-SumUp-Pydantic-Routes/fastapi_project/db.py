# Importamos los esquemas (modelos Pydantic) de Post y User.
# Estos modelos definen la estructura de los datos que se guardarán.
from fastapi_project.schemas.post import Post
from fastapi_project.schemas.user import User


# Creamos una clase que simula una base de datos en memoria.
class DummyDatabase:
    # Diccionario para almacenar usuarios.
    # La clave es un entero (id del usuario) y el valor es un objeto User.
    users: dict[int, User] = {}

    # Diccionario para almacenar posts.
    # La clave es un entero (id del post) y el valor es un objeto Post.
    posts: dict[int, Post] = {}


# Instancia única de DummyDatabase que actuará como "base de datos".
db = DummyDatabase()
