# EJERCICIO PRÁCTICO SQL - PARTE 1
## Base de datos: SQLite Tutorial (Chinook)

Este documento contiene 15 ejercicios prácticos de SQL basados en la base de datos de música Chinook.

---

## Configuración Inicial

```python
# Importar librerías necesarias
import sqlite3
import pandas as pd

# Conectar a la base de datos (ajusta la ruta según tu archivo)
conn = sqlite3.connect('chinook.db')
cursor = conn.cursor()
```

---

## Ejercicio 1: Obtén los clientes de Brasil

**Explicación:**
Vamos a consultar la tabla `customers` para obtener todos los campos de los clientes. Usaremos una cláusula `WHERE` para filtrar únicamente los registros donde el país sea 'Brazil'. Esta es una consulta simple que no requiere joins, solo un filtro básico.

```sql
SELECT * 
FROM customers 
WHERE Country = 'Brazil';
```

```python
query1 = """
SELECT * 
FROM customers 
WHERE Country = 'Brazil';
"""

df1 = pd.read_sql_query(query1, conn)
print(f"Total de clientes de Brasil: {len(df1)}")
df1
```

---

## Ejercicio 2: Obtén los empleados que son agentes de ventas

**Explicación:**
Consultaremos la tabla `employees` para obtener todos los campos de los empleados. Filtraremos con `WHERE` para seleccionar solo aquellos cuyo título (campo `Title`) sea 'Sales Support Agent'. No necesitamos joins aquí, solo acceder a una tabla con un filtro.

```sql
SELECT * 
FROM employees 
WHERE Title = 'Sales Support Agent';
```

```python
query2 = """
SELECT * 
FROM employees 
WHERE Title = 'Sales Support Agent';
"""

df2 = pd.read_sql_query(query2, conn)
print(f"Total de agentes de ventas: {len(df2)}")
df2
```

---

## Ejercicio 3: Obtén las canciones de 'AC/DC'

**Explicación:**
Para obtener las canciones de un artista específico, necesitamos hacer **dos INNER JOINs** porque las tablas están relacionadas así:
1. Primero unimos `tracks` con `albums` (usando `AlbumId`) para saber a qué álbum pertenece cada canción
2. Luego unimos `albums` con `artists` (usando `ArtistId`) para saber qué artista creó cada álbum
3. Finalmente filtramos con `WHERE` para obtener solo las canciones donde el nombre del artista sea 'AC/DC'

```sql
SELECT tracks.*
FROM tracks
INNER JOIN albums ON tracks.AlbumId = albums.AlbumId
INNER JOIN artists ON albums.ArtistId = artists.ArtistId
WHERE artists.Name = 'AC/DC';
```

```python
query3 = """
SELECT tracks.*
FROM tracks
INNER JOIN albums ON tracks.AlbumId = albums.AlbumId
INNER JOIN artists ON albums.ArtistId = artists.ArtistId
WHERE artists.Name = 'AC/DC';
"""

df3 = pd.read_sql_query(query3, conn)
print(f"Total de canciones de AC/DC: {len(df3)}")
df3.head(10)
```

---

## Ejercicio 4: Obtén los campos de los clientes que no sean de USA: Nombre completo, ID, País

**Explicación:**
Consultamos la tabla `customers` y seleccionamos campos específicos:
- `CustomerId`: el ID del cliente
- Concatenamos `FirstName` y `LastName` usando el operador `||` para crear el nombre completo
- `Country`: el país del cliente
Filtramos con `WHERE Country != 'USA'` para excluir los clientes de Estados Unidos.

```sql
SELECT CustomerId, 
       FirstName || ' ' || LastName AS NombreCompleto, 
       Country
FROM customers
WHERE Country != 'USA';
```

```python
query4 = """
SELECT CustomerId, 
       FirstName || ' ' || LastName AS NombreCompleto, 
       Country
FROM customers
WHERE Country != 'USA';
"""

df4 = pd.read_sql_query(query4, conn)
print(f"Total de clientes fuera de USA: {len(df4)}")
df4.head(10)
```

