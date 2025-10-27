# ¿Puedo usar dos claves primarias iguales en dos tablas?

## 🔹 1. Sí puedes tener la misma clave primaria en dos tablas diferentes

Cada tabla es independiente, así que puedes tener:

``` sql
CREATE TABLE usuarios (
    id INT PRIMARY KEY,
    nombre VARCHAR(50)
);

CREATE TABLE pedidos (
    id INT PRIMARY KEY,
    fecha DATE
);
```

👉 Aquí **ambas tablas tienen una columna `id` como clave primaria**, y
**pueden tener los mismos valores** (por ejemplo, `id = 1` en ambas).\
No hay conflicto, porque cada tabla gestiona sus claves de forma
separada.

------------------------------------------------------------------------

## 🔹 2. Pero no puedes tener dos claves primarias iguales en la misma tabla

Esto **sí está prohibido**.\
Una clave primaria debe ser **única y no nula** dentro de una tabla:

``` sql
CREATE TABLE productos (
    id INT PRIMARY KEY,
    nombre VARCHAR(50)
);
```

Aquí no podrías tener dos filas con `id = 1`.

------------------------------------------------------------------------

## 🔹 3. Si quieres relacionar las tablas (clave foránea)

Puedes usar la **misma columna y valor como relación**, pero no es la
misma clave primaria:

``` sql
CREATE TABLE usuarios (
    id INT PRIMARY KEY,
    nombre VARCHAR(50)
);

CREATE TABLE pedidos (
    id INT PRIMARY KEY,
    usuario_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
```

👉 En este caso: - `usuarios.id` es **clave primaria** en `usuarios`. -
`pedidos.usuario_id` es **clave foránea**, que puede repetir el valor de
`usuarios.id`.

------------------------------------------------------------------------

## 🔹 Resumen

  -----------------------------------------------------------------------
  Caso          ¿Se puede?                   Explicación
  ------------- ---------------------------- ----------------------------
  Misma clave   ✅                           Cada tabla es independiente
  primaria en 2                              
  tablas                                     
  distintas                                  

  Dos filas con ❌                           Violación de unicidad
  misma clave                                
  primaria en                                
  una tabla                                  

  Clave foránea ✅                           Correcto, es una relación
  que repite                                 
  valor de otra                              
  clave                                      
  primaria                                   
  -----------------------------------------------------------------------
