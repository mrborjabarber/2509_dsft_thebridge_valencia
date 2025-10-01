# Análisis del código Battleship

## 👍 Cosas positivas


### Repositorio
repositorio bien ordenado muy intuitivo y con un readme perfecto

### Logica impecable
La logica del juego esta perfecta, se nota trabajada.


### Uso de argparse
Bien implementado con subcomandos (`play` y `demo`) y argumentos personalizables (`--board`, `--ship`).  
Eso hace el script flexible y fácil de ejecutar.

### Separación lógica del flujo
Hay una función `main()` que concentra la lógica del juego, y la inicialización de argumentos queda afuera.  
Eso ayuda a la legibilidad.

### Modo demo
Interesante que se pueda simular un juego sin intervención del usuario, útil para probar estrategias o depurar.

### Uso de estrategias
La idea de mantener `user_strategy` y `comp_strategy` y actualizarlas dinámicamente hace que el juego sea más sofisticado.

### Mensajes claros al usuario
Incluye feedback adecuado ("Hit!", "Miss!", "Congratulations!", etc.).

### Logica Quit
Eso esta increible.

---

## ⚠️ Posibles mejoras

### Importaciones innecesarias (codigo residual u opcional)
- `import random` ya no se usa (está comentado).  
- Si no lo vas a usar, mejor eliminarlo para mantener el código limpio.

### Repetición de código
- Tanto en el turno del usuario como en el de la computadora se repite bastante lógica:  
  generar coordenadas, llamar a `utils.fire`, actualizar estrategia, etc.  
- Se podría abstraer en una función auxiliar tipo:
  ```python
  take_turn(player, board_self, board_enemy, strategy, is_demo)
  ```

### Control de flujo
- Hay muchos `while True` con `break` y `return`.  
- Se podría limpiar la lógica usando funciones bien delimitadas y devolviendo estados (`hit/miss/win`).



### Separación de responsabilidades
- Ahora `main()` hace **todo**: inicializa tableros, imprime, gestiona turnos, actualiza estrategias.  
- Podrías dividir en funciones más pequeñas:
  - `setup_game(size, ships)`  
  - `player_turn(...)`  
  - `computer_turn(...)`  
  - `check_victory(...)`  

### Pruebas automáticas
- Podría ser útil permitir un **modo silencioso** en `demo` (sin prints), para poder ejecutar partidas rápidas y usarlas en **tests unitarios**.






# Correcciones y mejoras al código de Battleship

## 1. Importaciones
- Eliminar imports no usados.
```python
import utils
from time import sleep
import argparse
```

---

## 2. Comparaciones con `None`
- Usar `is None` en lugar de `== None` (PEP8).
```python
if user_strategy is None:
    ...
if comp_strategy is not None:
    ...
```

---

## 3. Abstracción de turnos repetidos
- Crear funciones auxiliares para no repetir lógica.

```python
def take_turn(player, board_self, board_enemy, strategy, is_demo=False):
    """
    Ejecuta un turno para el jugador dado.
    player: 'user' o 'comp'
    board_self: el tablero del propio jugador
    board_enemy: el tablero del oponente
    strategy: estrategia de disparo (puede ser None)
    is_demo: si es modo demo
    """
    size = len(board_self)
    row, col = None, None

    if player == "user" and not is_demo:
        cell = input(f"Enter cell (A1-{chr(65+size-1)}{size}): ")
        parsed = utils.parse_cell(cell, size)
        if parsed is None:
            print("Invalid cell. Try again.")
            return strategy, False
        elif parsed == 'quit':
            print("Quitting game.")
            return strategy, "quit"
        row, col = parsed
    else:
        # demo o computadora
        sleep(0.5)
        if strategy is None:
            row, col = utils.random_cell_from_board(board_enemy)
        else:
            row, col = utils.next_cell_from_strategy(strategy)

    # Disparo
    result = utils.fire((row, col), board_enemy)
    if result is None:
        if player == "user":
            print("Cell already fired. Try again.")
        return strategy, False

    mark = 'X' if result else 'A'
    board_enemy[row, col] = mark

    if player == "user":
        print("Hit!" if result else "Miss!")
    else:
        print(f"Computer {'hit' if result else 'missed'} at {chr(65+row)}{col+1}.")

    # Actualizar estrategia
    if is_demo or player == "comp":
        if strategy is None and result:
            strategy = utils.initial_firing_strategy((row, col), board_enemy)
        elif strategy is not None:
            strategy = utils.update_firing_strategy(mark, (row, col), strategy)

    return strategy, True
```

---

## 4. Separación de responsabilidades
- `main()` queda más limpio y legible.

```python
def main():
    size = args.board
    ships = args.ship
    is_demo = args.cmd == "demo"

    # Inicialización de tableros
    board_user = utils.populate_board(utils.setup_board(size), ships)
    board_comp = utils.populate_board(utils.setup_board(size), ships)
    board_comp_for_user = utils.setup_board(size)
    board_user_for_comp = utils.setup_board(size)

    user_strategy, comp_strategy = None, None

    utils.display_boards(board_comp_for_user, board_user)

    while True:
        # Turno del usuario
        user_strategy, ok = take_turn("user", board_user, board_comp, user_strategy, is_demo)
        if ok == "quit":
            return
        if utils.scan_board(board_comp) == 0:
            print("Congratulations! You sank all the computer's ships!")
            return

        # Turno de la computadora
        comp_strategy, _ = take_turn("comp", board_comp, board_user, comp_strategy)
        if utils.scan_board(board_user) == 0:
            print("Sorry, the computer sank all your ships. Game over.")
            return
```

---

## 5. Legibilidad
- Aplicar **PEP8 linting** (espacios, saltos de línea, nombres consistentes).
- Nombres de variables más expresivos donde sea necesario.

---

## 6. Bonus (opcional)
- Añadir un **modo silencioso** para `demo` (sin prints), útil en pruebas automáticas.
- Dividir el proyecto en módulos (`game.py`, `strategies.py`, `utils.py`) para mayor mantenibilidad.
