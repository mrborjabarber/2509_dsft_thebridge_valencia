# OneHotEncoder (sklearn) - Guía Completa

## Índice

1. [¿Qué es OneHotEncoder?](#qué-es-onehotencoder)
2. [Ejemplo Simple](#ejemplo-simple)
3. [Cómo Funciona: fit, transform, fit_transform](#cómo-funciona-fit-transform-fit_transform)
4. [Parámetros Principales](#parámetros-principales)
5. [Casos Prácticos](#casos-prácticos)
6. [Comparación: OneHotEncoder vs get_dummies](#comparación-onehotencoder-vs-get_dummies)
7. [Integración con Pipelines](#integración-con-pipelines)
8. [Ejemplo Completo con Train/Test](#ejemplo-completo-con-traintest)
9. [Problemas Comunes y Soluciones](#problemas-comunes-y-soluciones)
10. [Resumen](#resumen)

---

## ¿Qué es OneHotEncoder?

**OneHotEncoder** es una clase de scikit-learn que convierte variables categóricas en **variables dummy binarias** mediante One-Hot Encoding. Es la versión profesional y robusta de `pd.get_dummies()`.

### Características principales

- Parte del ecosistema scikit-learn (sklearn)
- Sistema fit/transform para control preciso entre train/test
- Maneja categorías desconocidas en test
- Se integra perfectamente con Pipelines
- Soporta matrices sparse para eficiencia de memoria
- Ideal para despliegue en producción

### ¿Qué es One-Hot Encoding?

Transforma una columna categórica en múltiples columnas binarias, una por cada categoría única.

**Ejemplo visual:**
```
Original:        One-Hot Encoding:
Color            [Col_rojo, Col_azul, Col_verde]
-----            ---------------------------------
rojo      →           [1,      0,        0]
azul      →           [0,      1,        0]
verde     →           [0,      0,        1]
rojo      →           [1,      0,        0]
```

---

## Ejemplo Simple

```python
from sklearn.preprocessing import OneHotEncoder
import numpy as np

# Datos categóricos (debe ser 2D: filas x columnas)
colores = np.array([['rojo'], ['azul'], ['verde'], ['rojo'], ['verde']])

# Crear el encoder
ohe = OneHotEncoder(sparse_output=False)

# Fit: aprender las categorías
# Transform: convertir a one-hot
colores_encoded = ohe.fit_transform(colores)

print("Colores originales:")
print(colores.flatten())
print("\nColores codificados (one-hot):")
print(colores_encoded)
print("\nCategorías aprendidas:")
print(ohe.categories_)
print("\nNombres de features:")
print(ohe.get_feature_names_out())
```

**Salida:**
```
Colores originales:
['rojo' 'azul' 'verde' 'rojo' 'verde']

Colores codificados (one-hot):
[[0. 0. 1.]
 [1. 0. 0.]
 [0. 1. 0.]
 [0. 0. 1.]
 [0. 1. 0.]]

Categorías aprendidas:
[array(['azul', 'verde', 'rojo'], dtype=object)]

Nombres de features:
['x0_azul' 'x0_verde' 'x0_rojo']
```

---

## Cómo Funciona: fit, transform, fit_transform

### Métodos principales

```python
from sklearn.preprocessing import OneHotEncoder
import numpy as np

# Datos de entrenamiento
train_data = np.array([['Madrid'], ['Barcelona'], ['Valencia'], ['Madrid']])

# Datos de test
test_data = np.array([['Barcelona'], ['Madrid'], ['Sevilla']])

# Crear encoder
ohe = OneHotEncoder(sparse_output=False)

print("="*60)
print("1. fit() - Aprender categorías")
print("="*60)
ohe.fit(train_data)
print("Categorías aprendidas:", ohe.categories_)

print("\n" + "="*60)
print("2. transform() - Convertir a one-hot")
print("="*60)
train_encoded = ohe.transform(train_data)
print("Train transformado:")
print(train_encoded)

print("\n" + "="*60)
print("3. fit_transform() - fit + transform en un paso")
print("="*60)
ohe2 = OneHotEncoder(sparse_output=False)
train_encoded2 = ohe2.fit_transform(train_data)
print("Train con fit_transform:")
print(train_encoded2)

print("\n" + "="*60)
print("4. inverse_transform() - Recuperar categorías originales")
print("="*60)
original = ohe.inverse_transform(train_encoded)
print("Recuperado:")
print(original)

print("\n" + "="*60)
print("5. Manejo de categorías desconocidas")
print("="*60)
try:
    # Por defecto da error con categorías nuevas
    test_encoded = ohe.transform(test_data)
except ValueError as e:
    print(f"Error: {e}")

# Solución: handle_unknown='ignore'
ohe3 = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
ohe3.fit(train_data)
test_encoded = ohe3.transform(test_data)
print("\nTest transformado (con handle_unknown='ignore'):")
print(test_encoded)
print("Nota: 'Sevilla' se codifica como [0, 0, 0]")
```

### Tabla de métodos

| Método | Descripción | Cuándo usar | Ejemplo |
|--------|-------------|-------------|---------|
| `fit(X)` | Aprende las categorías únicas de X | Solo en datos de entrenamiento | `ohe.fit(X_train)` |
| `transform(X)` | Convierte X a one-hot usando categorías aprendidas | En train y test | `ohe.transform(X_test)` |
| `fit_transform(X)` | fit + transform en un solo paso | Solo en datos de entrenamiento | `ohe.fit_transform(X_train)` |
| `inverse_transform(X)` | Convierte one-hot de vuelta a categorías | Para interpretar resultados | `ohe.inverse_transform(X_encoded)` |
| `get_feature_names_out()` | Obtiene nombres de las columnas generadas | Para crear DataFrames descriptivos | `ohe.get_feature_names_out()` |

---

## Parámetros Principales

### Tabla de parámetros

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `categories` | 'auto'/list | 'auto' | Categorías por feature. 'auto' las detecta automáticamente |
| `drop` | None/'first'/'if_binary'/array | None | Elimina categorías para evitar multicolinealidad |
| `sparse_output` | bool | True | Si True, devuelve matriz sparse (ahorra memoria) |
| `dtype` | dtype | np.float64 | Tipo de dato de la salida |
| `handle_unknown` | 'error'/'ignore'/'infrequent_if_exist' | 'error' | Cómo manejar categorías desconocidas en test |
| `min_frequency` | int/float | None | Agrupa categorías poco frecuentes |
| `max_categories` | int | None | Limita número máximo de categorías |

### Ejemplos de parámetros

```python
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import pandas as pd

# Datos de ejemplo
data = np.array([
    ['Madrid', 'S'],
    ['Barcelona', 'M'],
    ['Valencia', 'L'],
    ['Madrid', 'S'],
    ['Sevilla', 'M'],
    ['Barcelona', 'L']
])

print("="*60)
print("1. sparse_output=False (devuelve array denso)")
print("="*60)
ohe1 = OneHotEncoder(sparse_output=False)
encoded1 = ohe1.fit_transform(data)
print("Tipo:", type(encoded1))
print("Forma:", encoded1.shape)
print(encoded1)

print("\n" + "="*60)
print("2. sparse_output=True (devuelve matriz sparse)")
print("="*60)
ohe2 = OneHotEncoder(sparse_output=True)
encoded2 = ohe2.fit_transform(data)
print("Tipo:", type(encoded2))
print("Forma:", encoded2.shape)
print("Representación sparse:")
print(encoded2)
print("\nConvertido a denso:")
print(encoded2.toarray())

print("\n" + "="*60)
print("3. drop='first' (elimina primera categoría)")
print("="*60)
ohe3 = OneHotEncoder(sparse_output=False, drop='first')
encoded3 = ohe3.fit_transform(data)
print("Sin drop:", ohe1.get_feature_names_out())
print("Con drop='first':", ohe3.get_feature_names_out())
print("Reducción de columnas:", len(ohe1.get_feature_names_out()), "→", len(ohe3.get_feature_names_out()))

print("\n" + "="*60)
print("4. handle_unknown='ignore' (ignora categorías nuevas)")
print("="*60)
train = np.array([['Madrid'], ['Barcelona'], ['Valencia']])
test = np.array([['Madrid'], ['Tokio'], ['Barcelona']])

ohe4 = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
ohe4.fit(train)
test_encoded = ohe4.transform(test)
print("Test con categoría desconocida 'Tokio':")
print(test_encoded)
print("\n'Tokio' se codifica como [0, 0, 0] (todas las columnas en 0)")

print("\n" + "="*60)
print("5. min_frequency (agrupa categorías poco frecuentes)")
print("="*60)
data_freq = np.array([
    ['A'], ['A'], ['A'], ['A'], ['A'],  # 5 veces
    ['B'], ['B'],                         # 2 veces
    ['C'],                                # 1 vez
    ['D']                                 # 1 vez
])

ohe5 = OneHotEncoder(sparse_output=False, min_frequency=3, handle_unknown='ignore')
encoded5 = ohe5.fit_transform(data_freq)
print("Categorías originales:", np.unique(data_freq))
print("Categorías después de min_frequency=3:", ohe5.categories_)
print("Features generados:", ohe5.get_feature_names_out())
print("\nB, C, D se agrupan en 'infrequent_sklearn' porque aparecen < 3 veces")

print("\n" + "="*60)
print("6. dtype (tipo de dato de salida)")
print("="*60)
ohe6 = OneHotEncoder(sparse_output=False, dtype=np.uint8)
encoded6 = ohe6.fit_transform(data[:, :1])
print("Tipo de dato:", encoded6.dtype)
print("Memoria usada (uint8):", encoded6.nbytes, "bytes")

ohe7 = OneHotEncoder(sparse_output=False, dtype=np.float64)
encoded7 = ohe7.fit_transform(data[:, :1])
print("Tipo de dato:", encoded7.dtype)
print("Memoria usada (float64):", encoded7.nbytes, "bytes")
print("Ahorro de memoria:", (1 - encoded6.nbytes/encoded7.nbytes)*100, "%")
```

---

## Casos Prácticos

### Caso 1: Preparación básica de datos

```python
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd

# Dataset de ejemplo
df = pd.DataFrame({
    'ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Madrid', 'Barcelona', 
               'Valencia', 'Madrid', 'Barcelona', 'Valencia', 'Madrid'],
    'género': ['M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'F'],
    'edad': [25, 30, 35, 28, 42, 38, 29, 45, 33, 27],
    'compra': [1, 0, 1, 1, 0, 1, 0, 1, 1, 0]
})

print("Dataset original:")
print(df)

# Separar features categóricas y numéricas
X_cat = df[['ciudad', 'género']].values
X_num = df[['edad']].values
y = df['compra'].values

# Codificar variables categóricas
ohe = OneHotEncoder(sparse_output=False, drop='first')
X_cat_encoded = ohe.fit_transform(X_cat)

# Combinar con variables numéricas
X_combined = np.hstack([X_cat_encoded, X_num])

print("\nFeatures codificadas:")
print("Nombres:", ohe.get_feature_names_out(['ciudad', 'género']).tolist() + ['edad'])
print("Forma:", X_combined.shape)
print(X_combined[:5])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X_combined, y, test_size=0.3, random_state=42
)

# Entrenar modelo
modelo = LogisticRegression()
modelo.fit(X_train, y_train)

# Evaluar
y_pred = modelo.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {accuracy:.2f}")
```

### Caso 2: Convertir salida a DataFrame

```python
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np

# Datos
df = pd.DataFrame({
    'ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Madrid'],
    'género': ['M', 'F', 'M', 'F'],
    'edad': [25, 30, 35, 28]
})

# Codificar solo columnas categóricas
cat_columns = ['ciudad', 'género']
X_cat = df[cat_columns].values

ohe = OneHotEncoder(sparse_output=False, drop='first')
X_encoded = ohe.fit_transform(X_cat)

# Crear DataFrame con nombres descriptivos
feature_names = ohe.get_feature_names_out(cat_columns)
df_encoded = pd.DataFrame(X_encoded, columns=feature_names)

# Añadir columnas numéricas
df_encoded['edad'] = df['edad'].values

print("DataFrame codificado:")
print(df_encoded)
```

### Caso 3: Múltiples columnas categóricas

```python
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

# Dataset más complejo
df = pd.DataFrame({
    'ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Madrid', 'Sevilla'],
    'color': ['rojo', 'azul', 'verde', 'rojo', 'azul'],
    'tamaño': ['S', 'M', 'L', 'S', 'M'],
    'precio': [100, 200, 150, 120, 180],
    'compra': [1, 0, 1, 1, 0]
})

# Identificar columnas por tipo
cat_columns = ['ciudad', 'color', 'tamaño']
num_columns = ['precio']

# Crear ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), cat_columns),
        ('num', 'passthrough', num_columns)
    ]
)

# Separar X e y
X = df.drop('compra', axis=1)
y = df['compra']

# Aplicar transformación
X_transformed = preprocessor.fit_transform(X)

print("Forma original:", X.shape)
print("Forma transformada:", X_transformed.shape)
print("\nNombres de features:")
print(preprocessor.get_feature_names_out())
```

### Caso 4: Manejo de valores faltantes

```python
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import numpy as np
import pandas as pd

# Datos con NaN
df = pd.DataFrame({
    'ciudad': ['Madrid', 'Barcelona', np.nan, 'Valencia', 'Madrid'],
    'género': ['M', 'F', 'M', np.nan, 'F']
})

print("Datos originales con NaN:")
print(df)

# Opción 1: Imputar antes de codificar
imputer = SimpleImputer(strategy='constant', fill_value='Desconocido')
ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')

df_imputed = pd.DataFrame(
    imputer.fit_transform(df),
    columns=df.columns
)
df_encoded = ohe.fit_transform(df_imputed)

print("\nOpción 1 - Imputar con 'Desconocido':")
print(df_encoded)
print("Features:", ohe.get_feature_names_out())

# Opción 2: Pipeline
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(sparse_output=False))
])

df_pipeline = pipeline.fit_transform(df)
print("\nOpción 2 - Pipeline con imputación por moda:")
print(df_pipeline)
```

---

## Comparación: OneHotEncoder vs get_dummies

### Tabla comparativa detallada

| Característica | OneHotEncoder | pd.get_dummies() |
|----------------|---------------|------------------|
| **Librería** | sklearn | pandas |
| **Sistema fit/transform** | Sí (control train/test) | No |
| **Manejo categorías desconocidas** | Sí (handle_unknown) | No (da error o ignora) |
| **Salida** | Array numpy (o DataFrame manual) | DataFrame con nombres |
| **Matriz sparse** | Sí (por defecto) | No |
| **Integración Pipeline** | Nativa | No |
| **Complejidad** | Más complejo | Muy simple |
| **Control producción** | Excelente | Limitado |
| **Velocidad** | Rápida | Rápida |
| **Nombrado columnas** | Manual (get_feature_names_out) | Automático y descriptivo |
| **drop (multicolinealidad)** | Sí (drop='first') | Sí (drop_first=True) |
| **min_frequency** | Sí | No |
| **max_categories** | Sí | No |

### Ejemplo lado a lado

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder

# Datos
df = pd.DataFrame({
    'ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Madrid'],
    'precio': [100, 200, 150, 120]
})

print("="*60)
print("MÉTODO 1: pd.get_dummies()")
print("="*60)

df_dummies = pd.get_dummies(df, columns=['ciudad'], drop_first=True)
print(df_dummies)
print("\nTipo de salida:", type(df_dummies))
print("Columnas:", df_dummies.columns.tolist())

print("\n" + "="*60)
print("MÉTODO 2: sklearn OneHotEncoder")
print("="*60)

ohe = OneHotEncoder(sparse_output=False, drop='first')
ciudad_encoded = ohe.fit_transform(df[['ciudad']])

# Crear DataFrame manualmente
feature_names = ohe.get_feature_names_out(['ciudad'])
df_ohe = pd.DataFrame(ciudad_encoded, columns=feature_names)
df_ohe['precio'] = df['precio'].values

print(df_ohe)
print("\nTipo de salida:", type(df_ohe))
print("Columnas:", df_ohe.columns.tolist())

print("\n" + "="*60)
print("COMPARACIÓN DE RESULTADOS")
print("="*60)
print("Son iguales?", df_dummies.equals(df_ohe))
print("Valores iguales?", np.allclose(df_dummies.values, df_ohe.values))
```

### Cuándo usar cada uno

**Usar OneHotEncoder cuando:**
- Construyes pipelines de machine learning
- Necesitas desplegar modelo en producción
- Debes manejar categorías desconocidas en test
- Trabajas con datos muy grandes (sparse matrices)
- Quieres usar ColumnTransformer
- Necesitas reproducibilidad exacta entre train/test
- Integración con sklearn es prioritaria

**Usar pd.get_dummies() cuando:**
- Análisis exploratorio rápido
- Prototipado en Jupyter notebooks
- Dataset pequeño/mediano
- No necesitas desplegar en producción
- Prefieres simplicidad sobre control
- Solo trabajas en pandas (sin sklearn)

---

## Integración con Pipelines

### Pipeline básico

```python
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd

# Dataset
df = pd.DataFrame({
    'ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Madrid', 'Sevilla'] * 20,
    'género': ['M', 'F', 'M', 'F', 'M'] * 20,
    'edad': [25, 30, 35, 28, 42] * 20,
    'salario': [30000, 45000, 50000, 35000, 55000] * 20,
    'compra': [1, 0, 1, 1, 0] * 20
})

# Separar features y target
X = df.drop('compra', axis=1)
y = df['compra']

# Definir columnas
cat_features = ['ciudad', 'género']
num_features = ['edad', 'salario']

# Crear preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), cat_features),
        ('num', StandardScaler(), num_features)
    ]
)

# Crear pipeline completo
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Entrenar
pipeline.fit(X_train, y_train)

# Predecir
y_pred = pipeline.predict(X_test)

# Evaluar
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Ver transformaciones
print("\nFeature names después del preprocessor:")
print(pipeline.named_steps['preprocessor'].get_feature_names_out())
```

### Pipeline con múltiples transformadores

```python
from sklearn.preprocessing import OneHotEncoder, StandardScaler, FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np

# Dataset
df = pd.DataFrame({
    'ciudad': ['Madrid', 'Barcelona', 'Valencia'] * 30,
    'edad': np.random.randint(18, 65, 90),
    'salario': np.random.randint(20000, 80000, 90),
    'compra': np.random.choice([0, 1], 90)
})

# Función personalizada para crear feature de interacción
def crear_ratio_edad_salario(X):
    return X[:, 0:1] / (X[:, 1:2] / 1000)

# Definir transformadores
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(drop='first'), ['ciudad']),
        ('num', StandardScaler(), ['edad', 'salario'])
    ],
    remainder='passthrough'
)

# Pipeline completo
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(max_iter=1000))
])

