# EJERCICIO PRÁCTICO SQL - PARTE 2
## Ejercicios con JOINS y Agregaciones Avanzadas

Este documento contiene 9 ejercicios avanzados de SQL con múltiples tablas relacionadas.

---

## Configuración Inicial

```python
# Importar librerías necesarias
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Conectar a la base de datos (ajusta la ruta según tu archivo)
conn = sqlite3.connect('chinook.db')
cursor = conn.cursor()

print("Conexión establecida exitosamente")
```

---

## Ejercicio 1: Facturas de Clientes de Brasil
### Nombre del cliente, Id de factura, fecha de la factura y el país de la factura

**Explicación:**
Vamos a unir dos tablas para obtener información de facturas junto con datos del cliente:
1. Partimos de la tabla `invoices` que contiene las facturas
2. Hacemos un **INNER JOIN** con `customers` usando el campo `CustomerId` que está en ambas tablas
3. Esto nos permite acceder tanto a los datos de la factura como a los datos del cliente
4. Filtramos con `WHERE customers.Country = 'Brazil'` para obtener solo facturas de clientes brasileños
5. Concatenamos `FirstName` y `LastName` del cliente para formar el nombre completo
6. Ordenamos por fecha de factura para ver la evolución cronológica

```sql
SELECT 
    customers.FirstName || ' ' || customers.LastName AS NombreCliente,
    invoices.InvoiceId,
    invoices.InvoiceDate,
    invoices.BillingCountry AS PaisFactura
FROM invoices
INNER JOIN customers ON invoices.CustomerId = customers.CustomerId
WHERE customers.Country = 'Brazil'
ORDER BY invoices.InvoiceDate;
```

```python
query1 = """
SELECT 
    customers.FirstName || ' ' || customers.LastName AS NombreCliente,
    invoices.InvoiceId,
    invoices.InvoiceDate,
    invoices.BillingCountry AS PaisFactura
FROM invoices
INNER JOIN customers ON invoices.CustomerId = customers.CustomerId
WHERE customers.Country = 'Brazil'
ORDER BY invoices.InvoiceDate;
"""

df1 = pd.read_sql_query(query1, conn)
print(f"Total de facturas de clientes de Brasil: {len(df1)}")
df1
```

---

## Ejercicio 2: Obtén cada factura asociada a cada agente de ventas con su nombre completo

**Explicación:**
Para conectar facturas con agentes de ventas necesitamos hacer **dos INNER JOINs** porque están relacionados de forma indirecta:
1. Empezamos con la tabla `invoices` (facturas)
2. Primer JOIN: unimos `invoices` con `customers` mediante `CustomerId` - esto nos da acceso al cliente de cada factura
3. Segundo JOIN: unimos `customers` con `employees` mediante `SupportRepId` (que es el ID del empleado asignado al cliente)
4. Así obtenemos el agente de ventas que gestiona al cliente que hizo la compra
5. Concatenamos el nombre del empleado y ordenamos por apellido del agente y fecha

**Relación:** Factura → Cliente → Empleado (agente de ventas)

```sql
SELECT 
    invoices.InvoiceId,
    invoices.InvoiceDate,
    invoices.Total,
    employees.FirstName || ' ' || employees.LastName AS NombreAgente,
    employees.Title
FROM invoices
INNER JOIN customers ON invoices.CustomerId = customers.CustomerId
INNER JOIN employees ON customers.SupportRepId = employees.EmployeeId
ORDER BY employees.LastName, invoices.InvoiceDate;
```

```python
query2 = """
SELECT 
    invoices.InvoiceId,
    invoices.InvoiceDate,
    invoices.Total,
    employees.FirstName || ' ' || employees.LastName AS NombreAgente,
    employees.Title
FROM invoices
INNER JOIN customers ON invoices.CustomerId = customers.CustomerId
INNER JOIN employees ON customers.SupportRepId = employees.EmployeeId
ORDER BY employees.LastName, invoices.InvoiceDate;
"""

df2 = pd.read_sql_query(query2, conn)
print(f"Total de facturas con agentes asignados: {len(df2)}")
df2.head(20)
```

---

## Ejercicio 3: Obtén el nombre del cliente, el país, el nombre del agente y el total

