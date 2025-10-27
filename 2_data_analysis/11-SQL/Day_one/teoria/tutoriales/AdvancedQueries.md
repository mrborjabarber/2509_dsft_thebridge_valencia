## Cláusula HAVING de SQL
Una cláusula HAVING especifica que una instrucción SQL SELECT debe devolver solo las filas donde los valores agregados cumplan las condiciones especificadas.
Se agregó al lenguaje SQL porque la palabra clave WHERE no se podía usar con funciones agregadas
Recuerda, WHERE para condiciones antes de agrupar, HAVING para condiciones después de agrupar.

Sintaxis:
```sql
SELECT column_name, aggregate_function(column_name)
FROM table_name
WHERE column_name operator value
GROUP BY column_name
HAVING aggregate_function(column_name) operator value;
```


## Ejemplo de cláusula HAVING de SQL
```sql
-- ¿Qué clientes nunca han realizado un pedido?
SELECT  C.CustomerID,
		C.CompanyName,
		COUNT(O.OrderID) [Total Count of Orders]
FROM Customers C
	LEFT JOIN Orders O ON C.CustomerID = O.CustomerID
GROUP BY C.CustomerID, C.CompanyName
HAVING COUNT(O.OrderID) = 0;
```


## Operador LIKE de SQL y comodines
El operador LIKE se utiliza para buscar un patrón especificado en una columna.
Los caracteres comodín se utilizan con el operador LIKE de SQL.
Necesitaremos lo siguiente:
1. %  Un sustituto de cero o más caracteres
2. _  Un sustituto de un solo carácter


## Ejemplos
```sql
-- Devuelve clientes de Bern, Berlin y Bergamo
SELECT * FROM Customers
WHERE City LIKE 'ber%';
-- Devuelve clientes de Bruxelles, Resende, Buenos Aires etc.
SELECT * FROM Customers
WHERE City LIKE '%es%';
-- Devuelve clientes con regiones CA y WA
select *
from Customers
where Region like '_A'
```


## Función ROUND de SQL
La función ROUND() se utiliza para redondear un campo numérico al número de decimales especificado.

Sintaxis
```sql
SELECT ROUND(column_name,decimals) FROM table_name;
```

Ejemplo
```sql
-- Encuentra el precio total para el pedido con orderid = 10266 y productID = 12
SELECT ROUND((UnitPrice * Quantity * (1 - Discount)), 2), *
FROM [Order Details]
WHERE OrderID = 10266;
```


## Cláusula SELECT TOP de SQL
La cláusula SELECT TOP se utiliza para especificar el número de registros a devolver.

Sintaxis
```sql
SELECT TOP number|percent column_name(s)
FROM table_name;
```
### Equivalente de SELECT TOP en MySQL
Sintaxis de MySQL

```MySQL
SELECT column_name(s)
FROM table_name
LIMIT number;
```


## Función ISNULL de SQL
Reemplaza NULL con el valor de reemplazo especificado.

Sintaxis
```sql
ISNULL ( check_expression , replacement_value )
```


## Ejemplos de ISNULL de SQL
```sql
SELECT ISNULL(NULL, 'thebridge.tech');
--Resultado: 'thebridge.tech'
SELECT ISNULL('Kaggle.com', 'thebridge.com');
--Resultado: 'Kaggle.com'

SELECT ISNULL(NULL, 45);
--Resultado: 45
SELECT ISNULL(12, 45);
--Resultado: 12

SELECT ISNULL(NULL, '2014-05-01');
--Resultado: '2014-05-01'
SELECT ISNULL('2014-04-30', '2014-05-01');
--Resultado: '2014-04-30'
```


## Variables de SQL
Objeto que contiene un solo valor de datos de un tipo especificado

Usos:
* Mantener datos para uso posterior
* Contadores
* Como entradas o salidas a procedimientos almacenados, funciones

Sintaxis:
```sql
DECLARE <@var_nam> <data_type>
```


## Ejemplos de variables de SQL
```sql
DECLARE @i int;
DECLARE @stringVar VARCHAR(200);
DECLARE @myDate DATETIME;
```


## Asignación de valores a variables de SQL
### SET
Se utiliza para establecer un valor a una variable escalar (no tabla).
Sintaxis:
```sql
DECLARE <@var_nam> <data_type>;
SET <@var_nam> = value;
```

Ejemplo:
```sql
DECLARE @i INT;
SET @i = 10;
SET @stringVar = 'Coding Bootcamp';
```


## Asignación de valores a variables de SQL
### SELECT
* Se utiliza para establecer un valor a una variable escalar
* También se puede usar para establecer valores a múltiples variables a la vez

Sintaxis:
```sql
SELECT @i = 1,
       @stringVar = 'Coding Bootcamp';
       @myDate = '2016-10-24'
```


