
# 📋 Opinión sobre el código

### ✅ Cosas buenas
- La lógica está bien estructurada: separar funciones para crear la matriz, colocar barcos y mostrar el tablero es una buena práctica.
- Uso de funciones como `is_sea`, `in_range_coord` y `get_initial_matrix`, que hacen que el código sea más modular y reutilizable.
- Correcta idea de separar barcos en diferentes tipos (1 casilla, 2 horizontales, 2 verticales).
- Intenta manejar turnos, municiones y condiciones de victoria/derrota, lo cual es un buen planteamiento para un juego tipo batalla naval.

### ❌ Cosas a mejorar
1. **Importaciones innecesarias**: `numpy` y `gamepy` no se usan.
2. **Errores en llamadas de funciones**: 
   - En `place_one_square_ships` y similares usas `x = get_random_x` en lugar de `x = get_random_x()`.
3. **Indentación incorrecta**: funciones como `print_matrix` y `all_ships_sunk` están mal anidadas dentro de otras.
4. **Funciones faltantes**: `print_ammunition_left`, `player_rival`, `get_coords`, `shot`, `claim_victory`, `claim_loose`, `print_matrix_with_ships` no están definidas.
5. **Legibilidad**: algunos `print` están desordenados, lo que dificulta entender qué ocurre en cada turno.
6. **Posibles bucles infinitos**: si no hay espacio suficiente para colocar barcos, los `while True` nunca terminarán.

---

# 🛠️ Versión corregida

```python
import random

# ========================
# VARIABLES GLOBALES
# ========================
lines = 5
columns = 5
sea = " "
ship_1 = "1"
ship_2 = "2"
ship_3 = "3"
missed_shot = "~"
success_shot = "X"
ammunition = 10
player1 = "P1"
player2 = "P2"

# ========================
# FUNCIONES DE MATRIZ
# ========================
def get_initial_matrix():
    return [[sea for _ in range(columns)] for _ in range(lines)]

def is_sea(x, y, matrix):
    return matrix[y][x] == sea

def in_range_coord(x, y):
    return 0 <= x < columns and 0 <= y < lines

# ========================
# COLOCAR BARCOS
# ========================
def get_random_x():
    return random.randint(0, columns - 1)

def get_random_y():
    return random.randint(0, lines - 1)

def place_one_square_ships(number, ship_class, matrix):
    ships_placed = 0
    while ships_placed < number:
        x, y = get_random_x(), get_random_y()
        if is_sea(x, y, matrix):
            matrix[y][x] = ship_class
            ships_placed += 1
    return matrix

def place_two_horizontal_squares_ships(number, ship_class, matrix):
    ships_placed = 0
    while ships_placed < number:
        x, y = get_random_x(), get_random_y()
        if in_range_coord(x + 1, y) and is_sea(x, y, matrix) and is_sea(x + 1, y, matrix):
            matrix[y][x] = ship_class
            matrix[y][x + 1] = ship_class
            ships_placed += 1
    return matrix

def place_two_vertical_squares_ships(number, ship_class, matrix):
    ships_placed = 0
    while ships_placed < number:
        x, y = get_random_x(), get_random_y()
        if in_range_coord(x, y + 1) and is_sea(x, y, matrix) and is_sea(x, y + 1, matrix):
            matrix[y][x] = ship_class
            matrix[y + 1][x] = ship_class
            ships_placed += 1
    return matrix

def place_and_print_ships(matrix, ships_number, player):
    one_square = ships_number // 2
    two_vertical = ships_number // 4
    two_horizontal = ships_number // 4
    print(f"Placing ships for {player}...")
    matrix = place_two_horizontal_squares_ships(two_horizontal, ship_2, matrix)
    matrix = place_two_vertical_squares_ships(two_vertical, ship_3, matrix)
    matrix = place_one_square_ships(one_square, ship_1, matrix)
    return matrix

# ========================
# IMPRIMIR TABLEROS
# ========================
def increase_character(c):
    return chr(ord(c) + 1)

def print_horizontal_barrier():
    print("+" + "---+" * columns)

def print_numbers_line():
    print("|   ", end="")
    for x in range(columns):
        print(f"| {x+1} ", end="")
    print("|")

def print_matrix(matrix, show_ships, player):
    print(f"\nThis is {player}'s sea:")
    print_horizontal_barrier()
    print_numbers_line()
    print_horizontal_barrier()
    character = "A"
    for y in range(lines):
        print(f"| {character} ", end="")
        for x in range(columns):
            square = matrix[y][x]
            if not show_ships and square not in (sea, missed_shot, success_shot):
                square = sea
            print(f"| {square} ", end="")
        print("|")
        character = increase_character(character)
        print_horizontal_barrier()

def all_ships_sunk(matrix):
    for row in matrix:
        for square in row:
            if square not in (sea, missed_shot, success_shot):
                return False
    return True

# ========================
# PLACEHOLDER DE JUEGO
# ========================
def play():
    ships_number = 6
    matrix_player1 = place_and_print_ships(get_initial_matrix(), ships_number, player1)
    matrix_player2 = place_and_print_ships(get_initial_matrix(), ships_number, player2)

    # Mostrar tableros iniciales (debug)
    print_matrix(matrix_player1, True, player1)
    print_matrix(matrix_player2, True, player2)

    print("\n⚠️ El loop de juego aún no está implementado.\n")

# ========================
# MAIN
# ========================
if __name__ == "__main__":
    play()
```

