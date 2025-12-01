"""
main_completo.py

Aplicación FastAPI completa con base de datos SQLite.

Esta es la aplicación principal que integra todos los componentes:
- database.py: Configuración de la base de datos
- models.py: Modelos SQLAlchemy
- schemas.py: Schemas Pydantic
- crud.py: Operaciones CRUD

Para ejecutar:
    uvicorn main_completo:app --reload

Para acceder a la documentación:
    http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn

# Importamos nuestros módulos
import models
import schemas
import crud
from database import engine, get_db

# ============================================
# CREACIÓN DE TABLAS
# ============================================

# Creamos todas las tablas definidas en models.py
# Base.metadata.create_all() lee todos los modelos que heredan de Base
# y crea las tablas correspondientes si no existen
models.Base.metadata.create_all(bind=engine)

# ============================================
# INICIALIZACIÓN DE LA APLICACIÓN
# ============================================

app = FastAPI(
    title="FastAPI Bootcamp - Aplicación Completa",
    description="""
    API completa con base de datos SQLite para el bootcamp de FastAPI.

    ## Características

    * **Usuarios**: CRUD completo de usuarios
    * **Items**: CRUD completo de items con relación a usuarios
    * **Tags**: Sistema de etiquetado para items
    * **Validación**: Validación automática con Pydantic
    * **Documentación**: Documentación interactiva automática

    ## Recursos

    Puedes probar todos los endpoints desde esta interfaz interactiva.
    """,
    version="3.0.0",
    contact={
        "name": "FastAPI Bootcamp",
        "url": "https://fastapi.tiangolo.com/",
    },
    license_info={
        "name": "MIT",
    },
)

# ============================================
# ENDPOINTS RAÍZ Y DE INFORMACIÓN
# ============================================

@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint raíz de la API.

    Retorna información básica sobre la API y sus recursos disponibles.
    """
    return {
        "mensaje": "Bienvenido a la API del Bootcamp de FastAPI",
        "version": "3.0.0",
        "documentacion": "/docs",
        "recursos": {
            "usuarios": "/users/",
            "items": "/items/",
            "tags": "/tags/"
        }
    }

@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint.

    Útil para verificar que la API está funcionando correctamente.
    Especialmente importante en entornos de producción para monitoring.
    """
    return {
        "status": "healthy",
        "database": "connected"
    }

# ============================================
# ENDPOINTS DE USUARIOS
# ============================================

@app.post(
    "/users/",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
    summary="Crear un nuevo usuario"
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo usuario en la base de datos.

    Args:
        user: Datos del usuario a crear (email, username, password)
        db: Sesión de base de datos (inyectada automáticamente)

    Returns:
        Usuario creado con su ID y fecha de creación

    Raises:
        HTTPException 400: Si el email o username ya están registrados

    Ejemplo de request body:
    ```json
    {
        "email": "usuario@ejemplo.com",
        "username": "usuario_ejemplo",
        "password": "Password123"
    }
    ```
    """
    # Verificamos si el email ya existe
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    # Verificamos si el username ya existe
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El username ya está en uso"
        )

    # Creamos el usuario
    return crud.create_user(db=db, user=user)

@app.get(
    "/users/",
    response_model=List[schemas.User],
    tags=["Users"],
    summary="Listar usuarios"
)
def read_users(
    skip: int = Query(0, ge=0, description="Número de usuarios a saltar"),
    limit: int = Query(100, ge=1, le=100, description="Límite de usuarios a retornar"),
    is_active: Optional[bool] = Query(None, description="Filtrar por usuarios activos/inactivos"),
    db: Session = Depends(get_db)
):
    """
    Obtiene una lista de usuarios con paginación y filtrado opcional.

    - **skip**: Número de usuarios a saltar (para paginación)
    - **limit**: Número máximo de usuarios a retornar (máximo 100)
    - **is_active**: Filtrar solo usuarios activos (true) o inactivos (false)
    """
    users = crud.get_users(db, skip=skip, limit=limit, is_active=is_active)
    return users

@app.get(
    "/users/{user_id}",
    response_model=schemas.User,
    tags=["Users"],
    summary="Obtener un usuario por ID"
)
def read_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene un usuario específico por su ID.

    Args:
        user_id: ID del usuario

    Returns:
        Usuario con todos sus items

    Raises:
        HTTPException 404: Si el usuario no existe
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    return db_user