# Separar y entrenar
X = df.drop('compra', axis=1)
y = df['compra']

pipeline.fit(X, y)

# Predecir en nuevos datos
nuevos_datos = pd.DataFrame({
    'ciudad': ['Madrid', 'Sevilla'],
    'edad': [30, 35],
    'salario': [40000, 50000]
})

predicciones = pipeline.predict(nuevos_datos)
print("Predicciones:", predicciones)
```

### Pipeline con GridSearchCV

```python
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
import pandas as pd
import numpy as np

# Dataset
np.random.seed(42)
df = pd.DataFrame({
    'ciudad': np.random.choice(['Madrid', 'Barcelona', 'Valencia', 'Sevilla'], 200),
    'género': np.random.choice(['M', 'F'], 200),
    'edad': np.random.randint(18, 65, 200),
    'compra': np.random.choice([0, 1], 200)
})

# Preparar datos
X = df.drop('compra', axis=1)
y = df['compra']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Crear pipeline
preprocessor = ColumnTransformer([
    ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), ['ciudad', 'género']),
    ('num', 'passthrough', ['edad'])
])

pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

# Definir grid de parámetros
param_grid = {
    'preprocessor__cat__drop': [None, 'first'],
    'classifier__n_estimators': [50, 100, 200],
    'classifier__max_depth': [5, 10, None]
}

