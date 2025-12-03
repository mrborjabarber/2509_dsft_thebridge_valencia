"""
Script para entrenar el modelo de predicción de ventas basado en gastos en publicidad
"""
import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

def train_model(csv_path='Advertising.csv', model_path='advertising.model'):
    """
    Entrena un modelo de regresión lineal con los datos de advertising
    y lo guarda en un archivo pickle
    """
    # Cargar datos
    df = pd.read_csv(csv_path)

    # Separar features y target
    X = df[['TV', 'radio', 'newspaper']]
    y = df['sales']

    # Entrenar modelo
    model = LinearRegression()
    model.fit(X, y)

    # Guardar modelo
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    print(f"Modelo entrenado y guardado en {model_path}")
    print(f"R² Score: {model.score(X, y):.4f}")

    return model

if __name__ == '__main__':
    train_model()
