# Correcciones y Comentarios sobre el código de Hundir la Flota

## ✅ Cosas positivas

-   **Buena legibilidad**: funciones cortas y bien comentadas.
-   **Buen readme**: es agradable y esta bien diseñado.
-  
-   **Uso de diccionarios (`LEYENDA`)** para mantener las descripciones
    de símbolos → muy limpio.
-   **Separación de responsabilidades**: creación de tableros,
    colocación de barcos, disparos y lógica de la partida están bien
    separados.
-   **Interfaz usuario--máquina** clara: se muestran tableros y
    resultados después de cada turno.
-   **Buena validación visual**: ocultas barcos enemigos en
    `mostrar_dos_tableros`.

------------------------------------------------------------------------

## ⚠️ Cosas a mejorar / posibles errores

### 1. Validación de entrada del jugador

Actualmente si el usuario introduce un número fuera de `1-10` o un
carácter no numérico, el programa falla.

``` python
def pedir_coordenada(mensaje, tamaño):
    while True:
        try:
            valor = int(input(mensaje)) - 1
            if 0 <= valor < tamaño:
                return valor
            else:
                print(f"⚠️ Debes elegir entre 1 y {tamaño}")
        except ValueError:
            print("⚠️ Ingresa un número válido.")
```

Uso en la partida:

``` python
fila = pedir_coordenada("Elige fila (1-10): ", tamaño_tablero)
col  = pedir_coordenada("Elige columna (1-10): ", tamaño_tablero)
```

------------------------------------------------------------------------

### 2. Colisiones entre barcos

`crear_barco` asegura que el barco quepa en el tablero, pero **no evita
que toque a otros barcos lateralmente**.\
Se puede ampliar la validación para comprobar casillas adyacentes.

------------------------------------------------------------------------

### 3. Disparos repetidos

Ahora mismo si disparas en una casilla repetida, devuelve
`"Ya disparado"` pero consumes turno igualmente.\
Podrías decidir: - Permitir que el jugador repita el disparo. - O
descontar turno pero dejarlo más claro.


------------------------------------------------------------------------

### 4. Centralizar definición de flota

Mejor usar constante global para definir barcos:

``` python
FLOTA = {
    "P": (4, 1),  # portaaviones
    "C": (3, 2),  # cruceros
    "S": (2, 3)   # submarinos
}
```

------------------------------------------------------------------------

### 5. Factorizar encabezado de tableros

La construcción repetida de cabecera puede hacerse función:

``` python
def encabezado_tablero(n):
    return " ".join(str(i) for i in range(1, n+1))
```

------------------------------------------------------------------------

### 6. Mejor feedback de partida

Además de los aciertos, mostrar cuántos barcos fueron hundidos.

------------------------------------------------------------------------

## ✨ Posibles mejoras opcionales

-   **Modo automático**: jugador vs máquina sin input.\
-   **Guardar/recuperar partida** con `pickle`.\
-   **IA más avanzada**: disparar alrededor de un acierto.

------------------------------------------------------------------------

👉 Resumen:\
El código está muy bien estructurado. Los puntos principales a corregir
son: 1. **Validación de entrada del jugador**.\
2. **Evitar barcos adyacentes** si quieres reglas más estrictas.
