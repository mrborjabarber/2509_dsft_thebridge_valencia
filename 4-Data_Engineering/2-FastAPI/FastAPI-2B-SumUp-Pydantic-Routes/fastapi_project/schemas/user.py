# Importamos BaseModel de Pydantic.
# BaseModel permite definir modelos de datos con validación automática.
from pydantic import BaseModel


# Este modelo se utiliza cuando se crea un nuevo usuario.
# No incluye 'id' porque el servidor lo generará automáticamente.
class UserCreate(BaseModel):
    # Correo electrónico del usuario que se va a crear.
    email: str


# Modelo completo de usuario que será guardado y devuelto por la API.
class User(BaseModel):
    # Identificador único del usuario.
    id: int

    # Correo electrónico del usuario.
    email: str