# GridSearch
grid_search = GridSearchCV(
    pipeline,
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)

# Entrenar
grid_search.fit(X_train, y_train)

# Resultados
print("Mejores parámetros:")
print(grid_search.best_params_)
print(f"\nMejor score: {grid_search.best_score_:.3f}")
print(f"Score en test: {grid_search.score(X_test, y_test):.3f}")
```

---

## Ejemplo Completo con Train/Test

### Implementación correcta

```python
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import numpy as np

# Dataset de ejemplo
np.random.seed(42)
df = pd.DataFrame({
    'ciudad': np.random.choice(['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao'], 500),
    'género': np.random.choice(['M', 'F'], 500),
    'nivel_educación': np.random.choice(['Primaria', 'Secundaria', 'Universidad'], 500),
    'edad': np.random.randint(18, 65, 500),
    'salario': np.random.randint(20000, 80000, 500),
    'compra': np.random.choice([0, 1], 500)
})

print("Dataset original:")
print(df.head(10))
print(f"\nForma: {df.shape}")
print(f"\nDistribución de target:\n{df['compra'].value_counts()}")

# Separar features y target
X = df.drop('compra', axis=1)
y = df['compra']

# Identificar columnas por tipo
cat_columns = ['ciudad', 'género', 'nivel_educación']
num_columns = ['edad', 'salario']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n{'='*60}")
print("CODIFICACIÓN DE VARIABLES CATEGÓRICAS")
print("="*60)

