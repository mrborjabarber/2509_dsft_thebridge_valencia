# API de Predicción de Ventas - Advertising

Solución completa del ejercicio de Flask API para desplegar un modelo de machine learning que predice ventas basándose en gastos de publicidad en TV, radio y periódicos.

## Archivos creados

- **model.py**: Script para entrenar y guardar el modelo de regresión lineal
- **app_advertising.py**: API Flask con todos los endpoints requeridos
- **test_api_advertising.py**: Cliente de prueba para consumir la API
- **Advertising.csv**: Base de datos con los registros de publicidad y ventas

## Requisitos cumplidos

### 1. Predicción de ventas
- Endpoint: `POST /predict`
- Recibe gastos en TV, radio y newspaper
- Retorna la predicción de ventas

### 2. Actualizar base de datos
- Endpoint: `POST /add_data`
- Permite añadir uno o múltiples registros nuevos
- Actualiza el archivo CSV

### 3. Reentrenar el modelo
- Endpoint: `POST /retrain`
- Reentrena el modelo con todos los datos actuales
- Actualiza el archivo del modelo

## Instalación y uso

### Paso 1: Instalar dependencias
```bash
pip install flask pandas scikit-learn
```

### Paso 2: Entrenar el modelo inicial (opcional)
```bash
python model.py
```

### Paso 3: Ejecutar la API
```bash
python app_advertising.py
```

La API estará disponible en `http://127.0.0.1:5000`

### Paso 4: Probar la API
En otra terminal, ejecutar:
```bash
python test_api_advertising.py
```

## Endpoints disponibles

### GET /
Información sobre la API y sus endpoints

### POST /predict
Predice ventas a partir de gastos en publicidad

**Request:**
```json
{
  "TV": 230.1,
  "radio": 37.8,
  "newspaper": 69.2
}
```

**Response:**
```json
{
  "input": {
    "TV": 230.1,
    "radio": 37.8,
    "newspaper": 69.2
  },
  "predicted_sales": 22100.0,
  "message": "Predicción realizada con éxito"
}
```

### POST /add_data
Añade nuevos registros a la base de datos

**Request (un registro):**
```json
{
  "TV": 150.0,
  "radio": 25.5,
  "newspaper": 40.0,
  "sales": 15000.0
}
```

**Request (múltiples registros):**
```json
[
  {"TV": 100.0, "radio": 20.0, "newspaper": 30.0, "sales": 12000.0},
  {"TV": 200.0, "radio": 35.0, "newspaper": 50.0, "sales": 18000.0}
]
```

**Response:**
```json
{
  "message": "2 registro(s) añadido(s) correctamente",
  "total_records": 203
}
```

### POST /retrain
Reentrena el modelo con todos los datos actuales

**Response:**
```json
{
  "message": "Modelo reentrenado con éxito",
  "total_records_used": 203,
  "r2_score": 0.8972
}
```

### GET /data
Obtiene todos los registros de la base de datos

**Response:**
```json
{
  "total_records": 200,
  "data": [...]
}
```

## Pruebas manuales con curl

```bash
# Predicción
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"TV": 230.1, "radio": 37.8, "newspaper": 69.2}'

# Añadir datos
curl -X POST http://127.0.0.1:5000/add_data \
  -H "Content-Type: application/json" \
  -d '{"TV": 150.0, "radio": 25.5, "newspaper": 40.0, "sales": 15000.0}'

# Reentrenar
curl -X POST http://127.0.0.1:5000/retrain

# Obtener datos
curl http://127.0.0.1:5000/data
```

## Arquitectura de la solución

1. **Modelo**: Regresión Lineal de scikit-learn
2. **Almacenamiento**: CSV (Advertising.csv)
3. **Modelo serializado**: Pickle (advertising.model)
4. **API**: Flask con endpoints RESTful
5. **Comunicación**: JSON

## Notas

- El modelo se carga automáticamente al iniciar la API
- Si no existe el modelo, se entrena automáticamente
- Los datos se persisten en el CSV
- El reentrenamiento actualiza el modelo en memoria y en disco