@app.patch(
    "/users/{user_id}",
    response_model=schemas.User,
    tags=["Users"],
    summary="Actualizar un usuario"
)
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza parcialmente un usuario.

    Solo necesitas enviar los campos que quieres actualizar.

    Raises:
        HTTPException 404: Si el usuario no existe
        HTTPException 400: Si el email/username ya están en uso por otro usuario
    """
    # Verificamos que el usuario existe
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )

    # Si se actualiza el email, verificamos que no esté en uso
    if user_update.email:
        existing_user = crud.get_user_by_email(db, email=user_update.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está en uso por otro usuario"
            )

    # Si se actualiza el username, verificamos que no esté en uso
    if user_update.username:
        existing_user = crud.get_user_by_username(db, username=user_update.username)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El username ya está en uso por otro usuario"
            )

    # Actualizamos el usuario
    updated_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    return updated_user

@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Users"],
    summary="Eliminar un usuario"
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina un usuario y todos sus items asociados.

    Raises:
        HTTPException 404: Si el usuario no existe
    """
    success = crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    # Con status 204, no retornamos contenido
    return

# ============================================
# ENDPOINTS DE ITEMS
# ============================================

@app.post(
    "/users/{user_id}/items/",
    response_model=schemas.Item,
    status_code=status.HTTP_201_CREATED,
    tags=["Items"],
    summary="Crear un item para un usuario"
)
def create_item_for_user(
    user_id: int,
    item: schemas.ItemCreate,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo item asociado a un usuario.

    Args:
        user_id: ID del usuario propietario del item
        item: Datos del item a crear

    Raises:
        HTTPException 404: Si el usuario no existe

    Ejemplo de request body:
    ```json
    {
        "name": "Laptop Gaming",
        "description": "Laptop potente para gaming",
        "price": 1299.99,
        "tax": 21.0,
        "tag_names": ["electronics", "gaming", "computers"]
    }
    ```
    """
    # Verificamos que el usuario existe
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )

    # Creamos el item
    return crud.create_item(db=db, item=item, owner_id=user_id)

@app.get(
    "/items/",
    response_model=List[schemas.Item],
    tags=["Items"],
    summary="Listar items"
)
def read_items(
    skip: int = Query(0, ge=0, description="Número de items a saltar"),
    limit: int = Query(100, ge=1, le=100, description="Límite de items a retornar"),
    owner_id: Optional[int] = Query(None, description="Filtrar por propietario"),
    tag: Optional[str] = Query(None, description="Filtrar por tag"),
    db: Session = Depends(get_db)
):
    """
    Obtiene una lista de items con paginación y filtros opcionales.

    - **skip**: Paginación - items a saltar
    - **limit**: Paginación - límite de items (máximo 100)
    - **owner_id**: Filtrar items de un usuario específico
    - **tag**: Filtrar items que tengan un tag específico
    """
    items = crud.get_items(
        db,
        skip=skip,
        limit=limit,
        owner_id=owner_id,
        tag_name=tag
    )
    return items

@app.get(
    "/items/{item_id}",
    response_model=schemas.Item,
    tags=["Items"],
    summary="Obtener un item por ID"
)
def read_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene un item específico por su ID.

    Raises:
        HTTPException 404: Si el item no existe
    """
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item con ID {item_id} no encontrado"
        )
    return db_item

@app.patch(
    "/items/{item_id}",
    response_model=schemas.Item,
    tags=["Items"],
    summary="Actualizar un item"
)
def update_item(
    item_id: int,
    item_update: schemas.ItemUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza parcialmente un item.

    Solo necesitas enviar los campos que quieres actualizar.

    Raises:
        HTTPException 404: Si el item no existe
    """
    updated_item = crud.update_item(db, item_id=item_id, item_update=item_update)
    if not updated_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item con ID {item_id} no encontrado"
        )
    return updated_item

@app.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Items"],
    summary="Eliminar un item"
)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina un item.

    Raises:
        HTTPException 404: Si el item no existe
    """
    success = crud.delete_item(db, item_id=item_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item con ID {item_id} no encontrado"
        )
    return

# ============================================
# ENDPOINTS DE TAGS
# ============================================

@app.get(
    "/tags/",
    response_model=List[schemas.Tag],
    tags=["Tags"],
    summary="Listar tags"
)
def read_tags(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Obtiene una lista de todos los tags disponibles.

    Los tags se crean automáticamente cuando se crean items con nuevos tags.
    """
    tags = crud.get_tags(db, skip=skip, limit=limit)
    return tags

# ============================================
# PUNTO DE ENTRADA PARA EJECUCIÓN DIRECTA
# ============================================

if __name__ == "__main__":
    # Si ejecutamos este archivo directamente con python main_completo.py
    # se iniciará el servidor uvicorn
    uvicorn.run(
        "main_completo:app",
        host="127.0.0.1",
        port=8000,
        reload=True  # Auto-reload cuando cambia el código
    )
