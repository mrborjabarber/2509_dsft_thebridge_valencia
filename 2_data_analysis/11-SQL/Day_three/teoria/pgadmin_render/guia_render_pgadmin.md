# 🗄️ Guía paso a paso: Crear una base de datos en Render y conectarla con pgAdmin4

## 🧩 Parte 1: Crear una cuenta y una base de datos en Render

### 1️⃣ Registrarte o iniciar sesión en Render
1. Ve a 👉 [https://render.com](https://render.com)  
2. Haz clic en **Sign Up** (si no tienes cuenta) o **Log In** (si ya tienes una).  
3. Puedes registrarte con **GitHub**, **Google**, o con tu **correo electrónico**.

---

### 2️⃣ Crear una nueva base de datos PostgreSQL
1. Una vez dentro del panel de Render, haz clic en el botón **New +** (arriba a la derecha).  
2. Selecciona **PostgreSQL**.  
3. Se abrirá un formulario con las siguientes opciones:  

   - **Name**: Escribe un nombre descriptivo (por ejemplo: `mi_basedatos`).  
   - **Database**: Puedes dejarlo igual al nombre o cambiarlo.  
   - **User**: Render crea un usuario automáticamente (puedes cambiarlo).  
   - **Region**: Elige la región más cercana a ti.  
   - **Instance Type**: Elige el tipo gratuito si estás empezando (`Free Tier`).  

4. Haz clic en **Create Database**.  

> ⚙️ Render tardará unos minutos en crear el servicio.  

---

### 3️⃣ Obtener las credenciales de conexión


1. Una vez creada la base de datos, haz clic sobre su nombre.  
2. En la pestaña **Info**, busca la sección **Connections**.  
3. Allí verás una cadena similar a:  

   ```
   postgres://<usuario>:<contraseña>@<host>:5432/<nombre_base_datos>
   ```

   Ejemplo:  
   ```
   postgres://admin_user:abcd1234@dpg-xyz1234abcd.us-east-1.render.com:5432/mi_basedatos
   ```

   Guarda estos datos:  
   - **Host:** `dpg-xyz1234abcd.us-east-1.render.com`  
   - **Port:** `5432`  
   - **Database name:** `mi_basedatos`  
   - **Username:** `admin_user`  
   - **Password:** `abcd1234`

opcion 2 copia el campo external database URL y ve a chatgpt e introduce este promt desglosa para conectar en pgadmin4 y pegas tu link  


---

## 🧭 Parte 2: Conectar Render con pgAdmin4

### 4️⃣ Configurar la conexión en pgAdmin4
1. Abre **pgAdmin4** en tu computadora.  
2. En el panel izquierdo, haz clic derecho en **Servers → Create → Server...**  
3. En la ventana que aparece:
   - **General → Name:** pon un nombre para la conexión (por ejemplo: `RenderDB`).  
   - Ve a la pestaña **Connection** y completa los campos:  
     - **Host name/address:** el host de Render (ej: `dpg-xyz1234abcd.us-east-1.render.com`)  
     - **Port:** `5432`  
     - **Maintenance database:** `mi_basedatos`  
     - **Username:** `admin_user`  
     - **Password:** `abcd1234`  

4. (Opcional) Marca la casilla **Save password** para no tener que escribirla cada vez.  
5. Haz clic en **Save**.  

---

### 5️⃣ Probar la conexión
- Si todo está correcto, verás tu servidor aparecer en el panel izquierdo de pgAdmin4.  
- Haz clic en él: debería conectarse y mostrar las carpetas de esquemas y tablas.  

> 🔍 Si falla:
> - Revisa que el **host** y la **contraseña** estén bien copiados.  
> - Asegúrate de que Render no esté suspendido (las bases de datos gratis pueden “dormir” tras inactividad).  
> - Render usa SSL, así que si te pide un modo de conexión, selecciona **Require SSL**.

---

## ⚙️ Parte 3: Crear tablas y cargar datos

### 6️⃣ Crear una tabla desde pgAdmin4
1. Abre tu base de datos → **Schemas → public → Tables**.  
2. Clic derecho → **Create → Table**.  
3. Escribe:
   - **Table name:** `clientes`  
   - En la pestaña **Columns**, agrega columnas como:
     - `id` (tipo `serial`, clave primaria)  
     - `nombre` (tipo `varchar(50)`)  
     - `email` (tipo `varchar(100)`)  
4. Haz clic en **Save**.  

También puedes usar SQL directamente:

```sql
CREATE TABLE clientes (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(50),
  email VARCHAR(100)
);
```

---

### 7️⃣ Insertar datos de prueba

Abre la pestaña de **Query Tool** (ícono del rayo) y escribe:

```sql
INSERT INTO clientes (nombre, email)
VALUES ('Juan Pérez', 'juanperez@gmail.com'),
       ('María López', 'maria@example.com');
```

Luego ejecuta la consulta (botón ▶️).  

Para ver los resultados:

```sql
SELECT * FROM clientes;
```

---

## 🎯 Resultado final

✅ Ya tienes:
- Una base de datos PostgreSQL **activa en Render**.  
- Conexión establecida y funcional en **pgAdmin4**.  
- Tablas creadas y datos insertados correctamente.  

---

### 📄 Créditos
Guía elaborada por Borja Barber Lead Instructor DS
.  
Versión: Octubre 2025.
