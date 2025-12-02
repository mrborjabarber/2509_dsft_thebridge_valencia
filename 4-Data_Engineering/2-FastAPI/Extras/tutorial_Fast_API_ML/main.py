import os
import json
import pickle
from datetime import datetime
from typing import List

import numpy as np
import tensorflow as tf
from tensorflow import keras
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


# ============================================================
# MODELOS Pydantic
# ============================================================

class DatosCasa(BaseModel):
    tamano: float = Field(..., gt=0)
    habitaciones: int = Field(..., ge=1, le=10)
    banos: int = Field(..., ge=1, le=5)
    antiguedad: float = Field(..., ge=0, le=100)


class PrediccionRespuesta(BaseModel):
    precio_predicho: float
    confianza: str
    timestamp: str


class DatosReentrenamiento(BaseModel):
    datos: List[DatosCasa]
    precios: List[float]
    epochs: int = Field(default=50, ge=1, le=200)


# ============================================================
# VARIABLES GLOBALES
# ============================================================

modelo_actual = None
scaler_actual = None
metadata_actual = {}
historial_predicciones = []


# ============================================================
# CARGA DEL MODELO
# ============================================================

def cargar_modelo() -> bool:
    global modelo_actual, scaler_actual, metadata_actual

    try:
        ruta_keras = "modelos/modelo_precios.keras"
        ruta_h5 = "modelos/modelo_precios.h5"

        if os.path.exists(ruta_keras):
            modelo_actual = keras.models.load_model(ruta_keras)
        elif os.path.exists(ruta_h5):
            modelo_actual = keras.models.load_model(ruta_h5)
        else:
            raise FileNotFoundError("No existe modelo guardado.")

        if not os.path.exists("scaler.pkl"):
            raise FileNotFoundError("Falta scaler.pkl")

        with open("scaler.pkl", "rb") as f:
            scaler_actual = pickle.load(f)

        if os.path.exists("modelos/metadata.json"):
            with open("modelos/metadata.json", "r") as f:
                metadata_actual.update(json.load(f))

        print("Modelo cargado correctamente.")
        return True

    except Exception as e:
        print("Error al cargar modelo:", e)
        return False


cargar_modelo()


# ============================================================
# INICIALIZAR APP
# ============================================================

app = FastAPI(title="API Predicción Casas")

# Servir carpeta /static (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Página principal = index.html
@app.get("/")
async def servir_frontend():
    ruta_html = "app/static/index.html"
    if os.path.exists(ruta_html):
        return FileResponse(ruta_html)
    return {"error": "Archivo index.html no encontrado en /app/static"}


# ============================================================
# PREDICCIÓN
# ============================================================

@app.post("/predecir", response_model=PrediccionRespuesta)
async def predecir_precio(datos: DatosCasa):

    if modelo_actual is None or scaler_actual is None:
        raise HTTPException(status_code=503, detail="Modelo no cargado.")

    try:
        entrada = np.array([[datos.tamano, datos.habitaciones, datos.banos, datos.antiguedad]])
        entrada_norm = scaler_actual.transform(entrada)

        pred = float(modelo_actual.predict(entrada_norm, verbose=0)[0][0])
        mae_modelo = metadata_actual.get("metricas", {}).get("mae", 20000)

        if pred == 0:
            confianza = "baja"
        else:
            err = (mae_modelo / abs(pred)) * 100
            confianza = "alta" if err < 10 else "media" if err < 20 else "baja"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        historial_predicciones.append({
            "timestamp": timestamp,
            "entrada": datos.dict(),
            "prediccion": pred,
            "confianza": confianza
        })

        return PrediccionRespuesta(
            precio_predicho=round(pred, 2),
            confianza=confianza,
            timestamp=timestamp
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# PREDICCIÓN LOTES
# ============================================================

@app.post("/predecir/lote")
async def predecir_lote(lista: List[DatosCasa]):
    if modelo_actual is None:
        raise HTTPException(status_code=503, detail="Modelo no cargado.")

    try:
        X = np.array([[d.tamano, d.habitaciones, d.banos, d.antiguedad] for d in lista])
        X_norm = scaler_actual.transform(X)
        preds = modelo_actual.predict(X_norm, verbose=0)

        salida = []

        for i, d in enumerate(lista):
            salida.append({
                "indice": i,
                "entrada": d.dict(),
                "precio_predicho": round(float(preds[i][0]), 2)
            })

        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "n_predicciones": len(salida),
            "predicciones": salida
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# MONITORIZACIÓN
# ============================================================

@app.get("/monitorizar")
async def monitorizar():
    if modelo_actual is None:
        raise HTTPException(status_code=503, detail="Modelo no cargado.")

    return {
        "metricas": metadata_actual.get("metricas", {}),
        "total_predicciones": len(historial_predicciones)
    }


@app.get("/monitorizar/historial")
async def historial(n: int = 100):
    return historial_predicciones[-n:]


# ============================================================
# REENTRENAMIENTO
# ============================================================

@app.post("/reentrenar")
async def reentrenar(datos: DatosReentrenamiento):

    if modelo_actual is None:
        raise HTTPException(status_code=500, detail="Modelo no cargado.")

    if len(datos.datos) < 10:
        raise HTTPException(status_code=400, detail="Se requieren al menos 10 datos.")

    if len(datos.datos) != len(datos.precios):
        raise HTTPException(status_code=400, detail="Los datos y precios no coinciden.")

    try:
        X = np.array([[d.tamano, d.habitaciones, d.banos, d.antiguedad] for d in datos.datos])
        y = np.array(datos.precios)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        X_train = scaler_actual.transform(X_train)
        X_test = scaler_actual.transform(X_test)

        modelo_actual.fit(
            X_train, y_train,
            epochs=datos.epochs,
            batch_size=max(1, min(32, len(X_train) // 4)),
            validation_split=0.2,
            verbose=0
        )

        y_pred = modelo_actual.predict(X_test, verbose=0)

        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        metadata_actual["metricas"] = {
            "mse": float(mse),
            "mae": float(mae),
            "r2": float(r2)
        }

        metadata_actual["fecha_entrenamiento"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        modelo_actual.save("modelos/modelo_precios.keras")

        with open("modelos/metadata.json", "w") as f:
            json.dump(metadata_actual, f, indent=2)

        return {
            "status": "ok",
            "metricas": metadata_actual["metricas"],
            "mensaje": "Reentrenamiento completado."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# VALIDACIÓN REENTRENAMIENTO
# ============================================================

@app.post("/reentrenar/validar")
async def validar_reentrenamiento(datos: DatosReentrenamiento):
    problemas = []

    if len(datos.datos) < 10:
        problemas.append("Debe proporcionar al menos 10 datos.")

    if len(datos.datos) != len(datos.precios):
        problemas.append("Los datos no coinciden con los precios.")

    if any(p <= 0 for p in datos.precios):
        problemas.append("Hay precios negativos o cero.")

    return {
        "valido": len(problemas) == 0,
        "problemas": problemas
    }
