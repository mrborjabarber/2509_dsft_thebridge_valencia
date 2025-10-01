# Análisis del código: Hundir la Flota (versión básica)

##  Cosas buenas
- Introducción amigable al juego con mensajes claros para el usuario.
- Estructura dividida en **tres fases** (crear tablero, poner barcos, disparar), lo cual ayuda a entender la lógica.
- Uso de variables contadoras (`contador`, `contador_aciertos`, `total_disparos`) para controlar la partida.
- Flujo de juego controlado por un **bucle while** con número máximo de disparos.
- Se da un **resumen final** de la partida (aciertos y disparos), lo cual mejora la experiencia del usuario.

##  Cosas mejorables
-El repositorio es un link a un zip eso deberias mejorarlo en el futuro.
- Las entradas `filas` y `columnas` se reciben como `input()` pero no se convierten a **enteros** antes de pasarlas a `crear_tablero`.  
  → Error potencial: `crear_tablero` seguramente espera números.
- Doble llamada a `coloca_barco` en el mismo bucle (`coloca_barco(tablero, barco)` y luego `tablero = coloca_barco(tablero, barco)`).  
  → Probable error de duplicación de código.
- Los barcos están **hardcodeados** en posiciones fijas, no son aleatorios ni definidos por el usuario.
- No hay validación de coordenadas en los disparos → el usuario puede meter valores fuera del tablero.
- `recibir_disparo` devuelve un booleano (`True/False`), pero el programa no informa al usuario si fue **impacto** o **agua**.
- El tablero se imprime directamente con `print(tablero)`, lo cual puede no ser visual ni amigable.
- La variable `disparo` se usa con `== True`, lo cual se puede simplificar a `if disparo:`.

##  Opinión general
Es un buen **primer prototipo** del juego: sencillo, funcional y claro para aprender.  
Con mejoras en la **interfaz de usuario** (mensajes de impacto, mostrar tablero mejor formateado, barcos aleatorios, validaciones), podría convertirse en un juego mucho más interactivo.

---

##  Código corregido y comentado

```python
from utils import *

print("BIENVENIDO AL JUEGO DE HUNDIR LA FLOTA")

# 1. CREAMOS TABLERO
print("Vamos a crear el tablero de juego")

# Convertir inputs a enteros
filas = int(input("Indica filas: "))
columnas = int(input("Indica columnas: "))
print(" " * 20)

print("Hay dos barcos, uno de 3 bloques y otro de 4")
print("¡ENCUÉNTRALOS!")

# Crear el tablero con las dimensiones indicadas
tablero = crear_tablero(filas, columnas)

# 2. PONEMOS LOS BARCOS (por ahora posiciones fijas)
barco1 = [(0, 1), (1, 1), (2, 1)]
barco2 = [(1, 3), (1, 4), (1, 5), (1, 6)]

# Colocar barcos en el tablero (evitar doble llamada)
for barco in [barco1, barco2]:
    tablero = coloca_barco(tablero, barco)

print(tablero)

# 3. DISPARAMOS
contador = 0
contador_aciertos = 0
total_disparos = 5
print(f"Llevas {contador} disparos de {total_disparos}.")
print("¡Te toca disparar!")

# FLUJO / BUCLE DE JUEGO
while contador < total_disparos:
    print("Nuevo disparo")

    try:
        fila = int(input("Indica la fila: "))
        columna = int(input("Indica la columna: "))

        # Validación de coordenadas
        if not (0 <= fila < filas and 0 <= columna < columnas):
            print(" Coordenadas fuera del tablero. Intenta de nuevo.")
            continue

        coordenada = (fila, columna)

        # Ejecutar disparo
        disparo = recibir_disparo(tablero, coordenada)
        contador += 1

        if disparo:
            print(" ¡Impacto!")
            contador_aciertos += 1
        else:
            print(" Agua...")

        print("Así está el juego:")
        print(f"Llevas {contador} disparos de {total_disparos}.")
        print(f"Aciertos: {contador_aciertos}")
        print(" ")
        print(tablero)
        print(" ")

    except ValueError:
        print(" Entrada inválida. Usa solo números.")

# Fin del juego
print("Has llegado al límite de disparos.")
print("RESUMEN DE LA PARTIDA")
print(f"Aciertos: {contador_aciertos}")
print("_" * 20)
```
