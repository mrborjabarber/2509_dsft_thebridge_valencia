# 📝 Análisis del código

## ✅ Cosas buenas
- **Uso de funciones modulares**: separar en funciones (`crear_tablero`, `crear_barco`, `colocar_barcos`, `disparar`) hace que el código sea más legible y reutilizable.  
- **Uso de `numpy`**: el uso de `np.full` para inicializar el tablero es eficiente y limpio.  
- **Estructura de juego clara**: la lógica del turno jugador-oponente está bien diferenciada.  
- **Control de errores en `input`**: usas `try/except` para validar entradas del usuario.  
- **Uso de aleatoriedad**: `random.choice` y `random.randint` hacen que las partidas sean distintas.  

## ❌ Cosas a mejorar
1. **Indices fuera de rango posibles**: en `crear_barco` usas `randint(1, tamaño_tablero - 1)` en lugar de `randint(0, tamaño_tablero - 1)`, lo que desperdicia la primera fila/columna y puede generar errores.  
2. **Superposición de barcos no controlada**: al colocar barcos, no validas que no se pisen unos con otros.  
3. **Tablas redundantes**: repites mucho código creando y colocando barcos para jugador y oponente. Esto podría hacerse con un bucle.  
4. **Variable `disparo` mal usada en turno del oponente**: el disparo del jugador y del oponente usan la misma variable y puede dar errores en el flujo.  
5. **Lógica de vidas confusa**: empiezas con `vidas_jugador = 1` y `vidas_oponente = 1`, pero tienes más de un barco, no es consistente.  

---

# 📌 Código corregido y simplificado

```python
import numpy as np
import random

def crear_tablero(tamaño_tablero: int = 10):
    """Crea un tablero vacío"""
    return np.full((tamaño_tablero, tamaño_tablero), "_")

def crear_barco(eslora: int, tamaño_tablero: int = 10):
    """Crea un barco con orientación aleatoria"""
    direccion = random.choice(["horizontal", "vertical"])

    if direccion == "horizontal":
        fila = random.randint(0, tamaño_tablero - 1)
        columna_inicial = random.randint(0, tamaño_tablero - eslora)
        barco = [(fila, columna_inicial + i) for i in range(eslora)]
    else:
        fila_inicial = random.randint(0, tamaño_tablero - eslora)
        columna = random.randint(0, tamaño_tablero - 1)
        barco = [(fila_inicial + i, columna) for i in range(eslora)]

    return barco

def colocar_barcos(barco, tablero):
    """Coloca un barco en el tablero si las casillas están libres"""
    for fila, columna in barco:
        if tablero[fila, columna] == "O":  # barco ya colocado
            return False
    for fila, columna in barco:
        tablero[fila, columna] = "O"
    return True

def disparar(casilla, tablero):
    """Dispara a una casilla y devuelve el resultado"""
    fila, columna = casilla
    if tablero[fila, columna] == "O":
        tablero[fila, columna] = "X"
        return "Tocado"
    elif tablero[fila, columna] == "_":
        tablero[fila, columna] = "A"
        return "Agua"
    else:
        return "Ya disparaste aquí"

# ==============================
# Juego principal
# ==============================
tamaño_tablero = 10
flota = [2, 2, 2, 3, 3, 4]  # tamaños de barcos

tablero_jugador = crear_tablero()
tablero_oponente = crear_tablero()

# Colocar barcos jugador
for eslora in flota:
    colocado = False
    while not colocado:
        barco = crear_barco(eslora, tamaño_tablero)
        colocado = colocar_barcos(barco, tablero_jugador)

# Colocar barcos oponente
for eslora in flota:
    colocado = False
    while not colocado:
        barco = crear_barco(eslora, tamaño_tablero)
        colocado = colocar_barcos(barco, tablero_oponente)

vidas_jugador = sum(flota)
vidas_oponente = sum(flota)

turnos_limite = 10
turno_actual = 1

print("Empieza el juego\n")


while turno_actual <= turnos_limite and vidas_jugador > 0 and vidas_oponente > 0:
    print(f"Turno {turno_actual}")

    # Turno jugador
    while True:
        try:
            x = int(input("Fila (0-9): "))
            y = int(input("Columna (0-9): "))
            break
        except ValueError:
            print("Entrada no válida. Intenta de nuevo.")

    resultado = disparar((x, y), tablero_oponente)
    print("Resultado:", resultado)

    if resultado == "Tocado":
        vidas_oponente -= 1
        if vidas_oponente == 0:
            print("¡Has ganado!")
            break

    # Turno oponente
    x, y = random.randint(0, 9), random.randint(0, 9)
    resultado_oponente = disparar((x, y), tablero_jugador)
    print(f"El oponente dispara a ({x},{y}): {resultado_oponente}")

    if resultado_oponente == "Tocado":
        vidas_jugador -= 1
        if vidas_jugador == 0:
            print("¡Has perdido!")
            break

    turno_actual += 1

if turno_actual > turnos_limite:
    print("¡Se acabó el juego por límite de turnos!")
```
