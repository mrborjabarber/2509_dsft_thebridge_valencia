"""
Cliente de prueba para consumir la API de predicción de ventas
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def print_response(response):
    """Imprime la respuesta de forma legible"""
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 60)

def test_home():
    """Prueba el endpoint de bienvenida"""
    print("\n=== TEST 1: Home ===")
    response = requests.get(f"{BASE_URL}/")
    print_response(response)

def test_predict():
    """Prueba el endpoint de predicción"""
    print("\n=== TEST 2: Predicción de ventas ===")
    data = {
        "TV": 230.1,
        "radio": 37.8,
        "newspaper": 69.2
    }
    response = requests.post(f"{BASE_URL}/predict", json=data)
    print_response(response)

def test_add_data():
    """Prueba el endpoint de añadir datos"""
    print("\n=== TEST 3: Añadir nuevos datos ===")
    new_data = {
        "TV": 150.0,
        "radio": 25.5,
        "newspaper": 40.0,
        "sales": 15000.0
    }
    response = requests.post(f"{BASE_URL}/add_data", json=new_data)
    print_response(response)

def test_add_multiple_data():
    """Prueba añadir múltiples registros"""
    print("\n=== TEST 4: Añadir múltiples registros ===")
    multiple_data = [
        {"TV": 100.0, "radio": 20.0, "newspaper": 30.0, "sales": 12000.0},
        {"TV": 200.0, "radio": 35.0, "newspaper": 50.0, "sales": 18000.0}
    ]
    response = requests.post(f"{BASE_URL}/add_data", json=multiple_data)
    print_response(response)

def test_retrain():
    """Prueba el endpoint de reentrenamiento"""
    print("\n=== TEST 5: Reentrenar modelo ===")
    response = requests.post(f"{BASE_URL}/retrain")
    print_response(response)

def test_get_data():
    """Prueba obtener todos los datos"""
    print("\n=== TEST 6: Obtener datos (últimos 5 registros) ===")
    response = requests.get(f"{BASE_URL}/data")
    if response.status_code == 200:
        data = response.json()
        print(f"\nStatus Code: {response.status_code}")
        print(f"Total registros: {data['total_records']}")
        print(f"Últimos 5 registros:")
        print(json.dumps(data['data'][-5:], indent=2))
        print("-" * 60)
    else:
        print_response(response)

def test_predict_error():
    """Prueba el manejo de errores en predicción"""
    print("\n=== TEST 7: Error - Datos incompletos ===")
    data = {
        "TV": 230.1,
        "radio": 37.8
        # Falta 'newspaper'
    }
    response = requests.post(f"{BASE_URL}/predict", json=data)
    print_response(response)

if __name__ == '__main__':
    print("=" * 60)
    print("CLIENTE DE PRUEBA - API PREDICCIÓN DE VENTAS")
    print("=" * 60)
    print("\nAsegúrate de que la API está ejecutándose en http://127.0.0.1:5000")
    print("Ejecuta: python app_advertising.py")

    try:
        # Ejecutar todas las pruebas
        test_home()
        test_predict()
        test_add_data()
        test_add_multiple_data()
        test_retrain()
        test_get_data()
        test_predict_error()

        print("\n" + "=" * 60)
        print("TODAS LAS PRUEBAS COMPLETADAS")
        print("=" * 60)

    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: No se puede conectar a la API")
        print("Por favor, asegúrate de que la API está ejecutándose:")
        print("  python app_advertising.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