# Crear encoder
ohe = OneHotEncoder(
    drop='first',              # Evitar multicolinealidad
    sparse_output=False,        # Devolver array denso
    handle_unknown='ignore'     # Manejar categorías nuevas
)

# IMPORTANTE: fit solo en train
X_train_cat = ohe.fit_transform(X_train[cat_columns])
X_train_num = X_train[num_columns].values

# Transform en test (sin fit)
X_test_cat = ohe.transform(X_test[cat_columns])
X_test_num = X_test[num_columns].values

# Combinar categóricas y numéricas
X_train_final = np.hstack([X_train_cat, X_train_num])
X_test_final = np.hstack([X_test_cat, X_test_num])

print(f"\nForma train: {X_train_final.shape}")
print(f"Forma test: {X_test_final.shape}")

# Ver nombres de features
feature_names = list(ohe.get_feature_names_out(cat_columns)) + num_columns
print(f"\nNúmero total de features: {len(feature_names)}")
print(f"\nPrimeros 10 features: {feature_names[:10]}")

# Crear DataFrame para mejor visualización
X_train_df = pd.DataFrame(X_train_final, columns=feature_names)
X_test_df = pd.DataFrame(X_test_final, columns=feature_names)

print("\nPrimeras filas de train codificado:")
print(X_train_df.head())