---

## Ejercicio 5: Obtén los empleados que son agentes de ventas: Nombre completo, Dirección (Ciudad, Estado, País) y email

**Explicación:**
Consultamos la tabla `employees` y seleccionamos campos específicos:
- Concatenamos `FirstName` y `LastName` para el nombre completo
- Extraemos los campos de dirección: `City`, `State`, `Country`
- Incluimos el `Email`
Filtramos con `WHERE` para obtener solo los empleados que sean 'Sales Support Agent'.

```sql
SELECT FirstName || ' ' || LastName AS NombreCompleto,
       City,
       State,
       Country,
       Email
FROM employees
WHERE Title = 'Sales Support Agent';
```

```python
query5 = """
SELECT FirstName || ' ' || LastName AS NombreCompleto,
       City,
       State,
       Country,
       Email
FROM employees
WHERE Title = 'Sales Support Agent';
"""

df5 = pd.read_sql_query(query5, conn)
df5
```

---

## Ejercicio 6: Obtén una lista con los países no repetidos a los que se han emitido facturas

**Explicación:**
Consultamos la tabla `invoices` para obtener los países de facturación. Usamos `DISTINCT` para eliminar duplicados y obtener solo una lista de países únicos. Ordenamos alfabéticamente con `ORDER BY` para facilitar la lectura del resultado.

```sql
SELECT DISTINCT BillingCountry
FROM invoices
ORDER BY BillingCountry;
```

```python
query6 = """
SELECT DISTINCT BillingCountry
FROM invoices
ORDER BY BillingCountry;
"""

df6 = pd.read_sql_query(query6, conn)
print(f"Total de países con facturas: {len(df6)}")
df6
```

---

## Ejercicio 7: Obtén una lista con los estados de USA no repetidos de donde son los clientes y cuántos clientes en cada uno

**Explicación:**
Consultamos la tabla `customers` y la agrupamos por estado (`State`) para contar cuántos clientes hay en cada uno. Usamos:
- `WHERE` para filtrar solo clientes de USA y que tengan un estado definido (no NULL)
- `GROUP BY State` para agrupar los registros por estado
- `COUNT(*)` para contar cuántos clientes hay en cada grupo
- `ORDER BY` para ordenar alfabéticamente por estado

```sql
SELECT State, COUNT(*) AS NumeroClientes
FROM customers
WHERE Country = 'USA' AND State IS NOT NULL
GROUP BY State
ORDER BY State;
```

```python
query7 = """
SELECT State, COUNT(*) AS NumeroClientes
FROM customers
WHERE Country = 'USA' AND State IS NOT NULL
GROUP BY State
ORDER BY State;
"""

df7 = pd.read_sql_query(query7, conn)
df7
```

---

## Ejercicio 8: Cuántos artículos tiene la factura 37

**Explicación:**
Consultamos la tabla `invoice_items` que contiene los artículos individuales de cada factura. Usamos `COUNT(*)` para contar cuántos registros (artículos) existen y filtramos con `WHERE` para obtener solo los de la factura con ID 37. Esta es una consulta de agregación simple sin joins.

```sql
SELECT COUNT(*) AS NumeroArticulos
FROM invoice_items
WHERE InvoiceId = 37;
```

```python
query8 = """
SELECT COUNT(*) AS NumeroArticulos
FROM invoice_items
WHERE InvoiceId = 37;
"""

df8 = pd.read_sql_query(query8, conn)
df8
```

---

## Ejercicio 9: Cuántas canciones tiene 'AC/DC'

**Explicación:**
Similar al ejercicio 3, pero ahora solo queremos contar las canciones en lugar de listar todos sus detalles. Hacemos **dos INNER JOINs**:
1. Unimos `tracks` con `albums` mediante `AlbumId`
2. Unimos `albums` con `artists` mediante `ArtistId`
3. Filtramos por el nombre del artista 'AC/DC'
4. Usamos `COUNT(*)` para contar el número total de canciones que coinciden

