# ✅ Cosas buenas del código

-   **Uso de `numpy`**: facilita la creación y manipulación de matrices
    para el tablero.
-   **Funciones separadas (`crear_tablero`, `crear_barco`,
    `colocar_barco`, `disparar`)**: mejora la modularidad y permite
    reutilizar código.
-   **Prevención de disparos repetidos**: se usa un `set`
    (`disparos_hechos`) para evitar disparar en las mismas coordenadas.
-   **Aleatoriedad controlada**: se utiliza `random.randint` para
    seleccionar disparos y posiciones de barcos, simulando un juego
    real.
-   **Control de errores en colocación de barcos**: con un número máximo
    de intentos para colocar cada barco.

------------------------------------------------------------------------

# ⚠️ Cosas malas del código

1.  **Estructura poco clara entre archivo principal y utilidades**:
    mezcla el código del "juego" y el de "utils" en un mismo archivo,
    cuando deberían estar separados en dos módulos distintos.
2.  **Función `crear_barco` limitada**:
    -   Siempre crea barcos pegados al borde superior o izquierdo
        (empieza en `(0, x)` o `(x, 0)`).
    -   No genera posiciones iniciales aleatorias reales, lo que reduce
        la variedad.
3.  **Colocación de barcos defectuosa**:
    -   No evita solapamiento entre barcos de distintas llamadas.
    -   Puede terminar con menos barcos de los esperados si los intentos
        fallan.
4.  **Gestión de vidas poco clara**: `vidas` se usa como contador de
    turnos, no de impactos.
5.  **Función `disparar` poco realista**:
    -   Marca como "X" cualquier casilla distinta de `"_"`, incluso agua
        ya disparada.
    -   No diferencia entre disparo repetido en un barco ya tocado.
6.  **Poca retroalimentación al jugador**: solo imprime el tablero sin
    mostrar estadísticas (aciertos, fallos, barcos hundidos).
7.  **Malas prácticas menores**:
    -   Variables en minúscula pero con guiones bajos inconsistentes
        (`tablero_juego`, `nfilas`, `ncols`).
    -   Mensajes de error con errores tipográficos:
        `"Error el colocaccion..."`.

------------------------------------------------------------------------

# 🛠️ Código corregido y mejorado

``` python
import numpy as np
import random
import time

# ==========================
# FUNCIONES UTILIDAD
# ==========================

def crear_tablero(tamano: int = 10) -> np.ndarray:
    """Crea un tablero vacío con guiones bajos."""
    return np.full((tamano, tamano), "_", dtype='<U1')


def crear_barco(eslora: int) -> list:
    """Crea un barco con orientación aleatoria (H o V)."""
    orientacion = random.choice(("H", "V"))
    if orientacion == "H":
        return [(0, j) for j in range(eslora)]
    else:
        return [(i, 0) for i in range(eslora)]


def colocar_barco(tablero: np.ndarray, eslora: int) -> bool:
    """Coloca un barco en el tablero sin solapamiento. Devuelve True si se colocó."""
    barco = crear_barco(eslora)
    tam = len(tablero)
    direccion = "V" if barco[0][0] != barco[-1][0] else "H"
    max_intentos = 200

    for _ in range(max_intentos):
        if direccion == "H":
            fila = random.randint(0, tam - 1)
            col_ini = random.randint(0, tam - eslora)
            coords = [(fila, col_ini + j) for j in range(eslora)]
        else:  # Vertical
            col = random.randint(0, tam - 1)
            fila_ini = random.randint(0, tam - eslora)
            coords = [(fila_ini + i, col) for i in range(eslora)]

        # Verifica que no se solape
        if all(tablero[i, j] == "_" for i, j in coords):
            for i, j in coords:
                tablero[i, j] = "O"
            return True
    return False


def inicializar_tablero(tablero: np.ndarray) -> np.ndarray:
    """Coloca una flota en el tablero."""
    flota = [2, 2, 2, 3, 3, 4]
    for eslora in flota:
        if not colocar_barco(tablero, eslora):
            print("Error al colocar un barco.")
    return tablero


def disparar(casilla: tuple, tablero: np.ndarray) -> str:
    """Realiza un disparo en el tablero y devuelve el resultado."""
    i, j = casilla
    if tablero[i, j] == "O":
        tablero[i, j] = "X"
        return "Tocado"
    elif tablero[i, j] in ("X", "A"):
        return "Ya disparado"
    else:
        tablero[i, j] = "A"
        return "Agua"


# ==========================
# JUEGO PRINCIPAL
# ==========================

def jugar(vidas: int = 10):
    tablero = crear_tablero(10)
    tablero = inicializar_tablero(tablero)

    disparos_hechos = set()
    nfilas, ncols = tablero.shape

    while vidas > 0:
        x, y = random.randint(0, nfilas - 1), random.randint(0, ncols - 1)

        if (x, y) in disparos_hechos:
            continue

        disparos_hechos.add((x, y))
        resultado = disparar((x, y), tablero)

        print(f"Disparo a ({x}, {y}) -> {resultado}")
        print(tablero, "\n") 

        vidas -= 1
        time.sleep(1)


if __name__ == "__main__":
    jugar(15)
```

------------------------------------------------------------------------

# 🔑 Mejoras en la versión corregida

-   **Separación clara de funciones** y flujo de juego en `jugar()`.
-   **Colocación de barcos realista**: ahora empieza en posiciones
    aleatorias y no siempre en el borde.
-   **Evita solapamiento** de barcos al colocarlos.
-   **Gestión más clara de disparos**:
    -   `"X"` = tocado.
    -   `"A"` = agua.
    -   `"Ya disparado"` si se repite el tiro.
-   **Mensajes claros**: el jugador sabe si dio en agua o tocó un barco.
-   **Función `inicializar_tablero`** que coloca toda la flota de forma
    automática.
