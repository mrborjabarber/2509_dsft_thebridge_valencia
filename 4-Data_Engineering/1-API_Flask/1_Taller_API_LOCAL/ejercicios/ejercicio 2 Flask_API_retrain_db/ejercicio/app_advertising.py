"""
API Flask para consumir el modelo de predicción de ventas
Requisitos:
1. Predicción de ventas a partir de gastos en publicidad
2. Actualizar la base de datos con nuevos registros
3. Reentrenar el modelo con los nuevos datos
"""
from flask import Flask, request, jsonify
import pickle
import pandas as pd
from model import train_model
import os

app = Flask(__name__)

# Rutas de archivos
MODEL_PATH = 'advertising.model'
CSV_PATH = 'Advertising.csv'

def load_model():
    """Carga el modelo entrenado"""
    if not os.path.exists(MODEL_PATH):
        print("Modelo no encontrado. Entrenando nuevo modelo...")
        train_model(CSV_PATH, MODEL_PATH)

    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    return model

# Cargar modelo al iniciar la aplicación
model = load_model()

@app.route('/')
def home():
    """Endpoint de bienvenida"""
    return jsonify({
        "message": "API de Predicción de Ventas",
        "endpoints": {
            "/predict": "POST - Predice ventas a partir de gastos en publicidad",
            "/add_data": "POST - Añade nuevos registros a la base de datos",
            "/retrain": "POST - Reentrena el modelo con todos los datos",
            "/data": "GET - Obtiene todos los registros"
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint 1: Predice ventas a partir de gastos en publicidad
    Espera JSON con: {"TV": float, "radio": float, "newspaper": float}
    """
    try:
        data = request.get_json()

        # Validar que vengan los datos necesarios
        if not all(key in data for key in ['TV', 'radio', 'newspaper']):
            return jsonify({
                "error": "Faltan datos. Se requieren: TV, radio, newspaper"
            }), 400

        # Preparar datos para predicción
        X = [[data['TV'], data['radio'], data['newspaper']]]

        # Realizar predicción
        prediction = model.predict(X)[0]

        return jsonify({
            "input": data,
            "predicted_sales": round(prediction, 2),
            "message": "Predicción realizada con éxito"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/add_data', methods=['POST'])
def add_data():
    """
    Endpoint 2: Añade nuevos registros a la base de datos
    Espera JSON con: {"TV": float, "radio": float, "newspaper": float, "sales": float}
    O una lista de registros
    """
    try:
        data = request.get_json()

        # Cargar CSV existente
        df = pd.read_csv(CSV_PATH)

        # Si es un solo registro, convertir a lista
        if isinstance(data, dict):
            data = [data]

        # Validar datos
        for record in data:
            if not all(key in record for key in ['TV', 'radio', 'newspaper', 'sales']):
                return jsonify({
                    "error": "Faltan datos. Se requieren: TV, radio, newspaper, sales"
                }), 400

        # Crear DataFrame con nuevos datos
        new_df = pd.DataFrame(data)

        # Añadir al CSV
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_csv(CSV_PATH, index=False)

        return jsonify({
            "message": f"{len(data)} registro(s) añadido(s) correctamente",
            "total_records": len(df)
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/retrain', methods=['POST'])
def retrain():
    """
    Endpoint 3: Reentrena el modelo con todos los datos actuales
    """
    try:
        global model

        # Reentrenar modelo
        model = train_model(CSV_PATH, MODEL_PATH)

        # Cargar datos para mostrar información
        df = pd.read_csv(CSV_PATH)

        return jsonify({
            "message": "Modelo reentrenado con éxito",
            "total_records_used": len(df),
            "r2_score": round(model.score(df[['TV', 'radio', 'newspaper']], df['sales']), 4)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/data', methods=['GET'])
def get_data():
    """
    Endpoint adicional: Obtiene todos los registros de la base de datos
    """
    try:
        df = pd.read_csv(CSV_PATH)
        return jsonify({
            "total_records": len(df),
            "data": df.to_dict(orient='records')
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
