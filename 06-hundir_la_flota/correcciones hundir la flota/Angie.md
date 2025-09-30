# Análisis del código del juego de barcos

##  Cosas buenas
- Uso claro de **funciones importadas** (`crear_tablero`, `colocar_barcos`, etc.), bien modularizado.
- Buen control del **turno** con variable booleana (`turno = 0 / 1`).
- Uso de **try/except** para manejar errores de entrada del usuario.
- Condiciones de victoria bien implementadas con `verificar_victoria`.
- La función principal está encapsulada en `juego()`, y se ejecuta solo con `if __name__ == "__main__":`, lo cual es buena práctica.

##  Cosas mejorables
- **Repetición de código** en la gestión de turnos → se podría extraer en funciones auxiliares (`turno_jugador()`, `turno_maquina()`).
- No se da **feedback claro al usuario** después de cada disparo (impacto, agua, hundido).
- Falta un **contador de turnos** o límite de jugadas para evitar partidas infinitas.
- Se podría añadir un **modo aleatorio de disparo mejorado** para la máquina (ahora dispara al azar sin memoria).


##  Opinión general
El código es **funcional y claro**, muy buen punto de partida para un juego clásico de Batalla Naval.  
Con pequeñas mejoras en la **experiencia del jugador** (mensajes más claros, feedback visual, límite de turnos, IA más lista), quedaría mucho más divertido y pulido.

---

##  Código pulido con comentarios

```python
from utils import (
    crear_tablero,
    colocar_barcos,
    disparar,
    disparo_aleatorio,
    verificar_victoria,
    mostrar_tablero
)

def juego():
    # Crear los tableros del jugador y la máquina
    tablero_jugador = crear_tablero()
    tablero_maquina = crear_tablero()

    # Colocar barcos en ambos tableros
    colocar_barcos(tablero_jugador)
    colocar_barcos(tablero_maquina)

    print("Tableros creados y barcos colocados.")
    turno = 0  # 0 = jugador, 1 = máquina

    # Bucle principal del juego
    while True:
        if turno == 0:
            # Turno del jugador
            print("\nTu tablero:")
            mostrar_tablero(tablero_jugador, ocultar_barcos=False)
            print("Tablero enemigo:")
            mostrar_tablero(tablero_maquina, ocultar_barcos=True)

            # Entrada de coordenadas con validación
            try:
                fila = int(input("Fila (0-9): "))
                col = int(input("Columna (0-9): "))
                if not (0 <= fila <= 9 and 0 <= col <= 9):
                    print(" Coordenadas fuera de rango. Intenta de nuevo.")
                    continue
            except ValueError:
                print(" Entrada no válida. Usa solo números.")
                continue

            # Disparo del jugador
            disparar((fila, col), tablero_maquina)

            # Verificar si el jugador ganó
            if verificar_victoria(tablero_maquina):
                print(" Has hundido todos los barcos enemigos. ¡YOU WIN!")
                break

            # Pasar turno a la máquina
            turno = 1
        else:
            # Turno de la máquina
            print("\nTurno de la máquina...")
            casilla = disparo_aleatorio(tablero_jugador)
            disparar(casilla, tablero_jugador)

            # Verificar si la máquina ganó
            if verificar_victoria(tablero_jugador):
                print(" La máquina hundió todos tus barcos. YOU LOSE.")
                break

            # Pasar turno al jugador
            turno = 0

# Punto de entrada del programa
if __name__ == "__main__":
    juego()
```