## SET vs SELECT para asignar valores a variables
* SET es el estándar ANSI para asignación de variables, SELECT no lo es
* SET solo puede asignar una variable a la vez, SELECT puede hacer múltiples asignaciones a la vez
* Si se asigna desde una consulta, SET solo puede asignar un valor escalar. Si la consulta devuelve múltiples valores/filas, SET generará un error. SELECT asignará uno de los valores a la variable y ocultará el hecho de que se devolvieron múltiples valores
* Al asignar desde una consulta, si no se devuelve ningún valor, SET asignará NULL, mientras que SELECT no hará la asignación en absoluto (por lo que la variable no se cambiará de su valor anterior)
* En cuanto a diferencias de velocidad, no hay diferencias directas entre SET y SELECT. Sin embargo, la capacidad de SELECT para hacer múltiples asignaciones de una sola vez le da una ligera ventaja de velocidad sobre SET.


## Tablas temporales
Se pueden usar como espacio de trabajo para resultados intermedios.

Pueden ser
* Tablas temporales locales (que comienzan con #)
* Tablas temporales globales (que comienzan con ##)
* Variables de tabla (que comienzan con @)
* Otras (no en el alcance de nuestra lección)


## Variables de TABLA
* Se utilizan en el ámbito de la rutina o lote dentro del cual se definen
* Causan menos recompilaciones
* No se ven afectadas por rollbacks

Ejemplo de sintaxis:
```sql
DECLARE @myStudents TABLE
		(ID int,
		LastName VARCHAR(50),
		FirstName VARCHAR(50)
		);
```


## Tablas temporales
* Soportan todas las características que puede tener una tabla de base de datos
* Se pueden alterar después de la creación
* Pueden tener múltiples índices
* Se pueden usar con SQL dinámico
* Pueden ser locales (#) o globales (##)

Ejemplo de sintaxis:
```sql
CREATE TABLE #myStudents
		(ID int,
		LastName VARCHAR(50),
		FirstName VARCHAR(50)
		);
```
Recuerda, ¡puede que tengamos que eliminarla manualmente!


### SELECT INTO
Podemos tomar los resultados de una consulta e insertarlos en una NUEVA tabla temporal.
El conjunto de resultados debe tener columnas nombradas de forma única que serán las columnas de la nueva tabla temporal.

Sintaxis:
```sql
-- Crear una tabla temporal que contiene el id de cada pedido y los ingresos totales de ese pedido
SELECT O.OrderID, SUM(ROUND((UnitPrice * Quantity * (1 - Discount)), 2)) [Final Price]
INTO #tempFinalPrices
FROM Orders O
	INNER JOIN [Order Details] OD ON O.OrderID = OD.OrderID
GROUP BY O.OrderID;

SELECT * FROM #tempFinalPrices;

DROP TABLE #tempFinalPrices;
```


## Operador IN de SQL
El operador IN te permite especificar múltiples valores en una cláusula WHERE.

Sintaxis:
```sql
SELECT column_name(s)
FROM table_name
WHERE column_name IN (value1,value2,...);
```


## Ejemplo del operador IN de SQL
```sql
-- ¿Cuántos objetos ha pedido cada cliente de Canadá, Reino Unido y Estados Unidos cada año?
SELECT C.CompanyName, C.Country, YEAR(O.OrderDate) AS [Year], SUM( OD.Quantity ) [Total Quantity]
FROM Customers C
	INNER JOIN Orders O ON C.CustomerID = O.CustomerID
	INNER JOIN [Order Details] OD ON O.OrderID = OD.OrderID
WHERE C.Country IN ('UK', 'USA', 'Canada')
GROUP BY C.CompanyName, YEAR(O.OrderDate), C.Country
ORDER BY C.CompanyName, YEAR(O.OrderDate);
```


## Subconsultas
Consultas incrustadas en consultas.

Ejemplo:
```sql
-- Encuentra el nombre de la empresa que realizó el pedido 10290.
SELECT CompanyName
FROM Customers
WHERE CustomerID = (SELECT CustomerID
			FROM Orders
			WHERE OrderID = 10290);
```
Mejor ejemplo de por qué usar una subconsulta:

Ejemplo:
```sql
-- Encuentra las empresas que realizaron pedidos en 1997
SELECT CompanyName
FROM Customers
WHERE CustomerID IN (SELECT CustomerID
			FROM Orders
			WHERE OrderDate BETWEEN '1997-01-01' AND '1997-12-31');
```


## VISTAS
Una vista es una tabla virtual. Una vista no es más que una instrucción SQL que se almacena en la base de datos
con un nombre asociado. Una vista es en realidad una composición de una tabla en forma de una consulta SQL predefinida.

Sintaxis
```sql
CREATE VIEW view_name AS
SELECT column1, column2.....
FROM table_name
WHERE [condition];
```


## Ejemplo de VISTAS
```sql
CREATE VIEW [Current Product List] AS
SELECT ProductID,ProductName
FROM Products
WHERE Discontinued=0;

SELECT * FROM [Current Product List];
```


## Consejos y trucos para los ejercicios
* Usa alias para nombres de tablas (ej. SELECT C.CompanyName FROM Customers AS C)
* Usa DISTINCT para resultados distintos (para propósitos de verificación)
* BEGIN TRANSACTION ... ROLLBACK para comandos INSERT, UPDATE, DELETE
* Usa @@ROWCOUNT para verificar el número de filas afectadas
* Usa siempre la cláusula WHERE para comandos DELETE y UPDATE
* Intenta nunca usar CURSORS y bucles WHILE
* Prefiere variables de tabla a tablas temporales