**Explicación:**
Similar al ejercicio anterior, pero ahora seleccionamos campos específicos de cada tabla:
1. Partimos de `invoices` para obtener el total de cada factura
2. **Primer INNER JOIN:** `invoices` con `customers` (mediante `CustomerId`) para obtener datos del cliente (nombre y país)
3. **Segundo INNER JOIN:** `customers` con `employees` (mediante `SupportRepId`) para obtener el agente de ventas asignado
4. Seleccionamos: nombre del cliente, su país, nombre del agente y el total de la factura
5. Ordenamos por total descendente para ver primero las facturas más grandes

Esta query crea un reporte completo de ventas mostrando la relación Cliente-Agente-Venta.

```sql
SELECT 
    customers.FirstName || ' ' || customers.LastName AS NombreCliente,
    customers.Country AS PaisCliente,
    employees.FirstName || ' ' || employees.LastName AS NombreAgente,
    invoices.Total
FROM invoices
INNER JOIN customers ON invoices.CustomerId = customers.CustomerId
INNER JOIN employees ON customers.SupportRepId = employees.EmployeeId
ORDER BY invoices.Total DESC;
```

```python
query3 = """
SELECT 
    customers.FirstName || ' ' || customers.LastName AS NombreCliente,
    customers.Country AS PaisCliente,
    employees.FirstName || ' ' || employees.LastName AS NombreAgente,
    invoices.Total
FROM invoices
INNER JOIN customers ON invoices.CustomerId = customers.CustomerId
INNER JOIN employees ON customers.SupportRepId = employees.EmployeeId
ORDER BY invoices.Total DESC;
"""

df3 = pd.read_sql_query(query3, conn)
print(f"Total de registros: {len(df3)}")
df3.head(20)
```

---

## Ejercicio 4: Obtén cada artículo de la factura con el nombre de la canción

**Explicación:**
Vamos a unir la tabla de artículos de factura con la tabla de canciones:
1. Partimos de `invoice_items` que contiene cada línea/artículo de las facturas
2. Hacemos un **INNER JOIN** con `tracks` (canciones) usando el campo `TrackId`
3. Esto nos permite ver qué canción específica se vendió en cada línea de factura
4. Además de los datos básicos, calculamos el subtotal multiplicando precio unitario por cantidad
5. Ordenamos por ID de factura y línea para agrupar los artículos de cada factura

**Relación:** Artículo de factura → Canción

```sql
SELECT 
    invoice_items.InvoiceLineId,
    invoice_items.InvoiceId,
    tracks.Name AS NombreCancion,
    invoice_items.UnitPrice,
    invoice_items.Quantity,
    invoice_items.UnitPrice * invoice_items.Quantity AS Subtotal
FROM invoice_items
INNER JOIN tracks ON invoice_items.TrackId = tracks.TrackId
ORDER BY invoice_items.InvoiceId, invoice_items.InvoiceLineId;
```

```python
query4 = """
SELECT 
    invoice_items.InvoiceLineId,
    invoice_items.InvoiceId,
    tracks.Name AS NombreCancion,
    invoice_items.UnitPrice,
    invoice_items.Quantity,
    invoice_items.UnitPrice * invoice_items.Quantity AS Subtotal
FROM invoice_items
INNER JOIN tracks ON invoice_items.TrackId = tracks.TrackId
ORDER BY invoice_items.InvoiceId, invoice_items.InvoiceLineId;
"""

df4 = pd.read_sql_query(query4, conn)
print(f"Total de artículos en facturas: {len(df4)}")
df4.head(20)
```

---

## Ejercicio 5: Muestra todas las canciones con su nombre, formato, álbum y género

**Explicación:**
Esta query requiere **tres INNER JOINs** para obtener información completa de cada canción desde múltiples tablas:
1. Partimos de `tracks` (canciones) como tabla principal
2. **Primer JOIN:** con `media_types` (mediante `MediaTypeId`) para obtener el formato (MP3, AAC, etc.)
3. **Segundo JOIN:** con `albums` (mediante `AlbumId`) para saber a qué álbum pertenece cada canción
4. **Tercer JOIN:** con `genres` (mediante `GenreId`) para conocer el género musical
5. Además, convertimos los milisegundos a minutos dividiendo entre 1000 (segundos) y luego entre 60 (minutos)
6. Ordenamos alfabéticamente por nombre de canción

