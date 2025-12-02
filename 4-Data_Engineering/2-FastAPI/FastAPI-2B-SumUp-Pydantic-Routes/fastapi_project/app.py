# Importamos los routers desde el proyecto.
# Cada router generalmente contiene un conjunto de rutas (endpoints)
# organizadas por funcionalidades, por ejemplo: posts y users.
from fastapi_project.routers.posts import router as posts_router
from fastapi_project.routers.users import router as users_router

# Importamos FastAPI para crear la aplicación principal de la API.
from fastapi import FastAPI

# Creamos una instancia de FastAPI, que será la aplicación principal.
app = FastAPI()

# Incluimos el router de posts dentro de la aplicación.
# prefix="/posts" indica que todas las rutas del router se accederán
# empezando por /posts (por ejemplo: GET /posts/, POST /posts/create)
# tags=["posts"] sirve para agrupar estas rutas en la documentación (Swagger).
app.include_router(posts_router, prefix="/posts", tags=["posts"])

# Hacemos lo mismo con el router de usuarios.
# Todas las rutas relacionadas con usuarios comenzarán con /users.
app.include_router(users_router, prefix="/users", tags=["users"])
