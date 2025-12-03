# ¿Qué es una API REST?

Una **API REST** (Representational State Transfer) es un estilo de
arquitectura para diseñar servicios web que permiten la comunicación
entre sistemas de manera sencilla y eficiente. Es ampliamente utilizada
en ciencia de datos para obtener, enviar o modificar datos desde
aplicaciones externas.

## Principios clave

1.  **Cliente-servidor**\
    La aplicación cliente y el servidor están separados. El cliente
    solicita recursos y el servidor los provee.

2.  **Sin estado (Stateless)**\
    Cada petición del cliente debe contener toda la información
    necesaria. El servidor no guarda el estado de la sesión.

3.  **Uso de recursos**\
    Los recursos se representan mediante URLs y se manipulan usando
    métodos HTTP.

4.  **Operaciones HTTP estándar**

    -   **GET**: Obtener datos.\
    -   **POST**: Crear nuevos datos.\
    -   **PUT**: Actualizar datos existentes.\
    -   **DELETE**: Eliminar datos.

5.  **Formato de intercambio**\
    Normalmente se usa JSON por su simplicidad y compatibilidad.

## Por qué es útil en Data Science

-   Facilita la integración con bases de datos externas.
-   Permite automatizar la obtención de datos.
-   Se usa para desplegar modelos de machine learning como servicios.
-   Permite crear pipelines que consumen datos en tiempo real.

## Ejemplo conceptual

Si un servidor tiene información sobre usuarios, podría exponer estos
endpoints:

-   `GET /usuarios` → devuelve la lista de usuarios\
-   `POST /usuarios` → agrega un nuevo usuario\
-   `GET /usuarios/10` → devuelve información del usuario con ID 10\
-   `PUT /usuarios/10` → actualiza información del usuario\
-   `DELETE /usuarios/10` → elimina al usuario

Este enfoque estandarizado facilita que cualquier aplicación pueda
comunicarse con el servidor sin importar el lenguaje de programación.
