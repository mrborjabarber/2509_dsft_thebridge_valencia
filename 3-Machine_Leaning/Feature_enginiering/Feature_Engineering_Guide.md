# Feature Engineering - Guía Completa

## Índice

1. [¿Qué es Feature Engineering?](#qué-es-feature-engineering)
2. [Importancia del Feature Engineering](#importancia-del-feature-engineering)
3. [Tipos de Features](#tipos-de-features)
4. [Técnicas Principales](#técnicas-principales)
5. [Feature Engineering para Variables Numéricas](#feature-engineering-para-variables-numéricas)
6. [Feature Engineering para Variables Categóricas](#feature-engineering-para-variables-categóricas)
7. [Feature Engineering para Fechas y Tiempo](#feature-engineering-para-fechas-y-tiempo)
8. [Feature Engineering para Texto](#feature-engineering-para-texto)
9. [Feature Engineering Avanzado](#feature-engineering-avanzado)
10. [Feature Selection](#feature-selection)
11. [Ejemplo Completo End-to-End](#ejemplo-completo-end-to-end)
12. [Mejores Prácticas](#mejores-prácticas)
13. [Errores Comunes](#errores-comunes)
14. [Resumen](#resumen)

---

## ¿Qué es Feature Engineering?

**Feature Engineering** es el proceso de usar conocimiento del dominio para crear, transformar o seleccionar variables (features) que mejoren el rendimiento de los modelos de machine learning.

### Definición

Es el arte y ciencia de:
- Crear nuevas features a partir de datos existentes
- Transformar features para que sean más útiles
- Seleccionar las features más relevantes
- Combinar múltiples features en nuevas representaciones

### Objetivo principal

Maximizar la información útil que los datos proporcionan al modelo, haciendo que los patrones sean más evidentes y fáciles de aprender.

---

## Importancia del Feature Engineering

### Por qué es importante

```
"Los datos y las features determinan el límite superior del rendimiento, 
mientras que los modelos y algoritmos solo se acercan a ese límite"
```

**Impacto en el modelo:**
- Un buen feature engineering puede mejorar la precisión en 10-30%
- Puede reducir el tiempo de entrenamiento significativamente
- Permite usar modelos más simples con mejores resultados
- Hace que los modelos sean más interpretables

### Ejemplo ilustrativo

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Datos sintéticos: predecir precio de casa
np.random.seed(42)
df = pd.DataFrame({
    'area_m2': np.random.randint(50, 300, 1000),
    'habitaciones': np.random.randint(1, 6, 1000),
    'antiguedad': np.random.randint(0, 50, 1000)
})

# Precio real tiene una relación no lineal
df['precio'] = (
    df['area_m2'] * 2000 + 
    df['habitaciones'] * 50000 + 
    (50 - df['antiguedad']) * 1000 +
    np.random.normal(0, 10000, 1000)
)

# Split
X = df.drop('precio', axis=1)
y = df['precio']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("="*60)
print("SIN FEATURE ENGINEERING")
print("="*60)

# Modelo básico
modelo1 = LinearRegression()
modelo1.fit(X_train, y_train)
y_pred1 = modelo1.predict(X_test)
r2_1 = r2_score(y_test, y_pred1)
rmse_1 = np.sqrt(mean_squared_error(y_test, y_pred1))

print(f"R2 Score: {r2_1:.4f}")
print(f"RMSE: {rmse_1:.2f}")

print("\n" + "="*60)
print("CON FEATURE ENGINEERING")
print("="*60)

# Crear nuevas features
def crear_features(df):
    df_new = df.copy()
    # Feature de interacción
    df_new['area_por_habitacion'] = df_new['area_m2'] / df_new['habitaciones']
    # Feature polinomial
    df_new['area_cuadrado'] = df_new['area_m2'] ** 2
    # Feature de edad de la casa
    df_new['es_nueva'] = (df_new['antiguedad'] < 5).astype(int)
    # Binning de área
    df_new['categoria_area'] = pd.cut(df_new['area_m2'], bins=[0, 100, 200, 300], labels=[0, 1, 2])
    return df_new

X_train_eng = crear_features(X_train)
X_test_eng = crear_features(X_test)

# Modelo con feature engineering
modelo2 = LinearRegression()
modelo2.fit(X_train_eng, y_train)
y_pred2 = modelo2.predict(X_test_eng)
r2_2 = r2_score(y_test, y_pred2)
rmse_2 = np.sqrt(mean_squared_error(y_test, y_pred2))

print(f"R2 Score: {r2_2:.4f}")
print(f"RMSE: {rmse_2:.2f}")

print("\n" + "="*60)
print("MEJORA")
print("="*60)
print(f"Mejora en R2: {(r2_2 - r2_1) / r2_1 * 100:.2f}%")
print(f"Reducción de RMSE: {(rmse_1 - rmse_2) / rmse_1 * 100:.2f}%")
```

---

## Tipos de Features

### Clasificación por naturaleza

```python
import pandas as pd

df = pd.DataFrame({
    # 1. Numéricas continuas
    'precio': [100.5, 200.3, 150.7],
    'temperatura': [23.5, 25.1, 22.8],
    
    # 2. Numéricas discretas
    'cantidad': [1, 5, 3],
    'habitaciones': [2, 3, 4],
    
    # 3. Categóricas nominales (sin orden)
    'color': ['rojo', 'azul', 'verde'],
    'ciudad': ['Madrid', 'Barcelona', 'Valencia'],
    
    # 4. Categóricas ordinales (con orden)
    'educacion': ['Primaria', 'Secundaria', 'Universidad'],
    'tamaño': ['S', 'M', 'L'],
    
    # 5. Binarias
    'es_cliente': [True, False, True],
    'tiene_descuento': [1, 0, 1],
    
    # 6. Fecha/Tiempo
    'fecha_compra': pd.to_datetime(['2024-01-15', '2024-02-20', '2024-03-10']),
    
    # 7. Texto
    'descripcion': ['producto nuevo', 'oferta especial', 'liquidación']
})

print("Tipos de features en el dataset:")
print(df.dtypes)
```

### Clasificación por origen

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **Raw Features** | Features originales sin procesar | edad, precio, ciudad |
| **Derived Features** | Creadas a partir de otras features | edad_en_decadas, precio_log |
| **Interaction Features** | Combinación de múltiples features | area * habitaciones |
| **Domain-specific Features** | Basadas en conocimiento experto | IMC = peso/(altura^2) |
| **Aggregated Features** | Estadísticos de agrupaciones | promedio_ventas_por_ciudad |

---

## Técnicas Principales

### Resumen de técnicas

| Categoría | Técnicas |
|-----------|----------|
| **Transformación** | Scaling, Normalización, Log, Box-Cox, Yeo-Johnson |
| **Codificación** | One-Hot, Label, Ordinal, Target, Frequency |
| **Creación** | Polinomiales, Interacciones, Binning, Agregaciones |
| **Extracción** | Fechas, Texto (TF-IDF, Word2Vec), Imágenes |
| **Reducción** | PCA, Feature Selection, Eliminación de correlacionadas |
| **Manejo de Missing** | Imputación, Indicador de faltante |

---

## Feature Engineering para Variables Numéricas

### 1. Escalado y Normalización

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# Datos de ejemplo
df = pd.DataFrame({
    'salario': [30000, 45000, 60000, 35000, 100000],
    'edad': [25, 30, 35, 28, 45],
    'años_experiencia': [2, 5, 10, 3, 20]
})

print("Datos originales:")
print(df)
print(f"\nEstadísticas:\n{df.describe()}")

# StandardScaler (z-score normalization)
scaler_std = StandardScaler()
df_std = pd.DataFrame(
    scaler_std.fit_transform(df),
    columns=[f'{col}_std' for col in df.columns]
)
print("\n" + "="*60)
print("StandardScaler (media=0, std=1):")
print(df_std)

# MinMaxScaler (rango 0-1)
scaler_minmax = MinMaxScaler()
df_minmax = pd.DataFrame(
    scaler_minmax.fit_transform(df),
    columns=[f'{col}_minmax' for col in df.columns]
)
print("\n" + "="*60)
print("MinMaxScaler (rango 0-1):")
print(df_minmax)

# RobustScaler (robusto a outliers)
scaler_robust = RobustScaler()
df_robust = pd.DataFrame(
    scaler_robust.fit_transform(df),
    columns=[f'{col}_robust' for col in df.columns]
)
print("\n" + "="*60)
print("RobustScaler (usa mediana y cuartiles):")
print(df_robust)
```

### 2. Transformaciones No Lineales

```python
import numpy as np
import pandas as pd
from scipy import stats

# Datos con distribución sesgada
np.random.seed(42)
df = pd.DataFrame({
    'ingreso': np.random.exponential(50000, 1000),
    'precio_casa': np.random.lognormal(12, 0.5, 1000),
    'transacciones': np.random.poisson(5, 1000)
})

print("Datos originales (primeras filas):")
print(df.head())
print(f"\nSkewness:\n{df.skew()}")

# Log transform
df['ingreso_log'] = np.log1p(df['ingreso'])  # log(1 + x)
df['precio_log'] = np.log1p(df['precio_casa'])

# Square root transform
df['transacciones_sqrt'] = np.sqrt(df['transacciones'])

# Box-Cox transform (requiere valores positivos)
df['ingreso_boxcox'], lambda_param = stats.boxcox(df['ingreso'])

print("\n" + "="*60)
print("Después de transformaciones:")
print(df[['ingreso_log', 'precio_log', 'transacciones_sqrt', 'ingreso_boxcox']].head())
print(f"\nSkewness después:\n{df[['ingreso_log', 'precio_log', 'transacciones_sqrt']].skew()}")
```

### 3. Binning (Discretización)

```python
import pandas as pd
import numpy as np

# Datos
df = pd.DataFrame({
    'edad': [18, 25, 35, 45, 55, 65, 75, 22, 38, 50],
    'salario': [25000, 35000, 55000, 75000, 65000, 45000, 35000, 30000, 60000, 70000]
})

print("Datos originales:")
print(df)

# Binning con rangos iguales
df['edad_bins_equal'] = pd.cut(
    df['edad'], 
    bins=4, 
    labels=['Joven', 'Adulto', 'Maduro', 'Senior']
)

# Binning con rangos personalizados
df['edad_bins_custom'] = pd.cut(
    df['edad'],
    bins=[0, 25, 40, 60, 100],
    labels=['18-25', '26-40', '41-60', '60+']
)

# Binning por cuantiles (igual cantidad en cada bin)
df['salario_quartiles'] = pd.qcut(
    df['salario'],
    q=4,
    labels=['Q1', 'Q2', 'Q3', 'Q4']
)

print("\n" + "="*60)
print("Después de binning:")
print(df)

# Convertir a one-hot
df_encoded = pd.get_dummies(df, columns=['edad_bins_equal', 'salario_quartiles'])
print("\n" + "="*60)
print("Con one-hot encoding:")
print(df_encoded.head())
```

### 4. Features Polinomiales

```python
from sklearn.preprocessing import PolynomialFeatures
import pandas as pd
import numpy as np

# Datos
df = pd.DataFrame({
    'x1': [1, 2, 3, 4, 5],
    'x2': [2, 4, 6, 8, 10]
})

print("Features originales:")
print(df)

# Crear features polinomiales de grado 2
poly = PolynomialFeatures(degree=2, include_bias=False)
features_poly = poly.fit_transform(df)

# Nombres de las nuevas features
feature_names = poly.get_feature_names_out(['x1', 'x2'])

df_poly = pd.DataFrame(features_poly, columns=feature_names)
print("\n" + "="*60)
print("Features polinomiales (grado 2):")
print(df_poly)
print("\nIncluye: x1, x2, x1^2, x1*x2, x2^2")
```

### 5. Features de Interacción

```python
import pandas as pd
import numpy as np

# Datos de viviendas
df = pd.DataFrame({
    'area_m2': [80, 120, 150, 200],
    'habitaciones': [2, 3, 4, 5],
    'baños': [1, 2, 2, 3],
    'precio': [150000, 220000, 280000, 350000]
})

print("Datos originales:")
print(df)

# Features de interacción
df['area_por_habitacion'] = df['area_m2'] / df['habitaciones']
df['habitaciones_x_baños'] = df['habitaciones'] * df['baños']
df['densidad'] = df['habitaciones'] / df['area_m2']
df['area_cuadrado'] = df['area_m2'] ** 2

print("\n" + "="*60)
print("Con features de interacción:")
print(df)

# Estas features pueden capturar relaciones no lineales
```

### 6. Agregaciones y Estadísticos

```python
import pandas as pd
import numpy as np

# Datos de transacciones
df = pd.DataFrame({
    'cliente_id': [1, 1, 1, 2, 2, 3, 3, 3, 3],
    'monto': [100, 150, 200, 300, 250, 50, 75, 100, 125],
    'fecha': pd.date_range('2024-01-01', periods=9, freq='D')
})

print("Transacciones originales:")
print(df)

# Crear features agregadas por cliente
features_cliente = df.groupby('cliente_id').agg({
    'monto': ['sum', 'mean', 'std', 'min', 'max', 'count'],
}).reset_index()

# Aplanar nombres de columnas
features_cliente.columns = ['cliente_id', 'total_gastado', 'promedio_compra', 
                             'std_compra', 'min_compra', 'max_compra', 'num_compras']

print("\n" + "="*60)
print("Features agregadas por cliente:")
print(features_cliente)

# Features adicionales
features_cliente['rango_compra'] = features_cliente['max_compra'] - features_cliente['min_compra']
features_cliente['coef_variacion'] = features_cliente['std_compra'] / features_cliente['promedio_compra']

print("\n" + "="*60)
print("Con features derivadas:")
print(features_cliente)
```

### 7. Ratios y Proporciones

```python
import pandas as pd

# Datos financieros
df = pd.DataFrame({
    'ingresos': [100000, 150000, 200000, 80000],
    'gastos': [70000, 100000, 150000, 60000],
    'activos': [500000, 750000, 1000000, 400000],
    'pasivos': [200000, 300000, 500000, 150000]
})

print("Datos originales:")
print(df)

# Crear ratios financieros
df['margen_beneficio'] = (df['ingresos'] - df['gastos']) / df['ingresos']
df['ratio_deuda'] = df['pasivos'] / df['activos']
df['retorno_activos'] = (df['ingresos'] - df['gastos']) / df['activos']
df['ahorro_mensual'] = (df['ingresos'] - df['gastos']) / 12

print("\n" + "="*60)
print("Con ratios financieros:")
print(df)
```

---

## Feature Engineering para Variables Categóricas

### 1. One-Hot Encoding

```python
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# Datos
df = pd.DataFrame({
    'ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Madrid', 'Sevilla'],
    'color': ['rojo', 'azul', 'verde', 'rojo', 'azul']
})

print("Datos originales:")
print(df)

# Método 1: pd.get_dummies
df_dummies = pd.get_dummies(df, columns=['ciudad', 'color'], drop_first=True)
print("\n" + "="*60)
print("Con pd.get_dummies:")
print(df_dummies)

# Método 2: OneHotEncoder
ohe = OneHotEncoder(sparse_output=False, drop='first')
encoded = ohe.fit_transform(df)
feature_names = ohe.get_feature_names_out(['ciudad', 'color'])
df_ohe = pd.DataFrame(encoded, columns=feature_names)

print("\n" + "="*60)
print("Con OneHotEncoder:")
print(df_ohe)
```

### 2. Label Encoding

```python
from sklearn.preprocessing import LabelEncoder
import pandas as pd

# Datos con orden natural
df = pd.DataFrame({
    'educacion': ['Primaria', 'Secundaria', 'Universidad', 'Primaria', 'Universidad'],
    'satisfaccion': ['Bajo', 'Medio', 'Alto', 'Medio', 'Alto']
})

print("Datos originales:")
print(df)

# Label Encoding
le = LabelEncoder()
df['educacion_encoded'] = le.fit_transform(df['educacion'])

print("\n" + "="*60)
print("Con Label Encoding:")
print(df)
print(f"\nMapeo: {dict(zip(le.classes_, le.transform(le.classes_)))}")
```

### 3. Ordinal Encoding

```python
from sklearn.preprocessing import OrdinalEncoder
import pandas as pd

# Datos con orden explícito
df = pd.DataFrame({
    'tamaño': ['S', 'M', 'L', 'XL', 'S', 'M'],
    'nivel': ['Bajo', 'Medio', 'Alto', 'Medio', 'Bajo', 'Alto']
})

print("Datos originales:")
print(df)

# Definir orden explícito
oe = OrdinalEncoder(categories=[
    ['S', 'M', 'L', 'XL'],
    ['Bajo', 'Medio', 'Alto']
])

df_encoded = oe.fit_transform(df)
df_result = pd.DataFrame(df_encoded, columns=['tamaño_ord', 'nivel_ord'])
df_result = pd.concat([df, df_result], axis=1)

print("\n" + "="*60)
print("Con Ordinal Encoding:")
print(df_result)
```

### 4. Frequency Encoding

```python
import pandas as pd

# Datos
df = pd.DataFrame({
    'ciudad': ['Madrid', 'Barcelona', 'Madrid', 'Valencia', 'Madrid', 
               'Barcelona', 'Sevilla', 'Madrid', 'Valencia', 'Madrid']
})

print("Datos originales:")
print(df)
print(f"\nConteo de valores:\n{df['ciudad'].value_counts()}")

# Frequency encoding
freq_map = df['ciudad'].value_counts(normalize=True).to_dict()
df['ciudad_freq'] = df['ciudad'].map(freq_map)

print("\n" + "="*60)
print("Con Frequency Encoding:")
print(df)
print(f"\nInterpretación: Madrid aparece en {freq_map['Madrid']*100:.0f}% de las filas")
```

### 5. Target Encoding (Mean Encoding)

```python
import pandas as pd
import numpy as np

# Datos
np.random.seed(42)
df = pd.DataFrame({
    'ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Madrid', 'Barcelona',
               'Valencia', 'Madrid', 'Barcelona', 'Madrid', 'Valencia'] * 10,
    'compra': np.random.choice([0, 1], 100)
})

print("Datos originales (primeras filas):")
print(df.head(10))

# Target encoding (promedio de la variable objetivo por categoría)
target_means = df.groupby('ciudad')['compra'].mean().to_dict()
df['ciudad_target_enc'] = df['ciudad'].map(target_means)

print("\n" + "="*60)
print("Promedios por ciudad:")
print(target_means)

print("\n" + "="*60)
print("Con Target Encoding:")
print(df.head(10))

print("\nNota: En train/test split, calcular solo en train para evitar data leakage")
```

### 6. Count Encoding

```python
import pandas as pd

# Datos
df = pd.DataFrame({
    'producto': ['A', 'B', 'A', 'C', 'A', 'B', 'A', 'D', 'B', 'A']
})

print("Datos originales:")
print(df)

# Count encoding
count_map = df['producto'].value_counts().to_dict()
df['producto_count'] = df['producto'].map(count_map)

print("\n" + "="*60)
print("Con Count Encoding:")
print(df)
print(f"\nConteos: {count_map}")
```

---

## Feature Engineering para Fechas y Tiempo

### 1. Extracción de Componentes Temporales

```python
import pandas as pd
import numpy as np

# Crear fechas de ejemplo
df = pd.DataFrame({
    'fecha': pd.date_range('2024-01-01', periods=10, freq='D'),
    'ventas': np.random.randint(100, 1000, 10)
})

print("Datos originales:")
print(df)

# Extraer componentes
df['año'] = df['fecha'].dt.year
df['mes'] = df['fecha'].dt.month
df['dia'] = df['fecha'].dt.day
df['dia_semana'] = df['fecha'].dt.dayofweek  # 0=Lunes, 6=Domingo
df['nombre_dia'] = df['fecha'].dt.day_name()
df['semana_año'] = df['fecha'].dt.isocalendar().week
df['trimestre'] = df['fecha'].dt.quarter
df['es_fin_semana'] = (df['fecha'].dt.dayofweek >= 5).astype(int)
df['es_inicio_mes'] = (df['fecha'].dt.day <= 7).astype(int)

print("\n" + "="*60)
print("Con features temporales:")
print(df)
```

### 2. Features Cíclicas

```python
import pandas as pd
import numpy as np

# Datos con información temporal
df = pd.DataFrame({
    'mes': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'hora': [0, 6, 12, 18, 3, 9, 15, 21, 2, 8, 14, 20]
})

print("Datos originales:")
print(df)

# Encoding cíclico (captura la naturaleza circular del tiempo)
# Para mes (12 meses en un año)
df['mes_sin'] = np.sin(2 * np.pi * df['mes'] / 12)
df['mes_cos'] = np.cos(2 * np.pi * df['mes'] / 12)

# Para hora (24 horas en un día)
df['hora_sin'] = np.sin(2 * np.pi * df['hora'] / 24)
df['hora_cos'] = np.cos(2 * np.pi * df['hora'] / 24)

print("\n" + "="*60)
print("Con encoding cíclico:")
print(df)
print("\nVentaja: diciembre (12) está cerca de enero (1) en el espacio transformado")
```

### 3. Features de Diferencia Temporal

```python
import pandas as pd
import numpy as np

# Datos de eventos
df = pd.DataFrame({
    'cliente_id': [1, 1, 1, 2, 2, 3],
    'fecha_compra': pd.to_datetime([
        '2024-01-01', '2024-01-15', '2024-02-10',
        '2024-01-05', '2024-03-20', '2024-01-10'
    ])
})

print("Datos originales:")
print(df)

# Ordenar por cliente y fecha
df = df.sort_values(['cliente_id', 'fecha_compra'])

# Diferencia entre compras consecutivas
df['dias_desde_ultima_compra'] = df.groupby('cliente_id')['fecha_compra'].diff().dt.days

# Días desde la primera compra
df['dias_desde_primera'] = (
    df['fecha_compra'] - df.groupby('cliente_id')['fecha_compra'].transform('first')
).dt.days

print("\n" + "="*60)
print("Con features de diferencia temporal:")
print(df)
```

### 4. Features de Agregación Temporal

```python
import pandas as pd
import numpy as np

# Datos de transacciones
df = pd.DataFrame({
    'cliente_id': [1, 1, 1, 1, 2, 2, 2],
    'fecha': pd.date_range('2024-01-01', periods=7, freq='W'),
    'monto': [100, 150, 200, 120, 80, 90, 110]
})

print("Datos originales:")
print(df)

# Rolling statistics (ventanas móviles)
df['rolling_mean_3'] = df.groupby('cliente_id')['monto'].transform(
    lambda x: x.rolling(window=3, min_periods=1).mean()
)

df['rolling_sum_3'] = df.groupby('cliente_id')['monto'].transform(
    lambda x: x.rolling(window=3, min_periods=1).sum()
)

# Lag features (valores pasados)
df['monto_lag_1'] = df.groupby('cliente_id')['monto'].shift(1)
df['monto_lag_2'] = df.groupby('cliente_id')['monto'].shift(2)

print("\n" + "="*60)
print("Con features de agregación temporal:")
print(df)
```

---

## Feature Engineering para Texto

### 1. Features Básicas de Texto

```python
import pandas as pd
import re

# Datos de texto
df = pd.DataFrame({
    'texto': [
        'Este es un ejemplo corto',
        'Este texto es mucho más largo y tiene MAYÚSCULAS',
        '¿Tiene signos de interrogación? ¡Sí!',
        'usuario@email.com tiene correos'
    ]
})

print("Textos originales:")
print(df)

# Features básicas
df['longitud'] = df['texto'].str.len()
df['num_palabras'] = df['texto'].str.split().str.len()
df['num_caracteres_sin_espacios'] = df['texto'].str.replace(' ', '').str.len()
df['promedio_longitud_palabra'] = df['longitud'] / df['num_palabras']
df['num_mayusculas'] = df['texto'].str.count(r'[A-Z]')
df['num_minusculas'] = df['texto'].str.count(r'[a-z]')
df['num_digitos'] = df['texto'].str.count(r'\d')
df['num_signos_puntuacion'] = df['texto'].str.count(r'[^\w\s]')
df['tiene_email'] = df['texto'].str.contains(r'\S+@\S+').astype(int)
df['tiene_url'] = df['texto'].str.contains(r'http[s]?://').astype(int)

print("\n" + "="*60)
print("Con features de texto:")
print(df)
```

### 2. Bag of Words y TF-IDF

```python
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pandas as pd

# Corpus de documentos
documentos = [
    'El perro corre en el parque',
    'El gato duerme en la casa',
    'El perro y el gato juegan',
    'La casa tiene un parque grande'
]

print("Documentos originales:")
for i, doc in enumerate(documentos):
    print(f"{i}: {doc}")

# Bag of Words
vectorizer_bow = CountVectorizer()
bow_matrix = vectorizer_bow.fit_transform(documentos)
df_bow = pd.DataFrame(
    bow_matrix.toarray(),
    columns=vectorizer_bow.get_feature_names_out()
)

print("\n" + "="*60)
print("Bag of Words:")
print(df_bow)

# TF-IDF
vectorizer_tfidf = TfidfVectorizer()
tfidf_matrix = vectorizer_tfidf.fit_transform(documentos)
df_tfidf = pd.DataFrame(
    tfidf_matrix.toarray(),
    columns=vectorizer_tfidf.get_feature_names_out()
)

print("\n" + "="*60)
print("TF-IDF:")
print(df_tfidf.round(3))
```

### 3. N-gramas

```python
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

documentos = [
    'machine learning es importante',
    'deep learning es machine learning',
    'el machine learning avanza rápido'
]

print("Documentos originales:")
for i, doc in enumerate(documentos):
    print(f"{i}: {doc}")

# Unigramas (palabras individuales)
vectorizer_1gram = CountVectorizer(ngram_range=(1, 1))
matrix_1gram = vectorizer_1gram.fit_transform(documentos)
df_1gram = pd.DataFrame(
    matrix_1gram.toarray(),
    columns=vectorizer_1gram.get_feature_names_out()
)

print("\n" + "="*60)
print("Unigramas:")
print(df_1gram)

# Bigramas (pares de palabras)
vectorizer_2gram = CountVectorizer(ngram_range=(2, 2))
matrix_2gram = vectorizer_2gram.fit_transform(documentos)
df_2gram = pd.DataFrame(
    matrix_2gram.toarray(),
    columns=vectorizer_2gram.get_feature_names_out()
)

print("\n" + "="*60)
print("Bigramas:")
print(df_2gram)

# Combinado (1-grama y 2-gramas)
vectorizer_both = CountVectorizer(ngram_range=(1, 2))
matrix_both = vectorizer_both.fit_transform(documentos)
print(f"\n{matrix_both.shape[1]} features totales (unigramas + bigramas)")
```

---

## Feature Engineering Avanzado

### 1. PCA (Principal Component Analysis)

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

# Datos con muchas features correlacionadas
np.random.seed(42)
df = pd.DataFrame({
    'f1': np.random.randn(100),
    'f2': np.random.randn(100),
    'f3': np.random.randn(100),
    'f4': np.random.randn(100),
    'f5': np.random.randn(100)
})

# Crear correlaciones artificiales
df['f2'] = df['f1'] * 0.8 + np.random.randn(100) * 0.2
df['f3'] = df['f1'] * 0.6 + np.random.randn(100) * 0.4

print("Features originales:")
print(df.head())
print(f"\nForma original: {df.shape}")
print(f"\nCorrelaciones:\n{df.corr()}")

# Estandarizar primero
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)

# Aplicar PCA
pca = PCA(n_components=3)
df_pca = pca.fit_transform(df_scaled)

print("\n" + "="*60)
print("Después de PCA:")
print(f"Nueva forma: {df_pca.shape}")
print(f"\nVarianza explicada por componente: {pca.explained_variance_ratio_}")
print(f"Varianza total explicada: {pca.explained_variance_ratio_.sum():.3f}")

# Crear DataFrame con componentes principales
df_result = pd.DataFrame(df_pca, columns=['PC1', 'PC2', 'PC3'])
print("\nPrimeras filas con componentes principales:")
print(df_result.head())
```

### 2. Feature Crosses (Cruces de Features)

```python
import pandas as pd
import numpy as np

# Datos de comercio electrónico
df = pd.DataFrame({
    'categoria': ['Electrónica', 'Ropa', 'Electrónica', 'Hogar', 'Ropa'],
    'temporada': ['Verano', 'Invierno', 'Verano', 'Verano', 'Invierno'],
    'descuento': [10, 20, 15, 5, 25]
})

print("Datos originales:")
print(df)

# Feature cross: combinar categoría y temporada
df['categoria_temporada'] = df['categoria'] + '_' + df['temporada']

# Feature cross con interacción numérica
df['cat_descuento'] = df['categoria'] + '_desc_' + df['descuento'].astype(str)

print("\n" + "="*60)
print("Con feature crosses:")
print(df)

# Codificar
df_encoded = pd.get_dummies(df, columns=['categoria_temporada'])
print("\n" + "="*60)
print("Codificado:")
print(df_encoded)
```

### 3. Clustering como Feature

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

# Datos de clientes
np.random.seed(42)
df = pd.DataFrame({
    'edad': np.random.randint(18, 70, 200),
    'ingreso': np.random.randint(20000, 100000, 200),
    'gasto_mensual': np.random.randint(500, 5000, 200)
})

print("Datos originales (primeras filas):")
print(df.head(10))

# Estandarizar
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)

# Clustering
kmeans = KMeans(n_clusters=4, random_state=42)
df['cluster'] = kmeans.fit_predict(df_scaled)

print("\n" + "="*60)
print("Con cluster como feature:")
print(df.head(10))

# Estadísticas por cluster
print("\n" + "="*60)
print("Características por cluster:")
print(df.groupby('cluster').mean())

# Codificar cluster
df_with_cluster = pd.get_dummies(df, columns=['cluster'], prefix='cluster')
print("\n" + "="*60)
print("Con cluster one-hot encoded:")
print(df_with_cluster.head())
```

---

## Feature Selection

### 1. Eliminación de Features con Baja Varianza

```python
from sklearn.feature_selection import VarianceThreshold
import pandas as pd
import numpy as np

# Datos con algunas features constantes o casi constantes
df = pd.DataFrame({
    'f1': [1, 1, 1, 1, 1],  # Sin varianza
    'f2': [1, 1, 1, 1, 2],  # Muy poca varianza
    'f3': np.random.randn(5),
    'f4': np.random.randn(5),
    'f5': [0, 0, 0, 0, 0]  # Sin varianza
})

print("Datos originales:")
print(df)
print(f"\nVarianza por feature:\n{df.var()}")

# Eliminar features con varianza = 0
selector = VarianceThreshold(threshold=0)
df_filtered = pd.DataFrame(
    selector.fit_transform(df),
    columns=df.columns[selector.get_support()]
)

print("\n" + "="*60)
print("Después de eliminar varianza = 0:")
print(df_filtered)
```

### 2. Correlación entre Features

```python
import pandas as pd
import numpy as np

# Datos con features correlacionadas
np.random.seed(42)
df = pd.DataFrame({
    'f1': np.random.randn(100),
    'f2': np.random.randn(100),
    'f3': np.random.randn(100),
})

# Crear features correlacionadas
df['f4'] = df['f1'] * 0.95 + np.random.randn(100) * 0.05
df['f5'] = df['f2'] * 0.90 + np.random.randn(100) * 0.10

print("Correlaciones:")
corr_matrix = df.corr()
print(corr_matrix)

# Eliminar features altamente correlacionadas
def remove_correlated_features(df, threshold=0.9):
    """Elimina features con correlación > threshold"""
    corr_matrix = df.corr().abs()
    upper = corr_matrix.where(
        np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
    )
    to_drop = [column for column in upper.columns if any(upper[column] > threshold)]
    return df.drop(columns=to_drop), to_drop

df_reduced, dropped = remove_correlated_features(df, threshold=0.9)

print("\n" + "="*60)
print(f"Features eliminadas (correlación > 0.9): {dropped}")
print(f"Features restantes: {list(df_reduced.columns)}")
```

### 3. Feature Importance con Modelos

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
import pandas as pd
import numpy as np

# Crear dataset
X, y = make_classification(
    n_samples=1000,
    n_features=10,
    n_informative=5,
    n_redundant=3,
    n_repeated=2,
    random_state=42
)

feature_names = [f'feature_{i}' for i in range(10)]
df = pd.DataFrame(X, columns=feature_names)

print("Dataset con 10 features")
print(f"Forma: {df.shape}")

# Entrenar modelo
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(df, y)

# Feature importance
importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': modelo.feature_importances_
}).sort_values('importance', ascending=False)

print("\n" + "="*60)
print("Feature Importance:")
print(importance_df)

# Seleccionar top features
top_features = importance_df.head(5)['feature'].tolist()
print(f"\nTop 5 features: {top_features}")

df_selected = df[top_features]
print(f"Nueva forma: {df_selected.shape}")
```

### 4. Recursive Feature Elimination (RFE)

```python
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
import pandas as pd

# Crear dataset
X, y = make_classification(
    n_samples=500,
    n_features=10,
    n_informative=5,
    random_state=42
)

feature_names = [f'feature_{i}' for i in range(10)]
df = pd.DataFrame(X, columns=feature_names)

print("Dataset original:")
print(f"Forma: {df.shape}")

# RFE: seleccionar 5 mejores features
estimator = LogisticRegression(max_iter=1000)
selector = RFE(estimator, n_features_to_select=5, step=1)
selector.fit(df, y)

# Features seleccionadas
selected_features = [
    feature for feature, selected in zip(feature_names, selector.support_) 
    if selected
]

print("\n" + "="*60)
print(f"Features seleccionadas por RFE: {selected_features}")
print(f"\nRanking de features:")
for feature, rank in zip(feature_names, selector.ranking_):
    print(f"  {feature}: {rank}")

# Nuevo dataset
df_selected = df[selected_features]
print(f"\nNueva forma: {df_selected.shape}")
```

---

## Mejores Prácticas

### 1. Orden de operaciones

```python
"""
Orden recomendado para Feature Engineering:

1. Exploración de datos (EDA)
   - Entender distribuciones
   - Identificar outliers
   - Analizar correlaciones

2. Manejo de valores faltantes
   - Imputación
   - Crear indicadores de missing

3. Train/Test Split
   - ANTES de cualquier transformación

4. Feature Engineering
   - Crear nuevas features
   - Transformaciones
   - Codificación

5. Feature Scaling
   - Estandarización
   - Normalización

6. Feature Selection
   - Eliminar features irrelevantes
   - Reducir dimensionalidad

7. Modelado
"""
```

### 2. Evitar Data Leakage

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Datos
df = pd.DataFrame({
    'feature': np.random.randn(100),
    'target': np.random.choice([0, 1], 100)
})

# Split primero
X_train, X_test, y_train, y_test = train_test_split(
    df[['feature']], df['target'], test_size=0.2, random_state=42
)

print("CORRECTO: fit solo en train")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # Solo transform

print("\nINCORRECTO: fit en todo el dataset")
# Esto causa data leakage
scaler_wrong = StandardScaler()
X_all_scaled = scaler_wrong.fit_transform(df[['feature']])
# El modelo "ve" información del test set
```

### 3. Documentar Features

```python
"""
Mantener un registro de features creadas:
"""

feature_documentation = {
    'area_por_habitacion': {
        'formula': 'area_m2 / habitaciones',
        'tipo': 'ratio',
        'razon': 'Captura densidad de ocupación',
        'creada': '2024-01-15'
    },
    'es_nueva': {
        'formula': 'antiguedad < 5',
        'tipo': 'booleana',
        'razon': 'Casas nuevas tienen premium de precio',
        'creada': '2024-01-15'
    }
}
```

---

## Errores Comunes

### 1. Feature Engineering antes del split

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

df = pd.DataFrame({
    'feature': np.random.randn(100),
    'target': np.random.choice([0, 1], 100)
})

print("ERROR: Scaling antes del split")
# Esto causa data leakage
scaler = StandardScaler()
df['feature_scaled'] = scaler.fit_transform(df[['feature']])
X_train, X_test, y_train, y_test = train_test_split(
    df[['feature_scaled']], df['target'], test_size=0.2
)

print("\nCORRECTO: Split primero, luego scaling")
X_train, X_test, y_train, y_test = train_test_split(
    df[['feature']], df['target'], test_size=0.2
)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

### 2. Target Encoding sin validación

```python
import pandas as pd
import numpy as np

# ERROR: Target encoding en todo el dataset
df = pd.DataFrame({
    'categoria': ['A', 'B', 'A', 'C', 'B'] * 20,
    'target': np.random.choice([0, 1], 100)
})

# Esto causa overfitting
target_means = df.groupby('categoria')['target'].mean()
df['categoria_encoded'] = df['categoria'].map(target_means)

print("ERROR: El modelo memoriza el target")

# CORRECTO: Calcular solo en train
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    df[['categoria']], df['target'], test_size=0.2, random_state=42
)

# Calcular medias solo en train
train_df = pd.concat([X_train, y_train], axis=1)
target_means = train_df.groupby('categoria')['target'].mean()

# Aplicar a train y test
X_train['categoria_encoded'] = X_train['categoria'].map(target_means)
X_test['categoria_encoded'] = X_test['categoria'].map(target_means)

print("\nCORRECTO: Medias calculadas solo en train")
```

---

## Resumen

### Puntos clave

1. **Feature Engineering es crucial**
   - Puede mejorar el rendimiento más que cambiar de modelo
   - Requiere conocimiento del dominio
   - Es un proceso iterativo

2. **Tipos principales de técnicas**
   - Transformaciones: scaling, log, binning
   - Codificación: one-hot, label, target
   - Creación: polinomiales, interacciones, agregaciones
   - Selección: correlación, importance, RFE

3. **Orden importa**
   - Split ANTES de fit transformers
   - Crear features ANTES de scaling
   - Validar DESPUÉS de cada transformación

4. **Evitar errores comunes**
   - Data leakage (fit en test)
   - Target encoding sin validación
   - Alta cardinalidad sin procesar
   - No manejar NaN/infinitos

5. **Mejores prácticas**
   - Documentar features creadas
   - Validar consistencia train/test
   - Usar pipelines de sklearn
   - Hacer feature engineering iterativo
   - Medir impacto de cada feature

### Workflow recomendado

```python
"""
1. EDA y entendimiento de datos
2. Manejo de missing values
3. Train/test split
4. Feature Engineering (fit solo en train)
   - Crear features
   - Transformaciones
   - Codificación
5. Scaling (fit solo en train)
6. Feature Selection
7. Modelado
8. Evaluación
9. Iteración
"""
```

---

## Referencias

- Documentación sklearn: [Preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html)
- Feature Engineering: [sklearn feature_extraction](https://scikit-learn.org/stable/modules/feature_extraction.html)
- Feature Selection: [sklearn feature_selection](https://scikit-learn.org/stable/modules/feature_selection.html)
- Libro recomendado: "Feature Engineering for Machine Learning" por Alice Zheng & Amanda Casari