print(f"\n{'='*60}")
print("ENTRENAMIENTO Y EVALUACIÓN")
print("="*60)

# Entrenar modelo
modelo = GradientBoostingClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)

modelo.fit(X_train_final, y_train)

# Predicciones
y_train_pred = modelo.predict(X_train_final)
y_test_pred = modelo.predict(X_test_final)

# Evaluación
print("\nAccuracy:")
print(f"  Train: {modelo.score(X_train_final, y_train):.3f}")
print(f"  Test:  {modelo.score(X_test_final, y_test):.3f}")

print("\nClassification Report (Test):")
print(classification_report(y_test, y_test_pred))

print("\nConfusion Matrix (Test):")
print(confusion_matrix(y_test, y_test_pred))

print(f"\n{'='*60}")
print("FEATURE IMPORTANCE")
print("="*60)

# Feature importance
importances = pd.DataFrame({
    'feature': feature_names,
    'importance': modelo.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 10 features más importantes:")
print(importances.head(10))

print(f"\n{'='*60}")
print("PREDICCIÓN EN NUEVOS DATOS")
print("="*60)

# Nuevos datos (con categoría desconocida)
nuevos_datos = pd.DataFrame({
    'ciudad': ['Madrid', 'Toledo', 'Barcelona'],  # Toledo no está en train
    'género': ['M', 'F', 'M'],
    'nivel_educación': ['Universidad', 'Secundaria', 'Primaria'],
    'edad': [30, 45, 25],
    'salario': [45000, 35000, 30000]
})

print("\nNuevos datos:")
print(nuevos_datos)

# Transformar nuevos datos
nuevos_cat = ohe.transform(nuevos_datos[cat_columns])
nuevos_num = nuevos_datos[num_columns].values
nuevos_final = np.hstack([nuevos_cat, nuevos_num])

# Predecir
predicciones = modelo.predict(nuevos_final)
probabilidades = modelo.predict_proba(nuevos_final)

print("\nPredicciones:")
for i, (pred, proba) in enumerate(zip(predicciones, probabilidades)):
    print(f"  Fila {i}: Clase {pred} (probabilidad: {proba[pred]:.3f})")

print("\nNota: 'Toledo' (categoría desconocida) fue manejado correctamente")
print("      gracias a handle_unknown='ignore'")
```

### Guardar y cargar encoder

```python
import pickle
from sklearn.preprocessing import OneHotEncoder
import numpy as np

# Entrenar encoder
data_train = np.array([['Madrid'], ['Barcelona'], ['Valencia']])
ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
ohe.fit(data_train)

# Guardar encoder
with open('ohe_encoder.pkl', 'wb') as f:
    pickle.dump(ohe, f)

print("Encoder guardado en 'ohe_encoder.pkl'")

# Simular nueva sesión/despliegue
print("\n" + "="*60)
print("NUEVA SESIÓN - Cargando encoder...")
print("="*60)

# Cargar encoder
with open('ohe_encoder.pkl', 'rb') as f:
    ohe_loaded = pickle.load(f)

# Usar en nuevos datos
data_test = np.array([['Barcelona'], ['Sevilla'], ['Madrid']])
test_encoded = ohe_loaded.transform(data_test)

print("\nCategorías aprendidas:", ohe_loaded.categories_)
print("\nNuevos datos transformados:")
print(test_encoded)
```

---

## Problemas Comunes y Soluciones

### Problema 1: ValueError con categorías desconocidas

**Problema:**
```python
from sklearn.preprocessing import OneHotEncoder
import numpy as np

train = np.array([['Madrid'], ['Barcelona']])
test = np.array([['Madrid'], ['Sevilla']])  # Sevilla no está en train

ohe = OneHotEncoder()
ohe.fit(train)

# Esto da error
try:
    test_encoded = ohe.transform(test)
except ValueError as e:
    print(f"Error: {e}")
```

**Salida:**
```
Error: Found unknown categories ['Sevilla'] in column 0 during transform
```

**Solución:**
```python
# Usar handle_unknown='ignore'
ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
ohe.fit(train)
test_encoded = ohe.transform(test)

print("Test codificado (Sevilla se convierte en [0, 0]):")
print(test_encoded)
```

### Problema 2: Input debe ser 2D

**Problema:**
```python
from sklearn.preprocessing import OneHotEncoder
import numpy as np

# Error: input es 1D
data = np.array(['Madrid', 'Barcelona', 'Valencia'])
ohe = OneHotEncoder()

try:
    encoded = ohe.fit_transform(data)
except ValueError as e:
    print(f"Error: {e}")
```

**Solución:**
```python
# Reshape a 2D
data_2d = data.reshape(-1, 1)  # O usar np.array([...]).reshape(-1, 1)
encoded = ohe.fit_transform(data_2d)

print("Forma correcta:", data_2d.shape)
print("Codificado:", encoded.toarray())

# Alternativa: usar doble corchete al crear array
data_2d_alt = np.array([['Madrid'], ['Barcelona'], ['Valencia']])
```

### Problema 3: Convertir sparse a denso

**Problema:**
```python
from sklearn.preprocessing import OneHotEncoder
import numpy as np

data = np.array([['Madrid'], ['Barcelona'], ['Valencia']])
ohe = OneHotEncoder()  # sparse_output=True por defecto
encoded = ohe.fit_transform(data)

print("Tipo:", type(encoded))  # <class 'scipy.sparse._csr.csr_matrix'>

# Esto no funciona con pandas
try:
    import pandas as pd
    df = pd.DataFrame(encoded)  # Crea DataFrame extraño
    print(df)
except Exception as e:
    print(f"Problema: {e}")
```

**Solución:**
```python
# Opción 1: sparse_output=False
ohe1 = OneHotEncoder(sparse_output=False)
encoded1 = ohe1.fit_transform(data)
print("Tipo (opción 1):", type(encoded1))

# Opción 2: .toarray()
ohe2 = OneHotEncoder()
encoded2 = ohe2.fit_transform(data).toarray()
print("Tipo (opción 2):", type(encoded2))

# Crear DataFrame correctamente
import pandas as pd
df = pd.DataFrame(encoded1, columns=ohe1.get_feature_names_out())
print("\nDataFrame:")
print(df)
```

### Problema 4: Alta cardinalidad (muchas categorías)

**Problema:**
```python
import numpy as np
from sklearn.preprocessing import OneHotEncoder

# Columna con 1000 categorías únicas
data = np.array([[f'cat_{i}'] for i in range(1000)])
ohe = OneHotEncoder(sparse_output=False)
encoded = ohe.fit_transform(data)

print(f"Forma de salida: {encoded.shape}")  # (1000, 1000)
print("Problema: demasiadas columnas")
```

**Soluciones:**
```python
# Solución 1: max_categories (sklearn >= 1.2)
from sklearn.preprocessing import OneHotEncoder
import numpy as np

np.random.seed(42)
data = np.array([[f'cat_{i}'] for i in np.random.randint(0, 100, 500)])

ohe = OneHotEncoder(
    max_categories=10,
    sparse_output=False,
    handle_unknown='infrequent_if_exist'
)
encoded = ohe.fit_transform(data)
print(f"Con max_categories=10: {encoded.shape}")

# Solución 2: min_frequency
ohe2 = OneHotEncoder(
    min_frequency=10,
    sparse_output=False,
    handle_unknown='infrequent_if_exist'
)
encoded2 = ohe2.fit_transform(data)
print(f"Con min_frequency=10: {encoded2.shape}")

# Solución 3: Usar otros encoders
from category_encoders import TargetEncoder
# Target encoding mantiene 1 columna
```

### Problema 5: Nombres de features no descriptivos

**Problema:**
```python
from sklearn.preprocessing import OneHotEncoder
import numpy as np

data = np.array([['Madrid', 'M'], ['Barcelona', 'F']])
ohe = OneHotEncoder(sparse_output=False)
encoded = ohe.fit_transform(data)

# Nombres por defecto no son descriptivos
print("Nombres por defecto:", ohe.get_feature_names_out())
# Output: ['x0_Barcelona' 'x0_Madrid' 'x1_F' 'x1_M']
```

**Solución:**
```python
# Pasar nombres de columnas
feature_names = ohe.get_feature_names_out(['ciudad', 'género'])
print("Nombres descriptivos:", feature_names)
# Output: ['ciudad_Barcelona' 'ciudad_Madrid' 'género_F' 'género_M']

# Crear DataFrame
import pandas as pd
df = pd.DataFrame(encoded, columns=feature_names)
print("\nDataFrame con nombres descriptivos:")
print(df)
```

### Problema 6: fit en test (data leakage)

**Problema:**
```python
from sklearn.preprocessing import OneHotEncoder
import numpy as np

train = np.array([['Madrid'], ['Barcelona'], ['Valencia']])
test = np.array([['Madrid'], ['Barcelona'], ['Sevilla']])

# INCORRECTO: fit en ambos
ohe_train = OneHotEncoder(sparse_output=False)
ohe_test = OneHotEncoder(sparse_output=False)

train_encoded = ohe_train.fit_transform(train)
test_encoded = ohe_test.fit_transform(test)  # ERROR: no hacer fit en test

print("Train shape:", train_encoded.shape)  # (3, 3)
print("Test shape:", test_encoded.shape)     # (3, 3)
print("Problema: diferentes columnas (Sevilla vs Valencia)")
```

**Solución:**
```python
# CORRECTO: fit solo en train
ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')

train_encoded = ohe.fit_transform(train)
test_encoded = ohe.transform(test)  # Solo transform

print("Train shape:", train_encoded.shape)  # (3, 3)
print("Test shape:", test_encoded.shape)     # (3, 3)
print("Correcto: mismas columnas, Sevilla se ignora")
```

---

## Resumen

### Ventajas de OneHotEncoder

- Control preciso con fit/transform
- Maneja categorías desconocidas (handle_unknown)
- Integración perfecta con sklearn Pipelines
- Matrices sparse para eficiencia de memoria
- Parámetros avanzados (min_frequency, max_categories)
- Ideal para producción y despliegue
- Reproducibilidad garantizada entre train/test

### Desventajas de OneHotEncoder

- Más complejo que pd.get_dummies()
- Requiere conversión manual para DataFrames descriptivos
- Sintaxis más verbosa
- Curva de aprendizaje mayor

### Mejores prácticas

1. **Siempre fit solo en train:** `ohe.fit(X_train)` luego `ohe.transform(X_test)`
2. **Usar handle_unknown='ignore':** Para manejar categorías nuevas en producción
3. **Usar drop='first':** Para evitar multicolinealidad en regresión lineal
4. **sparse_output=False:** Si vas a crear DataFrames o trabajar con arrays pequeños
5. **Guardar encoder:** Con pickle para usar en producción
6. **Usar Pipelines:** Para flujos de trabajo más limpios
7. **Documentar categorías:** Guardar `ohe.categories_` para referencia

### Código mínimo funcional

```python
from sklearn.preprocessing import OneHotEncoder
import numpy as np

# Datos
X_train = np.array([['Madrid'], ['Barcelona'], ['Valencia']])
X_test = np.array([['Madrid'], ['Sevilla']])

# Crear y entrenar
ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
X_train_enc = ohe.fit_transform(X_train)
X_test_enc = ohe.transform(X_test)
```

### Con Pipeline (recomendado para producción)

```python
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

# Pipeline completo
preprocessor = ColumnTransformer([
    ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), ['col_cat']),
    ('num', 'passthrough', ['col_num'])
])

pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier())
])

# Entrenar y predecir
pipeline.fit(X_train, y_train)
predictions = pipeline.predict(X_test)
```

### Cuándo usar OneHotEncoder

**Casos ideales:**
- Modelos en producción
- Pipelines de sklearn
- Necesitas manejar categorías desconocidas
- Trabajas con datos grandes (sparse matrices)
- Integración con GridSearchCV
- Reproducibilidad crítica

**Alternativas a considerar:**
- **pd.get_dummies():** Para análisis exploratorio rápido
- **OrdinalEncoder:** Para categorías con orden natural
- **TargetEncoder:** Para alta cardinalidad
- **LabelEncoder:** Solo para variable objetivo

### Parámetros más importantes

```python
OneHotEncoder(
    categories='auto',           # Detecta automáticamente
    drop='first',                # Evita multicolinealidad
    sparse_output=False,         # Array denso (más fácil de usar)
    handle_unknown='ignore',     # Ignora categorías nuevas
    min_frequency=None,          # Agrupa categorías poco frecuentes
    max_categories=None,         # Limita número de categorías
    dtype=np.float64             # Tipo de dato de salida
)
```

---

## Referencias

- Documentación oficial: [sklearn.preprocessing.OneHotEncoder](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html)
- User Guide: [Encoding categorical features](https://scikit-learn.org/stable/modules/preprocessing.html#encoding-categorical-features)
- Tutorial Pipeline: [Column Transformer with Mixed Types](https://scikit-learn.org/stable/auto_examples/compose/plot_column_transformer_mixed_types.html)
- Comparación encoders: [Category Encoders](https://contrib.scikit-learn.org/category_encoders/)