```sql
SELECT COUNT(*) AS NumeroCanciones
FROM tracks
INNER JOIN albums ON tracks.AlbumId = albums.AlbumId
INNER JOIN artists ON albums.ArtistId = artists.ArtistId
WHERE artists.Name = 'AC/DC';
```

```python
query9 = """
SELECT COUNT(*) AS NumeroCanciones
FROM tracks
INNER JOIN albums ON tracks.AlbumId = albums.AlbumId
INNER JOIN artists ON albums.ArtistId = artists.ArtistId
WHERE artists.Name = 'AC/DC';
"""

df9 = pd.read_sql_query(query9, conn)
df9
```

---

## Ejercicio 10: Cuántos artículos tiene cada factura

**Explicación:**
Consultamos la tabla `invoice_items` y la agrupamos por factura para contar cuántos artículos tiene cada una. Usamos:
- `GROUP BY InvoiceId` para agrupar todos los artículos de la misma factura
- `COUNT(*)` para contar cuántos artículos hay en cada grupo
- `ORDER BY InvoiceId` para ordenar las facturas secuencialmente

Esta query nos da un resumen de todas las facturas con su respectivo número de artículos.

```sql
SELECT InvoiceId, COUNT(*) AS NumeroArticulos
FROM invoice_items
GROUP BY InvoiceId
ORDER BY InvoiceId;
```

```python
query10 = """
SELECT InvoiceId, COUNT(*) AS NumeroArticulos
FROM invoice_items
GROUP BY InvoiceId
ORDER BY InvoiceId;
"""

df10 = pd.read_sql_query(query10, conn)
print(f"Total de facturas: {len(df10)}")
df10.head(20)
```

---

## Ejercicio 11: Cuántas facturas hay de cada país

**Explicación:**
Consultamos la tabla `invoices` y agrupamos por país de facturación para contar cuántas facturas se emitieron en cada país. Usamos:
- `GROUP BY BillingCountry` para agrupar todas las facturas del mismo país
- `COUNT(*)` para contar cuántas facturas hay en cada grupo
- `ORDER BY NumeroFacturas DESC` para ordenar de mayor a menor número de facturas, mostrando primero los países con más facturas

```sql
SELECT BillingCountry, COUNT(*) AS NumeroFacturas
FROM invoices
GROUP BY BillingCountry
ORDER BY NumeroFacturas DESC;
```

```python
query11 = """
SELECT BillingCountry, COUNT(*) AS NumeroFacturas
FROM invoices
GROUP BY BillingCountry
ORDER BY NumeroFacturas DESC;
"""

df11 = pd.read_sql_query(query11, conn)
df11
```

---

## Ejercicio 12: Cuántas facturas ha habido en 2009 y 2011

**Explicación:**
Consultamos la tabla `invoices` para contar facturas de años específicos. Usamos:
- `strftime('%Y', InvoiceDate)` para extraer solo el año de la fecha de la factura
- `IN ('2009', '2011')` para filtrar solo las facturas de 2009 O 2011 (no incluye 2010)
- `COUNT(*)` para contar el total de facturas que cumplen la condición

Esta query suma las facturas de ambos años, NO las cuenta por separado.

```sql
SELECT COUNT(*) AS NumeroFacturas
FROM invoices
WHERE strftime('%Y', InvoiceDate) IN ('2009', '2011');
```

```python
query12 = """
SELECT COUNT(*) AS NumeroFacturas
FROM invoices
WHERE strftime('%Y', InvoiceDate) IN ('2009', '2011');
"""

df12 = pd.read_sql_query(query12, conn)
df12
```

---

## Ejercicio 13: Cuántas facturas ha habido entre 2009 y 2011

