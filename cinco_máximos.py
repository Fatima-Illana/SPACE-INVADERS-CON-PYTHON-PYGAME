# -----------------------------------------------------------------------------
# Nombre del Programa: cinco_máximos.py
# Autor: Fátima Illana Guerra
# Objetivo del porgrama: Obtiene del archivo total de puntuaciones, las cinco 
# más altas, junto al nombre de sus usuarios correspondientes.
# -----------------------------------------------------------------------------

from typing import List

# MÉTODO DE SELECCIÓN
def permutar (lista : List[int], i, j : int) -> List[int]:
# """Permuta los elementos de las posiciones i, j."""
    t : int = lista[i]
    lista[i] = lista[j]
    lista[j] = t
    return lista

def posicionDelMáximo (lista : List[int], inicio : int) -> int:
# """Obtiene la posición del máximo."""
    posMáx : int = inicio
    for i in range (inicio + 1, len(lista)):
        if (lista[i] > lista[posMáx]):
            posMáx = i
    return posMáx

def ordenarSeleccion (lista : List[int]) -> List[int]:
# """Ordena la lista, según las posiciones de los máximos."""
    posMáx : int
    for i in range (0, len(lista)):
        posMáx = posicionDelMáximo (lista, i)
        permutar(lista, i, posMáx)
    return lista

def lista_puntuaciones (lista : List[List[str]]) -> List[int]:
# """Define en una lista de enteros, las puntuaciones almacenadas en el archivo de puntuaciones."""
    lista_números = []
    for i in lista:
        lista_números += [int(i[1])]
    return cinco_mayores(lista_números)

def cinco_mayores (lista : List[int]) -> List[int]:
# """Obtiene, a partir de la lista ordenada decrecientemente, los cinco mayores."""
    lista = ordenarSeleccion(lista)
    lista_final = []
    for i in range(0, 5):
        lista_final += [lista[i]]
    return lista_final

def lista_split (nombre_fichero : str) -> List[List[str]]:
# """Devuelve una lista de listas de str, formada por las líneas y palabras de un archivo."""
    fichero = open(nombre_fichero)
    lista_final = []
    linea = fichero.readline()
    while linea != "":
      lista_final += [linea.split()]
      linea = fichero.readline()
    return lista_final
    
def ganadores (nombre_fichero : str) -> None:
# """Relaciona las cinco puntuaciones más altas con sus usuarios."""
    lista_líneas = lista_split(nombre_fichero)
    lista_mayores = lista_puntuaciones (lista_líneas)
    lista_final = []
    for i in lista_mayores:
            for j in lista_líneas:
                if (j[1] == str(i)) and (len(lista_final) <= 5):
    
                        lista_final += [j]
                else:
                    lista_final += []
    return lista_final