**Relación:** Canción → Tipo de medio, Canción → Álbum, Canción → Género

```sql
SELECT 
    tracks.Name AS NombreCancion,
    media_types.Name AS Formato,
    albums.Title AS NombreAlbum,
    genres.Name AS Genero,
    tracks.Milliseconds / 1000.0 / 60.0 AS DuracionMinutos
FROM tracks
INNER JOIN media_types ON tracks.MediaTypeId = media_types.MediaTypeId
INNER JOIN albums ON tracks.AlbumId = albums.AlbumId
INNER JOIN genres ON tracks.GenreId = genres.GenreId
ORDER BY tracks.Name;
```

```python
query5 = """
SELECT 
    tracks.Name AS NombreCancion,
    media_types.Name AS Formato,
    albums.Title AS NombreAlbum,
    genres.Name AS Genero,
    tracks.Milliseconds / 1000.0 / 60.0 AS DuracionMinutos
FROM tracks
INNER JOIN media_types ON tracks.MediaTypeId = media_types.MediaTypeId
INNER JOIN albums ON tracks.AlbumId = albums.AlbumId
INNER JOIN genres ON tracks.GenreId = genres.GenreId
ORDER BY tracks.Name;
"""

df5 = pd.read_sql_query(query5, conn)
print(f"Total de canciones: {len(df5)}")
df5.head(20)
```

---

## Ejercicio 6: Cuántas canciones hay en cada playlist

**Explicación:**
Para contar las canciones por playlist necesitamos unir dos tablas y hacer una agregación:
1. Partimos de la tabla `playlists` que contiene las listas de reproducción
2. Hacemos un **LEFT JOIN** (no INNER) con `playlist_track` mediante `PlaylistId`
   - Usamos LEFT JOIN para incluir también playlists que puedan estar vacías (sin canciones)
3. `playlist_track` es una tabla intermedia que relaciona playlists con canciones (relación muchos a muchos)
4. Usamos `GROUP BY` para agrupar por playlist
5. `COUNT(playlist_track.TrackId)` cuenta cuántas canciones tiene cada playlist
6. Ordenamos descendente para ver primero las playlists con más canciones

**Relación:** Playlist ← playlist_track (tabla intermedia) → Tracks

```sql
SELECT 
    playlists.Name AS NombrePlaylist,
    COUNT(playlist_track.TrackId) AS NumeroCanciones
FROM playlists
LEFT JOIN playlist_track ON playlists.PlaylistId = playlist_track.PlaylistId
GROUP BY playlists.PlaylistId, playlists.Name
ORDER BY NumeroCanciones DESC;
```

```python
query6 = """
SELECT 
    playlists.Name AS NombrePlaylist,
    COUNT(playlist_track.TrackId) AS NumeroCanciones
FROM playlists
LEFT JOIN playlist_track ON playlists.PlaylistId = playlist_track.PlaylistId
GROUP BY playlists.PlaylistId, playlists.Name
ORDER BY NumeroCanciones DESC;
"""

df6 = pd.read_sql_query(query6, conn)
print(f"Total de playlists: {len(df6)}")
df6
```

### Visualización de las playlists con más canciones

```python
# Visualización de las playlists con más canciones
plt.figure(figsize=(12, 6))
plt.barh(df6['NombrePlaylist'][:10], df6['NumeroCanciones'][:10], color='skyblue')
plt.xlabel('Número de Canciones')
plt.ylabel('Playlist')
plt.title('Top 10 Playlists con más canciones')
plt.tight_layout()
plt.show()
```

---

## Ejercicio 7: Cuánto ha vendido cada empleado

**Explicación:**
Para calcular las ventas por empleado necesitamos conectar empleados con sus facturas a través de los clientes:
1. Partimos de la tabla `employees` para listar todos los empleados
2. **Primer LEFT JOIN:** con `customers` mediante `SupportRepId` (ID del empleado asignado como agente de ventas)
   - Usamos LEFT JOIN para incluir empleados sin clientes asignados
3. **Segundo LEFT JOIN:** con `invoices` mediante `CustomerId` para obtener las facturas de esos clientes
4. Usamos `GROUP BY` para agrupar por empleado
5. `COUNT(DISTINCT invoices.InvoiceId)` cuenta facturas únicas (DISTINCT evita duplicados)
6. `SUM(invoices.Total)` suma todos los totales de las facturas
7. `ROUND(..., 2)` redondea a 2 decimales para formato monetario
8. Ordenamos por ventas totales descendente