**Explicación:**
Similar al ejercicio anterior, pero ahora usamos `BETWEEN` para incluir el rango completo:
- `strftime('%Y', InvoiceDate)` extrae el año de la fecha
- `BETWEEN '2009' AND '2011'` incluye 2009, 2010 Y 2011 (todos los años del rango)
- `COUNT(*)` cuenta todas las facturas en ese periodo

La diferencia con el ejercicio 12 es que este incluye también las facturas de 2010.

```sql
SELECT COUNT(*) AS NumeroFacturas
FROM invoices
WHERE strftime('%Y', InvoiceDate) BETWEEN '2009' AND '2011';
```

```python
query13 = """
SELECT COUNT(*) AS NumeroFacturas
FROM invoices
WHERE strftime('%Y', InvoiceDate) BETWEEN '2009' AND '2011';
"""

df13 = pd.read_sql_query(query13, conn)
df13
```

---

## Ejercicio 14: Cuántos clientes hay de España y de Brasil

**Explicación:**
Consultamos la tabla `customers` para contar clientes de países específicos. Usamos:
- `WHERE Country IN ('Spain', 'Brazil')` para filtrar solo clientes de estos dos países
- `GROUP BY Country` para agrupar los resultados por país
- `COUNT(*)` para contar cuántos clientes hay en cada grupo

Esta query nos devuelve un registro por cada país con su respectivo conteo de clientes.

```sql
SELECT Country, COUNT(*) AS NumeroClientes
FROM customers
WHERE Country IN ('Spain', 'Brazil')
GROUP BY Country;
```

```python
query14 = """
SELECT Country, COUNT(*) AS NumeroClientes
FROM customers
WHERE Country IN ('Spain', 'Brazil')
GROUP BY Country;
"""

df14 = pd.read_sql_query(query14, conn)
df14
```

---

## Ejercicio 15: Obtén las canciones que su título empieza por 'You'

**Explicación:**
Consultamos la tabla `tracks` para buscar canciones por un patrón en su nombre. Usamos:
- `LIKE 'You%'` donde:
  - `LIKE` permite búsquedas con patrones
  - `'You%'` significa: empieza con "You" seguido de cualquier cosa
  - El símbolo `%` representa cero o más caracteres

Esta query encuentra todas las canciones cuyos títulos comienzan exactamente con "You".

```sql
SELECT *
FROM tracks
WHERE Name LIKE 'You%';
```

```python
query15 = """
SELECT *
FROM tracks
WHERE Name LIKE 'You%';
"""

df15 = pd.read_sql_query(query15, conn)
print(f"Total de canciones que empiezan por 'You': {len(df15)}")
df15.head(20)
```

---

## Cerrar la conexión

```python
# Cerrar la conexión a la base de datos
conn.close()
print("Conexión cerrada exitosamente")
```

---

## Notas Importantes

**Antes de ejecutar este código:**

1. Asegúrate de tener instalados los paquetes necesarios:
   ```bash
   pip install pandas sqlite3
   ```

2. Descarga la base de datos Chinook desde: https://www.sqlitetutorial.net/sqlite-sample-database/

3. Coloca el archivo `chinook.db` en el mismo directorio que tu script Python.

**Características del código:**
- Usa SQLite con la base de datos Chinook
- Todas las queries están optimizadas para SQLite
- Los resultados se muestran usando pandas DataFrames para mejor visualización
- Cada ejercicio incluye tanto la query SQL pura como el código Python para ejecutarla

**Conceptos SQL cubiertos:**
- ✅ SELECT básico
- ✅ WHERE con condiciones
- ✅ INNER JOIN
- ✅ Concatenación de strings (`||`)
- ✅ DISTINCT
- ✅ GROUP BY
- ✅ COUNT y agregaciones
- ✅ ORDER BY
- ✅ LIKE para búsqueda de patrones
- ✅ Funciones de fecha (strftime)
- ✅ BETWEEN y IN
