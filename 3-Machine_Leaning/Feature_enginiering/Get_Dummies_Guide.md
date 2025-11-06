# pd.get_dummies() - Guía Completa

## Índice

1. [¿Qué es get_dummies()?](#qué-es-get_dummies)
2. [Ejemplo Simple](#ejemplo-simple)
3. [Cómo Funciona](#cómo-funciona)
4. [Parámetros Principales](#parámetros-principales)
5. [Casos Prácticos](#casos-prácticos)
6. [Comparación: get_dummies vs OneHotEncoder](#comparación-get_dummies-vs-onehotencoder)
7. [Ejemplo Completo con Train/Test](#ejemplo-completo-con-traintest)
8. [Problemas Comunes y Soluciones](#problemas-comunes-y-soluciones)
9. [Resumen](#resumen)

---

## ¿Qué es get_dummies()?

**pd.get_dummies()** es una función de pandas que convierte variables categóricas en **variables dummy (binarias)** usando codificación One-Hot Encoding.

### Características principales

- Convierte cada categoría en una columna binaria separada (0 o 1)
- Es más simple y rápida que OneHotEncoder de scikit-learn
- Trabaja directamente con DataFrames de pandas
- No requiere fit/transform (menos control pero más conveniente)
- Automáticamente detecta columnas categóricas

### ¿Qué es One-Hot Encoding?

Transforma una columna categórica en múltiples columnas binarias, una por cada categoría única.

**Ejemplo visual:**
```
Original:        One-Hot Encoding:
Color            Color_rojo  Color_azul  Color_verde
-----            ----------  ----------  -----------
rojo      →           1          0           0
azul      →           0          1           0
verde     →           0          0           1
rojo      →           1          0           0
```

---

## Ejemplo Simple

```python
import pandas as pd

# Crear un DataFrame simple
df = pd.DataFrame({
    'color': ['rojo', 'azul', 'verde', 'rojo', 'verde'],
    'precio': [10, 20, 15, 12, 18]
})

print("DataFrame original:")
print(df)
print()

# Aplicar get_dummies
df_encoded = pd.get_dummies(df, columns=['color'])

print("DataFrame con get_dummies:")
print(df_encoded)
```

**Salida:**
```
DataFrame original:
   color  precio
0   rojo      10
1   azul      20
2  verde      15
3   rojo      12
4  verde      18

DataFrame con get_dummies:
   precio  color_azul  color_rojo  color_verde
0      10           0           1            0
1      20           1           0            0
2      15           0           0            1
3      12           0           1            0
4      18           0           0            1
```

---

## Cómo Funciona

### Sintaxis básica

```python
pd.get_dummies(data, prefix=None, columns=None, drop_first=False, dtype=None)
```

### Diferentes formas de usar get_dummies

```python
import pandas as pd

# 1. Sobre todo el DataFrame (detecta automáticamente object/category)
df = pd.DataFrame({
    'ciudad': ['Madrid', 'Barcelona', 'Valencia'],
    'género': ['M', 'F', 'M'],
    'edad': [25, 30, 35]
})

df_encoded = pd.get_dummies(df)
print("Automático (toda el DataFrame):")
print(df_encoded)
print()

# 2. Sobre columnas específicas
df_encoded = pd.get_dummies(df, columns=['ciudad'])
print("Columnas específicas:")
print(df_encoded)
print()

# 3. Directamente sobre una Serie
ciudades = pd.Series(['Madrid', 'Barcelona', 'Madrid', 'Valencia'])
ciudad_encoded = pd.get_dummies(ciudades)
print("Sobre una Serie:")
print(ciudad_encoded)
print()

# 4. Con prefijo personalizado
df_encoded = pd.get_dummies(df, columns=['ciudad'], prefix='City')
print("Con prefijo personalizado:")
print(df_encoded)
```

**Salida:**
```
Automático (toda el DataFrame):
   edad  ciudad_Barcelona  ciudad_Madrid  ciudad_Valencia  género_F  género_M
0    25                 0              1                0         0         1
1    30                 1              0                0         1         0
2    35                 0              0                1         0         1

Columnas específicas:
  género  edad  ciudad_Barcelona  ciudad_Madrid  ciudad_Valencia
0      M    25                 0              1                0
1      F    30                 1              0                0
2      M    35                 0              0                1

Sobre una Serie:
   Barcelona  Madrid  Valencia
0          0       1         0
1          1       0         0
2          0       1         0
3          0       0         1

Con prefijo personalizado:
  género  edad  City_Barcelona  City_Madrid  City_Valencia
0      M    25               0            1              0
1      F    30               1            0              0
2      M    35               0            0              1
```

---

## Parámetros Principales

### Tabla de parámetros

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `data` | DataFrame/Series | Datos a codificar | `df` |
| `columns` | list | Columnas específicas a codificar | `['color', 'tamaño']` |
| `prefix` | str/list/dict | Prefijo para nombres de columnas | `'cat_'` o `{'color': 'col'}` |
| `drop_first` | bool | Elimina primera categoría (evita multicolinealidad) | `True` |
| `dtype` | dtype | Tipo de dato de las columnas dummy | `np.uint8` |
| `dummy_na` | bool | Añade columna para valores NaN | `True` |

### Ejemplos de parámetros

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'color': ['rojo', 'azul', 'verde', np.nan, 'rojo'],
    'tamaño': ['S', 'M', 'L', 'S', 'M'],
    'precio': [10, 20, 15, 12, 18]
})

# 1. drop_first=True (elimina primera categoría)
df_drop = pd.get_dummies(df, columns=['color'], drop_first=True)
print("Con drop_first=True:")
print(df_drop)
print()

# 2. dummy_na=True (columna para valores NaN)
df_na = pd.get_dummies(df, columns=['color'], dummy_na=True)
print("Con dummy_na=True:")
print(df_na)
print()

# 3. dtype personalizado (ahorra memoria)
df_uint = pd.get_dummies(df, columns=['color'], dtype=np.uint8)
print("Con dtype=np.uint8:")
print(df_uint.dtypes)
print()

# 4. prefix como diccionario
df_prefix = pd.get_dummies(
    df, 
    columns=['color', 'tamaño'],
    prefix={'color': 'col', 'tamaño': 'tam'}
)
print("Con prefix personalizado por columna:")
print(df_prefix)
```

**Salida:**
```
Con drop_first=True:
  tamaño  precio  color_rojo  color_verde
0      S      10           1            0
1      M      20           0            0
2      L      15           0            1
3      S      12           0            0
4      M      18           1            0

Con dummy_na=True:
  tamaño  precio  color_azul  color_rojo  color_verde  color_nan
0      S      10           0           1            0          0
1      M      20           1           0            0          0
2      L      15           0           0            1          0
3      S      12           0           0            0          1
4      M      18           0           1            0          0

Con dtype=np.uint8:
tamaño       object
precio        int64
color_azul    uint8
color_rojo    uint8
color_verde   uint8
dtype: object

Con prefix personalizado por columna:
   precio  col_azul  col_rojo  col_verde  tam_L  tam_M  tam_S
0      10         0         1          0      0      0      1
1      20         1         0          0      0      1      0
2      15         0         0          1      1      0      0
3      12         0         0          0      0      0      1
4      18         0         1          0      0      1      0
```

---

## Casos Prácticos

### Caso 1: Preparación de datos para Machine Learning

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Dataset de ejemplo
df = pd.DataFrame({
    'ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Madrid', 'Barcelona', 
               'Valencia', 'Madrid', 'Barcelona'],
    'género': ['M', 'F', 'M', 'F', 'M', 'F', 'M', 'F'],
    'edad': [25, 30, 35, 28, 42, 38, 29, 45],
    'compra': [1, 0, 1, 1, 0, 1, 0, 1]
})

print("Dataset original:")
print(df)
print()

# Separar features y target
X = df.drop('compra', axis=1)
y = df['compra']

# Aplicar get_dummies
X_encoded = pd.get_dummies(X, drop_first=True)

print("Features codificadas:")
print(X_encoded)
print()

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.25, random_state=42
)

# Entrenar modelo
modelo = LogisticRegression()
modelo.fit(X_train, y_train)

# Predecir
y_pred = modelo.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.2f}")
```

### Caso 2: Múltiples columnas categóricas

```python
import pandas as pd

df = pd.DataFrame({
    'color': ['rojo', 'azul', 'verde', 'rojo'],
    'tamaño': ['pequeño', 'mediano', 'grande', 'pequeño'],
    'material': ['madera', 'metal', 'plástico', 'metal'],
    'precio': [100, 200, 150, 120]
})

print("Original:")
print(df)
print()

# Codificar todas las columnas categóricas automáticamente
df_encoded = pd.get_dummies(df)

print("Codificado (automático):")
print(df_encoded)
print()

# Codificar solo columnas específicas
df_encoded2 = pd.get_dummies(df, columns=['color', 'tamaño'])

print("Codificado (columnas específicas):")
print(df_encoded2)
```

### Caso 3: Evitar multicolinealidad con drop_first

```python
import pandas as pd

df = pd.DataFrame({
    'género': ['M', 'F', 'M', 'F', 'M']
})

# Sin drop_first (3 columnas: género_F, género_M)
df_sin_drop = pd.get_dummies(df)
print("Sin drop_first:")
print(df_sin_drop)
print()

# Con drop_first (1 columna: género_M)
df_con_drop = pd.get_dummies(df, drop_first=True)
print("Con drop_first=True:")
print(df_con_drop)
print()

print("Explicación:")
print("- Si género_M = 0, entonces es F")
print("- Si género_M = 1, entonces es M")
print("- No necesitamos ambas columnas (redundante)")
```

### Caso 4: Manejo de valores NaN

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'ciudad': ['Madrid', 'Barcelona', np.nan, 'Valencia', 'Madrid'],
    'precio': [100, 200, 150, 120, 180]
})

print("Original con NaN:")
print(df)
print()

# Opción 1: Ignorar NaN (por defecto)
df_ignore = pd.get_dummies(df, columns=['ciudad'])
print("Ignorando NaN:")
print(df_ignore)
print()

# Opción 2: Crear columna para NaN
df_with_na = pd.get_dummies(df, columns=['ciudad'], dummy_na=True)
print("Con columna para NaN:")
print(df_with_na)
```

---

## Comparación: get_dummies vs OneHotEncoder

### Tabla comparativa

| Característica | pd.get_dummies() | sklearn.OneHotEncoder |
|----------------|------------------|-----------------------|
| **Complejidad** | Muy simple | Más complejo |
| **fit/transform** | No requiere | Sí requiere |
| **Control train/test** | Manual | Automático |
| **Salida** | DataFrame (nombres descriptivos) | Array/DataFrame (numérico) |
| **Categorías desconocidas** | Error | Puede manejar con `handle_unknown` |
| **Integración sklearn** | Manual | Nativa (Pipeline) |
| **Velocidad** | Rápida | Rápida |
| **Memoria** | Más eficiente con dtype | Similar |
| **Columnas sparse** | No soporta nativamente | Sí soporta |

### Ejemplos lado a lado

```python
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import numpy as np

# Datos
df = pd.DataFrame({
    'ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Madrid'],
    'precio': [100, 200, 150, 120]
})

print("=" * 50)
print("MÉTODO 1: pd.get_dummies()")
print("=" * 50)

df_dummies = pd.get_dummies(df, columns=['ciudad'])
print(df_dummies)
print("\nTipo:", type(df_dummies))
print("Nombres de columnas:", df_dummies.columns.tolist())

print("\n" + "=" * 50)
print("MÉTODO 2: sklearn.OneHotEncoder")
print("=" * 50)

ohe = OneHotEncoder(sparse_output=False)
ciudad_encoded = ohe.fit_transform(df[['ciudad']])

# Convertir a DataFrame para comparar
df_ohe = pd.DataFrame(
    ciudad_encoded,
    columns=ohe.get_feature_names_out(['ciudad'])
)
df_ohe['precio'] = df['precio'].values

print(df_ohe)
print("\nTipo:", type(df_ohe))
print("Nombres de columnas:", df_ohe.columns.tolist())
```

### Cuándo usar cada uno

**Usar pd.get_dummies() cuando:**
- Necesitas rapidez y simplicidad
- Trabajas exclusivamente en pandas
- Haces análisis exploratorio
- No necesitas reproducir exactamente la transformación
- Trabajas con datasets pequeños/medianos

**Usar OneHotEncoder cuando:**
- Necesitas control exacto entre train/test
- Usas sklearn Pipelines
- Desplegarás el modelo en producción
- Necesitas manejar categorías desconocidas
- Trabajas con datos sparse (muchas categorías)

---

## Ejemplo Completo con Train/Test

### Problema: Alineación de columnas

El principal desafío con `get_dummies()` es que train y test pueden tener diferentes columnas si no aparecen todas las categorías en ambos conjuntos.

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import numpy as np

# Dataset de ejemplo
np.random.seed(42)
df = pd.DataFrame({
    'ciudad': np.random.choice(['Madrid', 'Barcelona', 'Valencia', 'Sevilla'], 100),
    'género': np.random.choice(['M', 'F'], 100),
    'edad': np.random.randint(18, 65, 100),
    'compra': np.random.choice([0, 1], 100)
})

print("Dataset completo:")
print(df.head(10))
print(f"\nForma: {df.shape}")
print(f"\nCategorías en ciudad: {df['ciudad'].unique()}")

# Separar features y target
X = df.drop('compra', axis=1)
y = df['compra']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\n{'='*60}")
print("PROBLEMA: Codificación incorrecta")
print("="*60)

# Método INCORRECTO (diferentes columnas)
X_train_wrong = pd.get_dummies(X_train, drop_first=True)
X_test_wrong = pd.get_dummies(X_test, drop_first=True)

print("\nColumnas en train:", X_train_wrong.columns.tolist())
print("Columnas en test:", X_test_wrong.columns.tolist())
print("\nSon iguales?", X_train_wrong.columns.equals(X_test_wrong.columns))

print(f"\n{'='*60}")
print("SOLUCIÓN 1: Alinear columnas manualmente")
print("="*60)

# Codificar train
X_train_encoded = pd.get_dummies(X_train, drop_first=True)

# Codificar test
X_test_encoded = pd.get_dummies(X_test, drop_first=True)

# Alinear columnas (añadir faltantes con 0, eliminar extras)
X_test_aligned = X_test_encoded.reindex(columns=X_train_encoded.columns, fill_value=0)

print("\nColumnas en train:", X_train_encoded.columns.tolist())
print("Columnas en test alineado:", X_test_aligned.columns.tolist())
print("\nSon iguales?", X_train_encoded.columns.equals(X_test_aligned.columns))

# Entrenar modelo
modelo = LogisticRegression(max_iter=1000)
modelo.fit(X_train_encoded, y_train)

# Predecir
y_pred = modelo.predict(X_test_aligned)
accuracy = accuracy_score(y_test, y_pred)

print(f"\nAccuracy: {accuracy:.2f}")

print(f"\n{'='*60}")
print("SOLUCIÓN 2: Codificar todo antes del split")
print("="*60)

# Método alternativo: codificar antes de split
X_all_encoded = pd.get_dummies(X, drop_first=True)
X_train2, X_test2, y_train2, y_test2 = train_test_split(
    X_all_encoded, y, test_size=0.2, random_state=42
)

print("\nColumnas en train:", X_train2.columns.tolist())
print("Columnas en test:", X_test2.columns.tolist())
print("\nSon iguales?", X_train2.columns.equals(X_test2.columns))

# Entrenar modelo
modelo2 = LogisticRegression(max_iter=1000)
modelo2.fit(X_train2, y_train2)

# Predecir
y_pred2 = modelo2.predict(X_test2)
accuracy2 = accuracy_score(y_test2, y_pred2)

print(f"\nAccuracy: {accuracy2:.2f}")

print("\nNOTA: La Solución 2 es más simple pero puede causar data leakage")
print("si hay transformaciones adicionales basadas en estadísticas de los datos.")
```

### Implementación robusta con función helper

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

def get_dummies_train_test(X_train, X_test, columns=None, drop_first=True):
    """
    Aplica get_dummies asegurando que train y test tengan las mismas columnas.
    
    Parameters:
    -----------
    X_train : DataFrame
        Datos de entrenamiento
    X_test : DataFrame
        Datos de test
    columns : list, optional
        Columnas a codificar (si None, codifica todas las object/category)
    drop_first : bool
        Si True, elimina la primera categoría
    
    Returns:
    --------
    X_train_encoded, X_test_encoded : DataFrames
        DataFrames codificados con las mismas columnas
    """
    # Codificar train
    X_train_encoded = pd.get_dummies(X_train, columns=columns, drop_first=drop_first)
    
    # Codificar test
    X_test_encoded = pd.get_dummies(X_test, columns=columns, drop_first=drop_first)
    
    # Alinear columnas
    # Añadir columnas faltantes en test con valor 0
    for col in X_train_encoded.columns:
        if col not in X_test_encoded.columns:
            X_test_encoded[col] = 0
    
    # Eliminar columnas en test que no están en train
    for col in X_test_encoded.columns:
        if col not in X_train_encoded.columns:
            X_test_encoded = X_test_encoded.drop(col, axis=1)
    
    # Reordenar columnas para que coincidan
    X_test_encoded = X_test_encoded[X_train_encoded.columns]
    
    return X_train_encoded, X_test_encoded


# Ejemplo de uso
df = pd.DataFrame({
    'ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Madrid', 'Sevilla', 
               'Barcelona', 'Madrid', 'Valencia'] * 10,
    'género': ['M', 'F', 'M', 'F', 'M', 'F', 'M', 'F'] * 10,
    'edad': [25, 30, 35, 28, 42, 38, 29, 45] * 10,
    'compra': [1, 0, 1, 1, 0, 1, 0, 1] * 10
})

# Separar features y target
X = df.drop('compra', axis=1)
y = df['compra']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Aplicar función helper
X_train_enc, X_test_enc = get_dummies_train_test(
    X_train, X_test, 
    columns=['ciudad', 'género'], 
    drop_first=True
)

print("Forma train:", X_train_enc.shape)
print("Forma test:", X_test_enc.shape)
print("\nColumnas coinciden?", X_train_enc.columns.equals(X_test_enc.columns))

# Entrenar modelo
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train_enc, y_train)

# Evaluar
y_pred = modelo.predict(X_test_enc)
print("\nReporte de clasificación:")
print(classification_report(y_test, y_pred))
```

---

## Problemas Comunes y Soluciones

### Problema 1: Columnas diferentes en train/test

**Problema:**
```python
X_train_enc = pd.get_dummies(X_train)
X_test_enc = pd.get_dummies(X_test)
# Error: diferentes columnas si no aparecen todas las categorías
```

**Solución:**
```python
# Usar función helper o reindex
X_test_enc = X_test_enc.reindex(columns=X_train_enc.columns, fill_value=0)
```

### Problema 2: Multicolinealidad

**Problema:**
```python
# Sin drop_first crea variables redundantes
df_enc = pd.get_dummies(df, columns=['género'])
# Crea: género_M y género_F (redundante, una implica la otra)
```

**Solución:**
```python
# Usar drop_first=True
df_enc = pd.get_dummies(df, columns=['género'], drop_first=True)
# Crea solo: género_M (si 0 = F, si 1 = M)
```

### Problema 3: Demasiadas columnas (alta cardinalidad)

**Problema:**
```python
# Columna con muchas categorías únicas
df['código_postal'] = ['28001', '28002', '28003', ...]  # 1000+ valores únicos
df_enc = pd.get_dummies(df, columns=['código_postal'])
# Resultado: 1000+ columnas nuevas
```

**Soluciones:**
```python
# Solución 1: Agrupar categorías
df['zona'] = df['código_postal'].str[:2]  # Primeros 2 dígitos
df_enc = pd.get_dummies(df, columns=['zona'])

# Solución 2: Target Encoding
from category_encoders import TargetEncoder
te = TargetEncoder()
df['código_postal_encoded'] = te.fit_transform(df['código_postal'], df['target'])

# Solución 3: Frequency Encoding
freq = df['código_postal'].value_counts(normalize=True)
df['código_postal_freq'] = df['código_postal'].map(freq)
```

### Problema 4: Pérdida de información de NaN

**Problema:**
```python
import numpy as np
df = pd.DataFrame({'ciudad': ['Madrid', np.nan, 'Barcelona']})
df_enc = pd.get_dummies(df)
# NaN se ignora, perdemos la información de que faltaba
```

**Solución:**
```python
# Usar dummy_na=True
df_enc = pd.get_dummies(df, dummy_na=True)
# Crea columna ciudad_nan para identificar valores faltantes
```

### Problema 5: Alto uso de memoria

**Problema:**
```python
# Por defecto crea columnas uint8/int64
df_enc = pd.get_dummies(df, columns=['categoria'])
print(df_enc.memory_usage(deep=True))
```

**Solución:**
```python
# Usar dtype más eficiente
df_enc = pd.get_dummies(df, columns=['categoria'], dtype=np.uint8)
# uint8 usa 1 byte vs 8 bytes de int64 (87.5% menos memoria)
```

### Problema 6: Nombres de columnas con espacios/caracteres especiales

**Problema:**
```python
df = pd.DataFrame({'tipo producto': ['tipo A', 'tipo B', 'tipo C']})
df_enc = pd.get_dummies(df)
# Crea: "tipo producto_tipo A" (con espacios)
```

**Solución:**
```python
# Limpiar nombres antes
df.columns = df.columns.str.replace(' ', '_')
df['tipo_producto'] = df['tipo_producto'].str.replace(' ', '_')
df_enc = pd.get_dummies(df)
# Crea: "tipo_producto_tipo_A"
```

---

## Resumen

### Ventajas de pd.get_dummies()

- Extremadamente simple de usar
- Integración nativa con pandas
- Rápida para datasets pequeños/medianos
- Nombres de columnas descriptivos
- No requiere fit/transform
- Ideal para análisis exploratorio

### Desventajas de pd.get_dummies()

- No maneja bien train/test (requiere alineación manual)
- No hay control de categorías desconocidas
- No se integra con sklearn Pipelines
- Puede crear muchas columnas (alta cardinalidad)
- Requiere más trabajo manual en producción

### Mejores prácticas

1. **Usa drop_first=True** para evitar multicolinealidad
2. **Alinea columnas** entre train y test con `reindex()`
3. **Usa dtype=np.uint8** para ahorrar memoria
4. **Considera dummy_na=True** si los NaN son informativos
5. **Para producción**, considera usar OneHotEncoder
6. **Limpia nombres** de columnas y categorías antes de codificar
7. **Agrupa categorías** si hay alta cardinalidad

### Código mínimo funcional

```python
import pandas as pd

# Simple
df_encoded = pd.get_dummies(df, columns=['columna_cat'], drop_first=True)

# Con train/test
X_train_enc = pd.get_dummies(X_train, drop_first=True)
X_test_enc = pd.get_dummies(X_test, drop_first=True)
X_test_enc = X_test_enc.reindex(columns=X_train_enc.columns, fill_value=0)
```

### Cuándo usar get_dummies()

**Casos ideales:**
- Análisis exploratorio de datos
- Prototipos rápidos
- Notebooks de Jupyter
- Datasets pequeños/medianos
- Cuando trabajas exclusivamente en pandas

**Casos donde considerar alternativas:**
- Pipelines de producción → OneHotEncoder
- Alta cardinalidad → Target/Frequency Encoding
- Necesitas reproducibilidad exacta → OneHotEncoder
- Integración con sklearn → OneHotEncoder

### Alternativas relacionadas

- **sklearn.preprocessing.OneHotEncoder:** Más control, mejor para producción
- **category_encoders.OneHotEncoder:** Versión mejorada con más opciones
- **pd.factorize():** Para Label Encoding simple
- **sklearn.preprocessing.LabelEncoder:** Label Encoding con fit/transform
- **category_encoders.TargetEncoder:** Para alta cardinalidad

---

## Referencias

- Documentación oficial: [pandas.get_dummies](https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html)
- Guía de categorical data: [Working with categorical data](https://pandas.pydata.org/docs/user_guide/categorical.html)
- Comparación con OneHotEncoder: [sklearn.preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html#encoding-categorical-features)
