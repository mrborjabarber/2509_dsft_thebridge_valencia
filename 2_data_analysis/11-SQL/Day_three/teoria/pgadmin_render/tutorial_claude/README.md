# Tutorial PostgreSQL con Render, pgAdmin 4 y Python

## Descripción

Tutorial completo para crear y gestionar una base de datos PostgreSQL utilizando Render (hosting gratuito), pgAdmin 4 (administración visual) y Python (operaciones programáticas).

El proyecto implementa un sistema de gestión para una **Escuela de Informática** con tres tablas relacionadas:
- **estudiantes**: Información de los estudiantes
- **cursos**: Catálogo de cursos disponibles
- **inscripciones**: Relación entre estudiantes y cursos (incluye calificaciones)

## Requisitos Previos

### Software
- Python 3.8 o superior
- [pgAdmin 4](https://www.pgadmin.org/download/)
- Cuenta gratuita en [Render](https://render.com/)
- Jupyter Notebook (incluido en Anaconda o instalable con pip)

### Librerías Python
```bash
pip install psycopg2-binary python-dotenv pandas jupyter
```

## Instalación

1. **Clona o descarga este repositorio**

2. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

   O instala manualmente:
   ```bash
   pip install psycopg2-binary python-dotenv pandas jupyter
   ```

3. **Crea tu archivo .env**
   ```bash
   cp .env.example .env
   ```

   Luego edita `.env` con tus credenciales de Render.

4. **Inicia Jupyter Notebook**
   ```bash
   jupyter notebook
   ```

   Se abrirá tu navegador. Abre el archivo `tutorial_postgresql_render.ipynb`

## Contenido del Tutorial

### Paso 1: Crear Base de Datos en Render
- Registro en Render
- Creación de base de datos PostgreSQL
- Obtención de credenciales

### Paso 2: Configurar archivo .env
- Configuración de variables de entorno
- Buenas prácticas de seguridad

### Paso 3: Conectar con pgAdmin 4
- Configuración de conexión SSL
- Exploración de la base de datos
- Uso del Query Tool

### Paso 4: Conectar desde Python
- Uso de psycopg2
- Funciones de conexión
- Manejo de errores

### Paso 5: Crear Tablas
- Diseño del esquema
- Primary Keys y Foreign Keys
- Constraints y validaciones

### Paso 6: Insertar Datos
- Operaciones CREATE
- Inserción de datos relacionados
- Prevención de SQL injection

### Paso 7: Consultas SQL
- SELECT básico
- JOINs (INNER, LEFT)
- Agregaciones (COUNT, AVG, SUM)
- Consultas avanzadas

### Operaciones CRUD Adicionales
- UPDATE (actualizar registros)
- DELETE (eliminar registros)

## Estructura de la Base de Datos

```
ESTUDIANTES
├─ id (PRIMARY KEY)
├─ nombre
├─ apellido
├─ email (UNIQUE)
├─ fecha_inscripcion
└─ telefono

CURSOS
├─ id (PRIMARY KEY)
├─ nombre
├─ descripcion
├─ profesor
├─ duracion_horas
└─ precio

INSCRIPCIONES
├─ id (PRIMARY KEY)
├─ estudiante_id (FOREIGN KEY → estudiantes.id)
├─ curso_id (FOREIGN KEY → cursos.id)
├─ fecha_inscripcion
├─ calificacion
└─ estado
```

## Archivos del Proyecto

```
.
├── tutorial_postgresql_render.ipynb  # Tutorial principal
├── .env.example                      # Plantilla de configuración
├── .gitignore                        # Archivos a ignorar en git
└── README.md                         # Este archivo
```

## Seguridad

- **NUNCA** subas el archivo `.env` a repositorios públicos
- El archivo `.gitignore` ya está configurado para ignorar `.env`
- Usa contraseñas fuertes para tu base de datos
- Render requiere conexiones SSL (ya configurado en el tutorial)

## Ejercicios Propuestos

1. Añadir una tabla `profesores` y relacionarla con `cursos`
2. Crear vistas SQL para consultas frecuentes
3. Implementar búsqueda de cursos por palabra clave
4. Crear reportes con estadísticas generales
5. Exportar resultados a CSV
6. Añadir validaciones de datos
7. Implementar sistema de auditoría

## Recursos Adicionales

- [Documentación PostgreSQL](https://www.postgresql.org/docs/)
- [Documentación psycopg2](https://www.psycopg.org/docs/)
- [Render Database Docs](https://render.com/docs/databases)
- [pgAdmin Documentation](https://www.pgadmin.org/docs/)

## Solución de Problemas

### No puedo conectar a la base de datos
- Verifica que el modo SSL esté en "Require"
- Comprueba que las credenciales sean correctas
- Asegúrate de tener conexión a internet
- Verifica que tu firewall no bloquee el puerto 5432

### Error al importar psycopg2
```bash
# Si tienes problemas con psycopg2, usa la versión binary:
pip uninstall psycopg2
pip install psycopg2-binary
```

### El archivo .env no se carga
- Verifica que el archivo se llame exactamente `.env` (sin extensión adicional)
- Asegúrate de que esté en la misma carpeta que el notebook
- No debe haber espacios alrededor del `=` en las variables

## Contribuciones

Si encuentras errores o tienes sugerencias de mejora, por favor:
1. Abre un Issue
2. Envía un Pull Request

## Licencia

Este tutorial es de código abierto y está disponible para uso educativo.

---

Creado con fines educativos para aprender PostgreSQL, Python y gestión de bases de datos.