**Relación:** Empleado → Clientes asignados → Facturas de esos clientes

```sql
SELECT 
    employees.EmployeeId,
    employees.FirstName || ' ' || employees.LastName AS NombreEmpleado,
    employees.Title,
    COUNT(DISTINCT invoices.InvoiceId) AS NumeroFacturas,
    ROUND(SUM(invoices.Total), 2) AS TotalVentas
FROM employees
LEFT JOIN customers ON employees.EmployeeId = customers.SupportRepId
LEFT JOIN invoices ON customers.CustomerId = invoices.CustomerId
GROUP BY employees.EmployeeId, employees.FirstName, employees.LastName, employees.Title
ORDER BY TotalVentas DESC;
```

```python
query7 = """
SELECT 
    employees.EmployeeId,
    employees.FirstName || ' ' || employees.LastName AS NombreEmpleado,
    employees.Title,
    COUNT(DISTINCT invoices.InvoiceId) AS NumeroFacturas,
    ROUND(SUM(invoices.Total), 2) AS TotalVentas
FROM employees
LEFT JOIN customers ON employees.EmployeeId = customers.SupportRepId
LEFT JOIN invoices ON customers.CustomerId = invoices.CustomerId
GROUP BY employees.EmployeeId, employees.FirstName, employees.LastName, employees.Title
ORDER BY TotalVentas DESC;
"""

df7 = pd.read_sql_query(query7, conn)
print(f"Total de empleados: {len(df7)}")
df7
```

### Visualización de ventas por empleado

```python
# Visualización de ventas por empleado (solo agentes de ventas)
df7_ventas = df7[df7['Title'] == 'Sales Support Agent']

plt.figure(figsize=(10, 6))
plt.bar(df7_ventas['NombreEmpleado'], df7_ventas['TotalVentas'], color='coral')
plt.xlabel('Empleado')
plt.ylabel('Total Ventas ($)')
plt.title('Ventas Totales por Agente de Ventas')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
```

---

## Ejercicio 8: ¿Quién ha sido el agente de ventas que más ha vendido en 2009?

**Explicación:**
Similar al ejercicio 7, pero con filtros adicionales para un año específico y limitando el resultado:
1. Unimos `employees` con `customers` mediante `SupportRepId`
2. Unimos `customers` con `invoices` mediante `CustomerId`
3. **Usamos INNER JOIN** (no LEFT) porque solo queremos empleados con ventas
4. Filtramos con dos condiciones en WHERE:
   - `strftime('%Y', invoices.InvoiceDate) = '2009'` → solo facturas de 2009
   - `employees.Title = 'Sales Support Agent'` → solo agentes de ventas
5. Agrupamos por empleado y sumamos sus ventas del 2009
6. Ordenamos descendente por total de ventas
7. **LIMIT 1** nos da solo el primer resultado: el empleado con más ventas

**Relación:** Empleado (agente) → Clientes → Facturas del 2009

```sql
SELECT 
    employees.EmployeeId,
    employees.FirstName || ' ' || employees.LastName AS NombreEmpleado,
    employees.Title,
    COUNT(DISTINCT invoices.InvoiceId) AS NumeroFacturas,
    ROUND(SUM(invoices.Total), 2) AS TotalVentas2009
FROM employees
INNER JOIN customers ON employees.EmployeeId = customers.SupportRepId
INNER JOIN invoices ON customers.CustomerId = invoices.CustomerId
WHERE strftime('%Y', invoices.InvoiceDate) = '2009'
    AND employees.Title = 'Sales Support Agent'
GROUP BY employees.EmployeeId, employees.FirstName, employees.LastName, employees.Title
ORDER BY TotalVentas2009 DESC
LIMIT 1;
```

