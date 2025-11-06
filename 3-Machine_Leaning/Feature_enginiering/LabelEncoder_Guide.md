# LabelEncoder - Guía Completa

## Índice

1. [¿Qué es LabelEncoder?](#qué-es-labelencoder)
2. [Ejemplo Simple](#ejemplo-simple)
3. [Cómo Funciona](#cómo-funciona)
4. [Caso Práctico: Clasificación](#caso-práctico-clasificación)
5. [Limitación Importante: Orden Artificial](#limitación-importante-orden-artificial)
6. [Cuándo Usar Cada Codificador](#cuándo-usar-cada-codificador)
7. [Ejemplo Completo con Train/Test](#ejemplo-completo-con-traintest)
8. [Resumen](#resumen)

---

## ¿Qué es LabelEncoder?

**LabelEncoder** es una herramienta de scikit-learn que convierte **categorías de texto en números enteros**. Es útil porque los algoritmos de machine learning solo entienden números.

### Características principales

- Convierte datos categóricos en números enteros secuenciales
- Asigna un número único a cada categoría
- Es reversible (puedes recuperar las etiquetas originales)
- Útil para variables objetivo y features categóricas

---

## Ejemplo Simple

```python
from sklearn.preprocessing import LabelEncoder

# Datos categóricos
colores = ['rojo', 'azul', 'verde', 'rojo', 'verde', 'azul']

# Crear el encoder
le = LabelEncoder()

# Transformar texto → números
colores_encoded = le.fit_transform(colores)
print(colores_encoded)
# Output: [2 0 1 2 1 0]

# Ver la correspondencia
print(le.classes_)
# Output: ['azul' 'verde' 'rojo']
```

**Resultado de la codificación:**
- `azul` → 0
- `verde` → 1
- `rojo` → 2

**Nota:** Los números se asignan en orden alfabético por defecto.

---

## Cómo Funciona

### Métodos principales

```python
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()

# 1. fit() - Aprende las categorías únicas
le.fit(['gato', 'perro', 'gato', 'pájaro'])
print("Categorías aprendidas:", le.classes_)
# Output: ['gato' 'perro' 'pájaro']

# 2. transform() - Convierte a números
numeros = le.transform(['gato', 'perro', 'pájaro'])
print("Números asignados:", numeros)
# Output: [0 1 2]

# 3. fit_transform() - Hace ambos pasos a la vez
numeros = le.fit_transform(['gato', 'perro', 'gato'])
print("Resultado:", numeros)
# Output: [0 1 0]

# 4. inverse_transform() - Recupera las etiquetas originales
originales = le.inverse_transform([0, 1, 2])
print("Etiquetas originales:", originales)
# Output: ['gato' 'perro' 'pájaro']
```

### Tabla de métodos

| Método | Descripción | Cuándo usar |
|--------|-------------|-------------|
| `fit(data)` | Aprende las categorías únicas | Solo en datos de entrenamiento |
| `transform(data)` | Convierte categorías a números | En train y test |
| `fit_transform(data)` | fit + transform en un solo paso | Solo en datos de entrenamiento |
| `inverse_transform(data)` | Convierte números a categorías | Para interpretar resultados |

---

## Caso Práctico: Clasificación

```python
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

# Dataset de ejemplo
data = pd.DataFrame({
    'tamaño': ['pequeño', 'mediano', 'grande', 'pequeño', 'grande'],
    'color': ['rojo', 'azul', 'rojo', 'verde', 'azul'],
    'comprar': ['no', 'sí', 'sí', 'no', 'sí']  # Variable objetivo
})

print("Datos originales:")
print(data)

# Codificar características (features)
le_tamaño = LabelEncoder()
le_color = LabelEncoder()

data['tamaño_encoded'] = le_tamaño.fit_transform(data['tamaño'])
data['color_encoded'] = le_color.fit_transform(data['color'])

# Codificar variable objetivo
le_target = LabelEncoder()
y = le_target.fit_transform(data['comprar'])

print("\nDatos codificados:")
print(data)
print("\nVariable objetivo codificada:")
print(y)

# Ver las correspondencias
print("\nCorrespondencias tamaño:")
for i, clase in enumerate(le_tamaño.classes_):
    print(f"  {clase} → {i}")

print("\nCorrespondencias color:")
for i, clase in enumerate(le_color.classes_):
    print(f"  {clase} → {i}")

print("\nCorrespondencias target:")
for i, clase in enumerate(le_target.classes_):
    print(f"  {clase} → {i}")
```

**Resultado:**
```
Datos originales:
   tamaño  color comprar
0  pequeño   rojo      no
1  mediano   azul      sí
2   grande   rojo      sí
3  pequeño  verde      no
4   grande   azul      sí

Datos codificados:
   tamaño  color comprar  tamaño_encoded  color_encoded
0  pequeño   rojo      no               2              1
1  mediano   azul      sí               1              0
2   grande   rojo      sí               0              1
3  pequeño  verde      no               2              2
4   grande   azul      sí               0              0

Variable objetivo codificada:
[0 1 1 0 1]

Correspondencias tamaño:
  grande → 0
  mediano → 1
  pequeño → 2

Correspondencias color:
  azul → 0
  rojo → 1
  verde → 2

Correspondencias target:
  no → 0
  sí → 1
```

---

## Limitación Importante: Orden Artificial

### El problema

LabelEncoder asigna números secuenciales, lo que **implica un orden que puede no existir**:

```python
from sklearn.preprocessing import LabelEncoder

# Ejemplo problemático
frutas = ['manzana', 'naranja', 'plátano']
le = LabelEncoder()
encoded = le.fit_transform(frutas)

print("Codificación:", encoded)
# Output: [0 1 2]

# Problema: El modelo puede interpretar que:
# naranja (1) > manzana (0)
# plátano (2) > naranja (1)
# Pero esto no tiene sentido para frutas sin orden natural
```

### La solución: OneHotEncoder

Para características sin orden natural, usar **OneHotEncoder**:

```python
from sklearn.preprocessing import OneHotEncoder
import numpy as np

frutas = [['manzana'], ['naranja'], ['plátano'], ['manzana']]
ohe = OneHotEncoder(sparse_output=False)
encoded = ohe.fit_transform(frutas)

print("OneHot Encoding:")
print(encoded)
print("\nCategorías:", ohe.categories_)

# Output:
# [[1. 0. 0.]  <- manzana
#  [0. 1. 0.]  <- naranja
#  [0. 0. 1.]  <- plátano
#  [1. 0. 0.]] <- manzana
```

### Comparación visual

```python
# LabelEncoder
# frutas: ['manzana', 'naranja', 'plátano']
# → [0, 1, 2]
# Problema: Implica orden 0 < 1 < 2

# OneHotEncoder
# frutas: ['manzana', 'naranja', 'plátano']
# → [[1,0,0], [0,1,0], [0,0,1]]
# Ventaja: No implica orden, cada categoría es independiente
```

---

## Cuándo Usar Cada Codificador

### Tabla de decisión

| Situación | Codificador recomendado | Razón |
|-----------|------------------------|-------|
| Variable objetivo (y) | **LabelEncoder** | Solo necesita números únicos |
| Categorías con orden natural (pequeño < mediano < grande) | **LabelEncoder** u **OrdinalEncoder** | El orden tiene significado |
| Categorías sin orden (rojo, azul, verde) | **OneHotEncoder** | Evita orden artificial |
| Árboles de decisión / Random Forest | Ambos funcionan | Los árboles manejan bien ambos tipos |
| Regresión lineal / SVM / Redes neuronales | **OneHotEncoder** (para features) | Estos modelos son sensibles al orden |
| Alta cardinalidad (muchas categorías) | **Target Encoding** o **LabelEncoder** | OneHot crea demasiadas columnas |

### Ejemplos por tipo de variable

```python
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder, OneHotEncoder

# 1. Variable con orden natural
educacion = ['Primaria', 'Secundaria', 'Universidad', 'Primaria']
le = LabelEncoder()
edu_encoded = le.fit_transform(educacion)
print("Educación (LabelEncoder):", edu_encoded)

# 2. Variable sin orden (mejor OneHot)
colores = [['rojo'], ['azul'], ['verde'], ['rojo']]
ohe = OneHotEncoder(sparse_output=False)
col_encoded = ohe.fit_transform(colores)
print("Colores (OneHotEncoder):\n", col_encoded)

# 3. Variable objetivo (siempre LabelEncoder)
target = ['compra', 'no_compra', 'compra', 'compra']
le_target = LabelEncoder()
target_encoded = le_target.fit_transform(target)
print("Target (LabelEncoder):", target_encoded)
```

---

## Ejemplo Completo con Train/Test

### Flujo completo de preprocesamiento

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

# 1. Crear dataset
df = pd.DataFrame({
    'ciudad': ['Madrid', 'Barcelona', 'Madrid', 'Valencia', 'Barcelona', 
               'Madrid', 'Valencia', 'Barcelona'],
    'género': ['M', 'F', 'M', 'F', 'M', 'F', 'M', 'F'],
    'edad': [25, 30, 35, 28, 42, 38, 29, 45],
    'compra': ['sí', 'no', 'sí', 'sí', 'no', 'sí', 'no', 'sí']
})

print("Dataset original:")
print(df)

# 2. Separar features y target
X = df[['ciudad', 'género', 'edad']]
y = df['compra']

# 3. Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

print(f"\nTamaño train: {len(X_train)}")
print(f"Tamaño test: {len(X_test)}")

# 4. Codificar features categóricas
le_ciudad = LabelEncoder()
le_genero = LabelEncoder()

# IMPORTANTE: fit solo en train
X_train_encoded = pd.DataFrame({
    'ciudad': le_ciudad.fit_transform(X_train['ciudad']),
    'género': le_genero.fit_transform(X_train['género']),
    'edad': X_train['edad'].values
})

# En test: solo transform (sin fit)
X_test_encoded = pd.DataFrame({
    'ciudad': le_ciudad.transform(X_test['ciudad']),
    'género': le_genero.transform(X_test['género']),
    'edad': X_test['edad'].values
})

print("\nX_train codificado:")
print(X_train_encoded)

# 5. Codificar target
le_y = LabelEncoder()
y_train_encoded = le_y.fit_transform(y_train)
y_test_encoded = le_y.transform(y_test)

print("\ny_train codificado:", y_train_encoded)
print("Correspondencia:", dict(zip(le_y.classes_, range(len(le_y.classes_)))))

# 6. Entrenar modelo
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train_encoded, y_train_encoded)

# 7. Predicción
predicciones_encoded = modelo.predict(X_test_encoded)
predicciones_originales = le_y.inverse_transform(predicciones_encoded)

print("\nPredicciones:")
print(predicciones_originales)

# 8. Evaluación
accuracy = accuracy_score(y_test_encoded, predicciones_encoded)
print(f"\nAccuracy: {accuracy:.2f}")

# Reporte de clasificación con etiquetas originales
print("\nReporte de clasificación:")
print(classification_report(
    y_test, 
    predicciones_originales, 
    target_names=le_y.classes_
))
```

### Puntos críticos del ejemplo

**1. fit vs transform:**
```python
# CORRECTO
le.fit_transform(X_train)  # En train: fit + transform
le.transform(X_test)       # En test: solo transform

# INCORRECTO (causa data leakage)
le.fit_transform(X_train)  # En train
le.fit_transform(X_test)   # En test: NO hacer fit de nuevo
```

**2. Mantener encoders separados:**
```python
# Crear un encoder por cada columna categórica
le_ciudad = LabelEncoder()
le_genero = LabelEncoder()
le_target = LabelEncoder()

# No reutilizar el mismo encoder para diferentes columnas
```

**3. Guardar encoders para producción:**
```python
import pickle

# Guardar encoders
with open('le_ciudad.pkl', 'wb') as f:
    pickle.dump(le_ciudad, f)

# Cargar encoders
with open('le_ciudad.pkl', 'rb') as f:
    le_ciudad_loaded = pickle.load(f)

# Usar en nuevos datos
nuevos_datos = ['Barcelona', 'Madrid']
encoded = le_ciudad_loaded.transform(nuevos_datos)
```

---

## Resumen

### Ventajas de LabelEncoder

- Simple y fácil de usar
- Eficiente en memoria (almacena solo enteros)
- Perfecto para variables objetivo
- Funciona bien con árboles de decisión
- Reversible con inverse_transform()

### Desventajas de LabelEncoder

- Crea orden artificial en categorías sin orden
- No adecuado para regresión lineal/SVM con features sin orden
- Puede causar problemas si aparecen categorías nuevas en test

### Mejores prácticas

1. **Para variable objetivo (y):** Usar siempre LabelEncoder
2. **Para features sin orden:** Preferir OneHotEncoder
3. **Para features con orden:** LabelEncoder u OrdinalEncoder
4. **fit solo en train:** Evitar data leakage
5. **Guardar encoders:** Para usar en producción
6. **Manejar categorías desconocidas:** Usar `handle_unknown='ignore'` en OneHotEncoder o crear categoría "Otros"

### Código mínimo funcional

```python
from sklearn.preprocessing import LabelEncoder

# Crear y ajustar
le = LabelEncoder()
y_train_encoded = le.fit_transform(y_train)

# Transformar test
y_test_encoded = le.transform(y_test)

# Recuperar originales
y_pred_original = le.inverse_transform(y_pred_encoded)
```

### Alternativas a considerar

- **OrdinalEncoder:** Para múltiples columnas con orden
- **OneHotEncoder:** Para categorías sin orden
- **TargetEncoder:** Para alta cardinalidad
- **pd.get_dummies():** Alternativa rápida para OneHot en pandas

---

## Referencias

- Documentación oficial: [sklearn.preprocessing.LabelEncoder](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html)
- Comparación de encoders: [Categorical Encoding Methods](https://scikit-learn.org/stable/modules/preprocessing.html#encoding-categorical-features)
