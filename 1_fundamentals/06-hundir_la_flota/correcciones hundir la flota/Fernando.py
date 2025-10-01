import numpy as np
import random

# PARÁMETROS

N = 10                 

VACIO = "_"              
AGUA  = "A"               
HIT   = "X"               

FLOTA = [("P", 4, 1), ("C", 3, 2), ("S", 2, 3)]

NO_CONTACT = False  

OBJETIVO_IMPACTOS = sum(eslora * cantidad for _, eslora, cantidad in FLOTA)

# CREACIÓN Y COLOCACIÓN BARCOS

def crear_barco(eslora: int, tamaño: int = N):
    direcciones = [(0, 1), (1, 0), (0, -1), (-1, 0)]  
    while True:  # ERROR: había una comilla sobrante después de while True
        f = random.randint(0, tamaño - 1)
        c = random.randint(0, tamaño - 1)
        df, dc = random.choice(direcciones)
        coords = [(f + i * df, c + i * dc) for i in range(eslora)]
        if all(0 <= r < tamaño and 0 <= k < tamaño for r, k in coords):
            return coords

def sitio_valido(tab: np.ndarray, coords):
    n = tab.shape[0]

    # 1) sin solapamiento
    if not all(tab[r, c] == VACIO for r, c in coords):
        return False

    # 2) regla de "no contacto" (opcional)
    if NO_CONTACT:
        for r, c in coords:
            # ERROR: se usó 'for nr == (r, c, n):', lo cual es sintaxis inválida.
            # Corregido: iterar sobre vecinos adyacentes
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n:
                        if tab[nr, nc] in ("P", "C", "S"):
                            return False
    return True

def colocar_barco(coords, tab: np.ndarray, letra: str):
    for r, c in coords:
        tab[r, c] = letra

def colocar_barcos(tab: np.ndarray):
    barcos = []
    for letra, eslora, cantidad in FLOTA:
        for _ in range(cantidad):
            while True:
                coords = crear_barco(eslora, tab.shape[0])
                if sitio_valido(tab, coords):
                    colocar_barco(coords, tab, letra)
                    barcos.append(coords)
                    break
    return barcos

# DISPAROS 

def disparar(celda, tab: np.ndarray):
    r, c = celda
    if tab[r, c] in ("P", "C", "S"):
        tab[r, c] = HIT
        return "Tocado"
    if tab[r, c] == VACIO:
        tab[r, c] = AGUA
        return "Agua"
    return "Ya disparado"

def disparo_aleatorio(tab: np.ndarray):
    n = tab.shape[0]
    while True:
        r, c = random.randint(0, n - 1), random.randint(0, n - 1)
        if tab[r, c] not in (HIT, AGUA):
            return r, c

# PINTAR LOS TABLEROS

def mostrar_dos_tableros(mio: np.ndarray, cpu: np.ndarray, revelar_cpu=False):
    n = mio.shape[0]

    # CPU oculta barcos si revelar_cpu=False
    cpu_vista = cpu if revelar_cpu else np.where(np.isin(cpu, ("P", "C", "S")), VACIO, cpu)

    cab = "   " + " ".join(map(str, range(n)))
    print("\n    TU TABLERO".ljust(2 * n + 10) + "TABLERO ENEMIGO")
    print(cab + "     " + cab)
    print("  +" + "-" * (2 * n - 1) + "+     +" + "-" * (2 * n - 1) + "+")
    for i in range(n):
        izq = " ".join(mio[i])
        der = " ".join(cpu_vista[i])
        print(f"{i:>2}|{izq}|   {i:>2}|{der}|")
    print("  +" + "-" * (2 * n - 1) + "+     +" + "-" * (2 * n - 1) + "+")
    print("Leyenda: P/C/S=Barco (solo izq)  X=Tocado  A=Agua  _=Sin disparar\n")

# BUCLE JUEGO

def jugar():
    mi_tab = np.full((N, N), VACIO)
    su_tab = np.full((N, N), VACIO)

    colocar_barcos(mi_tab)
    colocar_barcos(su_tab)

    mis_hits = 0
    sus_hits = 0

    print("🚢 Hundir la Flota — simple (numpy + random)")
    print(f"Regla 'no contacto': {'ACTIVADA' if NO_CONTACT else 'desactivada'}")
    print("Formato de tiro: fila col (ej.: 3 5). Escribe 'salir' para terminar.\n")

    while True:
        mostrar_dos_tableros(mi_tab, su_tab)
        s = input("Tu disparo: ").strip().lower()
        if s == "salir":
            print("Fin.")
            return
        try:
            r, c = map(int, s.split())
            if not (0 <= r < N and 0 <= c < N):
                raise ValueError
        except Exception:
            print("Entrada inválida. Usa 'fila col' (ej.: 3 5)\n")
            continue

        res = disparar((r, c), su_tab)
        print("Tú:", res)
        if res == "Tocado":
            mis_hits += 1
            if mis_hits == OBJETIVO_IMPACTOS:
                mostrar_dos_tableros(mi_tab, su_tab, revelar_cpu=True)
                print("🏆 ¡Victoria! Hundiste toda la flota enemiga.")
                break
        elif res == "Ya disparado":
            print()
            continue

        r2, c2 = disparo_aleatorio(mi_tab)
        res2 = disparar((r2, c2), mi_tab)
        print(f"Máquina ({r2}, {c2}): {res2}\n")
        if res2 == "Tocado":
            sus_hits += 1
            if sus_hits == OBJETIVO_IMPACTOS:
                mostrar_dos_tableros(mi_tab, su_tab, revelar_cpu=True)
                print("💀 Derrota: la máquina hundió toda tu flota.")
                break

if __name__ == "__main__":
    jugar()