```python
query8 = """
SELECT 
    employees.EmployeeId,
    employees.FirstName || ' ' || employees.LastName AS NombreEmpleado,
    employees.Title,
    COUNT(DISTINCT invoices.InvoiceId) AS NumeroFacturas,
    ROUND(SUM(invoices.Total), 2) AS TotalVentas2009
FROM employees
INNER JOIN customers ON employees.EmployeeId = customers.SupportRepId
INNER JOIN invoices ON customers.CustomerId = invoices.CustomerId
WHERE strftime('%Y', invoices.InvoiceDate) = '2009'
    AND employees.Title = 'Sales Support Agent'
GROUP BY employees.EmployeeId, employees.FirstName, employees.LastName, employees.Title
ORDER BY TotalVentas2009 DESC
LIMIT 1;
"""

df8 = pd.read_sql_query(query8, conn)
print("El agente de ventas que más vendió en 2009:")
df8
```

### Comparación de todos los agentes en 2009

```python
# Mostrar todos los agentes de ventas en 2009 para comparación
query8_all = """
SELECT 
    employees.FirstName || ' ' || employees.LastName AS NombreEmpleado,
    COUNT(DISTINCT invoices.InvoiceId) AS NumeroFacturas,
    ROUND(SUM(invoices.Total), 2) AS TotalVentas2009
FROM employees
INNER JOIN customers ON employees.EmployeeId = customers.SupportRepId
INNER JOIN invoices ON customers.CustomerId = invoices.CustomerId
WHERE strftime('%Y', invoices.InvoiceDate) = '2009'
    AND employees.Title = 'Sales Support Agent'
GROUP BY employees.EmployeeId, employees.FirstName, employees.LastName
ORDER BY TotalVentas2009 DESC;
"""

df8_all = pd.read_sql_query(query8_all, conn)
print("Comparación de todos los agentes en 2009:")
df8_all
```

---

## Ejercicio 9: ¿Cuáles son los 3 grupos que más han vendido?

**Explicación:**
Para saber qué artistas han vendido más, necesitamos conectar artistas con las ventas reales haciendo **tres INNER JOINs**:
1. Partimos de `artists` (artistas/grupos)
2. **Primer JOIN:** con `albums` mediante `ArtistId` → para relacionar artistas con sus álbumes
3. **Segundo JOIN:** con `tracks` mediante `AlbumId` → para obtener las canciones de cada álbum
4. **Tercer JOIN:** con `invoice_items` mediante `TrackId` → para ver qué canciones se vendieron realmente
5. Agrupamos por artista para consolidar todas sus ventas
6. `COUNT(DISTINCT invoice_items.InvoiceLineId)` cuenta el número de veces que se vendieron sus canciones
7. `SUM(invoice_items.UnitPrice * invoice_items.Quantity)` calcula el total de dinero generado
8. Ordenamos por ventas totales descendente
9. **LIMIT 3** nos da solo los 3 artistas con mayores ventas

**Relación:** Artista → Álbumes → Canciones → Artículos vendidos

```sql
SELECT 
    artists.ArtistId,
    artists.Name AS NombreArtista,
    COUNT(DISTINCT invoice_items.InvoiceLineId) AS UnidadesVendidas,
    ROUND(SUM(invoice_items.UnitPrice * invoice_items.Quantity), 2) AS TotalVentas
FROM artists
INNER JOIN albums ON artists.ArtistId = albums.ArtistId
INNER JOIN tracks ON albums.AlbumId = tracks.AlbumId
INNER JOIN invoice_items ON tracks.TrackId = invoice_items.TrackId
GROUP BY artists.ArtistId, artists.Name
ORDER BY TotalVentas DESC
LIMIT 3;
```

```python
query9 = """
SELECT 
    artists.ArtistId,
    artists.Name AS NombreArtista,
    COUNT(DISTINCT invoice_items.InvoiceLineId) AS UnidadesVendidas,
    ROUND(SUM(invoice_items.UnitPrice * invoice_items.Quantity), 2) AS TotalVentas
FROM artists
INNER JOIN albums ON artists.ArtistId = albums.ArtistId
INNER JOIN tracks ON albums.AlbumId = tracks.AlbumId
INNER JOIN invoice_items ON tracks.TrackId = invoice_items.TrackId
GROUP BY artists.ArtistId, artists.Name
ORDER BY TotalVentas DESC
LIMIT 3;
"""

df9 = pd.read_sql_query(query9, conn)
print("Top 3 grupos/artistas que más han vendido:")
df9
```

### Top 10 artistas para más contexto

