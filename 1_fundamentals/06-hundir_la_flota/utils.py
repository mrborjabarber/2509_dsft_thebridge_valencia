import numpy as np 
import random 

def crear_tablero(tamaño=(10,10)): 
    return np.full(tamaño, "_") 

# Definimos la función colocar_barco que recibe:
# - barco: una lista de coordenadas (tuplas con fila y columna)
# - tablero: la matriz/lista donde vamos a colocar el barco
def colocar_barco(barco, tablero):
    # Recorremos cada coordenada del barco
    for casilla in barco:
        # Desempaquetamos la tupla en fila y columna
        fila, columna = casilla 
        # Marcamos en el tablero esa posición con 'O' (representa un barco)
        tablero[fila][columna] = 'O'
        
def disparar(casilla, tablero):
    fila, columna = casilla 
    if tablero [fila, columna] == "0":
        tablero[fila,columna ] = "X"
        return "Tocado" 
    
    else:
        tablero[fila,columna] = "A" 
        
resultado = disparar((0,4), tablero)
print(tablero)
print(resultado)