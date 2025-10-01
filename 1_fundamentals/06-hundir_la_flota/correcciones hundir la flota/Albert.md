# Análisis del código: Hundir la Flota con NumPy

##  Cosas buenas
- Uso de **NumPy** para representar el tablero, lo cual simplifica el manejo de matrices.
- Función `crear_tablero` clara y parametrizable (permite cambiar tamaño).
- Barcos generados con orientación aleatoria (`crear_barcos`) → añade variedad al juego.
- `colocar_barcos` evita solapamiento de barcos con un bucle hasta encontrar posición válida.
- Disparo del jugador y de la máquina implementados de manera independiente.
- Funciones separadas para responsabilidades concretas (**modularidad**): crear tablero, colocar barcos, disparar, comprobar hundimiento, victoria, mostrar tablero.
- `victoria` usa NumPy (`np.any`) para verificar condición de fin de juego de forma eficiente.

##  Cosas mejorables
- `disparar_maquina` puede repetir disparos ya hechos → debería evitar disparar a casillas con "A" o "X".
- El disparo del jugador no valida si ya se disparó antes a esa casilla.
- `comprobar_barco_hundido` funciona bien, pero no se integra aún en la lógica principal (solo devuelve `True/False`).
- `mostrar_tablero` imprime todo sin ocultar barcos enemigos, lo cual en una partida real daría ventaja al jugador.
- Comentarios y docstrings podrían estar mejor estructurados (hay errores tipográficos como "duncion" → "función").

##  Opinión general
El código es **claro, modular y bien organizado**, con funciones que cubren las necesidades básicas del juego.  
Con pequeñas mejoras en la **validación de disparos, optimización de colocación de barcos, y diferenciación de lo que ve cada jugador**, sería una implementación robusta para un juego de Batalla Naval jugable en terminal.

---

##  Código Utils corregido y comentado

```python
import numpy as np
import random

# Crear un tablero vacío con "_"
def crear_tablero(tamaño=(10, 10)):
    return np.full(tamaño, "_")

# Generar un barco de cierta eslora con orientación aleatoria
def crear_barcos(eslora, tamaño_tablero=10):
    orientacion = random.choice(["horizontal", "vertical"])
    if orientacion == "horizontal":
        fila = random.randint(0, tamaño_tablero - 1)
        columna_inicial = random.randint(0, tamaño_tablero - eslora)
        barco = [(fila, columna_inicial + i) for i in range(eslora)]
    else:
        fila_inicial = random.randint(0, tamaño_tablero - eslora)
        columna = random.randint(0, tamaño_tablero - 1)
        barco = [(fila_inicial + i, columna) for i in range(eslora)]
    return barco

# Colocar barcos en el tablero evitando solapamientos
def colocar_barcos(tablero, lista_flota):
    barcos = []
    for eslora in lista_flota:
        barco_colocado = False
        while not barco_colocado:
            barco = crear_barcos(eslora, len(tablero))
            # Verificar que las casillas estén libres
            if all(tablero[fila, columna] == "_" for fila, columna in barco):
                for fila, columna in barco:
                    tablero[fila, columna] = "O"
                barcos.append(barco)
                barco_colocado = True
    return barcos

# Disparo del jugador: devuelve "Tocado" o "Agua"
def disparar_jugador(casilla, tablero_maquina):
    fila, columna = casilla
    if tablero_maquina[fila, columna] == "O":
        tablero_maquina[fila, columna] = "X"
        return "Tocado"
    elif tablero_maquina[fila, columna] in ["X", "A"]:
        return "Ya disparaste aquí"
    else:
        tablero_maquina[fila, columna] = "A"
        return "Agua"

# Disparo de la máquina: aleatorio, debería evitar casillas repetidas
def disparar_maquina(tablero_jugador):
    while True:
        fila = random.randint(0, len(tablero_jugador) - 1)
        columna = random.randint(0, len(tablero_jugador[0]) - 1)
        if tablero_jugador[fila, columna] not in ["X", "A"]:  # Evitar repetidos
            if tablero_jugador[fila, columna] == "O":
                tablero_jugador[fila, columna] = "X"
                return (fila, columna), "Tocado"
            else:
                tablero_jugador[fila, columna] = "A"
                return (fila, columna), "Agua"

# Comprueba si todas las casillas de un barco han sido impactadas
def comprobar_barco_hundido(barco, tablero):
    return all(tablero[fila, columna] == "X" for fila, columna in barco)

# Comprueba si en un tablero quedan barcos
def victoria(tablero):
    return not np.any(tablero == "O")

# Muestra el tablero (se puede mejorar para ocultar barcos enemigos)
def mostrar_tablero(tablero, ocultar_barcos=False):
    for fila in tablero:
        fila_str = []
        for celda in fila:
            if ocultar_barcos and celda == "O":
                fila_str.append("_")  # Oculta los barcos
            else:
                fila_str.append(celda)
        print(" ".join(fila_str))
    print()
```