```python
# Mostrar el Top 10 para más contexto
query9_top10 = """
SELECT 
    artists.Name AS NombreArtista,
    COUNT(DISTINCT invoice_items.InvoiceLineId) AS UnidadesVendidas,
    ROUND(SUM(invoice_items.UnitPrice * invoice_items.Quantity), 2) AS TotalVentas
FROM artists
INNER JOIN albums ON artists.ArtistId = albums.ArtistId
INNER JOIN tracks ON albums.AlbumId = tracks.AlbumId
INNER JOIN invoice_items ON tracks.TrackId = invoice_items.TrackId
GROUP BY artists.ArtistId, artists.Name
ORDER BY TotalVentas DESC
LIMIT 10;
"""

df9_top10 = pd.read_sql_query(query9_top10, conn)
print("Top 10 artistas/grupos:")
df9_top10
```

### Visualización del Top 10 artistas

```python
# Visualización del Top 10 artistas
plt.figure(figsize=(12, 6))
plt.barh(df9_top10['NombreArtista'], df9_top10['TotalVentas'], color='green')
plt.xlabel('Total Ventas ($)')
plt.ylabel('Artista/Grupo')
plt.title('Top 10 Artistas/Grupos por Ventas')
plt.gca().invert_yaxis()  # Para mostrar el más vendido arriba
plt.tight_layout()
plt.show()
```

---

## Resumen Estadístico de las Ventas

```sql
SELECT 
    COUNT(DISTINCT InvoiceId) AS TotalFacturas,
    COUNT(DISTINCT CustomerId) AS TotalClientes,
    ROUND(SUM(Total), 2) AS VentasTotales,
    ROUND(AVG(Total), 2) AS PromedioFactura,
    ROUND(MIN(Total), 2) AS FacturaMinima,
    ROUND(MAX(Total), 2) AS FacturaMaxima
FROM invoices;
```

```python
# Resumen general de ventas
query_resumen = """
SELECT 
    COUNT(DISTINCT InvoiceId) AS TotalFacturas,
    COUNT(DISTINCT CustomerId) AS TotalClientes,
    ROUND(SUM(Total), 2) AS VentasTotales,
    ROUND(AVG(Total), 2) AS PromedioFactura,
    ROUND(MIN(Total), 2) AS FacturaMinima,
    ROUND(MAX(Total), 2) AS FacturaMaxima
FROM invoices;
"""

df_resumen = pd.read_sql_query(query_resumen, conn)
print("Resumen General de Ventas:")
df_resumen
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

### Conceptos SQL Cubiertos:

- ✅ **INNER JOIN** (múltiples tablas)
- ✅ **LEFT JOIN**
- ✅ **GROUP BY** con agregaciones (COUNT, SUM, AVG)
- ✅ **Filtrado con WHERE** y funciones de fecha
- ✅ **Ordenamiento con ORDER BY**
- ✅ **Limitación de resultados con LIMIT**
- ✅ **Concatenación de strings** (`||`)
- ✅ **Funciones de agregación avanzadas**
- ✅ **Subconsultas implícitas**
- ✅ **Cálculos en SELECT** (operaciones matemáticas)

### Visualizaciones incluidas:

- 📊 Gráficos de barras para playlists
- 📊 Comparación de ventas por empleado
- 📊 Top 10 artistas más vendidos

### Antes de ejecutar:

1. Asegúrate de tener la base de datos `chinook.db` en el mismo directorio

2. Instala las dependencias necesarias:
   ```bash
   pip install pandas matplotlib
   ```

3. La base de datos Chinook puede descargarse desde:
   https://www.sqlitetutorial.net/sqlite-sample-database/

### Estructura de las consultas:

Estos ejercicios demuestran patrones comunes en SQL:

- **Consultas de relación uno a muchos**: Clientes → Facturas
- **Consultas de relación muchos a muchos**: Playlists ↔ Tracks
- **Agregaciones con múltiples niveles**: Empleados → Clientes → Facturas
- **Análisis de ventas**: Ranking, totales, promedios
- **Filtros temporales**: Análisis por año específico

### Tips para mejorar el rendimiento:

- Usa `EXPLAIN QUERY PLAN` antes de tus queries para ver cómo SQLite las ejecuta
- Considera crear índices en columnas frecuentemente usadas en JOINs
- Limita los resultados cuando sea posible con `LIMIT`
- Usa `COUNT(DISTINCT ...)` solo cuando sea necesario, ya que es más costoso
