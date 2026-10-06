"""
callejero.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP03B
Integrantes:
    - Miguel Pajuelo Gomez
    - Jorge Ois de Pascual

Descripción:
Librería con herramientas y clases auxiliares necesarias para la representación de un callejero en un grafo.

Complétese esta descripción según las funcionalidades agregadas por el grupo.
"""

import osmnx as ox
import matplotlib.pyplot  as plt
import networkx as nx
import pandas as pd
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
import re
from fuzzywuzzy import process

from typing import Tuple

class AddressNotFoundError(Exception):
    """Excepción personalizada cuando no se encuentra una dirección"""
    pass

STREET_FILE_NAME="direcciones.csv"

PLACE_NAME = "Madrid, Spain"
MAP_FILE_NAME="madrid.graphml"

MAX_SPEEDS = {
    'living_street': 20,
    'residential': 30,
    'primary_link': 40,
    'unclassified': 40,
    'secondary_link': 40,
    'trunk_link': 40,
    'secondary': 50,
    'tertiary': 50,
    'primary': 50,
    'trunk': 50,
    'tertiary_link': 50,
    'busway': 50,
    'motorway_link': 70,
    'motorway': 100
}


class ServiceNotAvailableError(Exception):
    "Excepción que indica que la navegación no está disponible en este momento"
    pass


class AdressNotFoundError(Exception):
    "Excepción que indica que una dirección buscada no existe en la base de datos"
    pass


############## Parte 2 ##############

def hora_dec(num:str)-> float:

    pattern = re.compile(r"(\d+)°(\d+)'([\d\.]+)\'\' ([NSWE]+)")

    coords = re.fullmatch(pattern, num)
    coords_grados = float(coords.group(1))
    coords_minutos = float(coords.group(2))
    coords_segundos = float(coords.group(3))
    coords_direccion = coords.group(4)

    coords_decimal =  coords_grados + (coords_minutos / 60) + (coords_segundos / 3600)
    if  coords_direccion in ["S", "W"]:
        coords_decimal =  -coords_decimal

    return coords_decimal


def carga_callejero() -> pd.DataFrame:
    """ Función que carga el callejero de Madrid, lo procesa y devuelve
    un DataFrame con los datos procesados
    
    Args: None
    Returns:
        DataFrame: dataframe con los datos del callejero procesados.
    Raises:
        FileNotFoundError si el fichero csv con las direcciones no existe
    """
    file = BASE_DIR / "direcciones.csv"

    if not os.path.exists(file):
        raise FileNotFoundError(f"Fichero {file} no encontrado en el PATH")

    columnas = ["VIA_CLASE", "VIA_PAR", "VIA_NOMBRE","NUMERO",  "LATITUD", "LONGITUD"]

    df = pd.read_csv(file, sep=";", usecols=columnas,encoding=  "latin1")

    df["VIA_COMPLETA"] = (
                        df["VIA_CLASE"].str.strip().str.title() +
                        " " +
                        df["VIA_PAR"].str.strip().str.lower() +
                        " " +
                        df["VIA_NOMBRE"].str.strip().str.title() +
                        ", " +
                        df["NUMERO"].apply(str).str.strip()
                        )

    df["LONGITUD"]= df["LONGITUD"].apply(hora_dec)
    df["LATITUD"]= df["LATITUD"].apply(hora_dec)

    return df
    



def busca_direccion(direccion:str, callejero:pd.DataFrame) -> Tuple[float,float]:
    """ Función que busca una dirección, dada en el formato
        calle, numero
    en el DataFrame callejero de Madrid y devuelve el par latitud, longitud) en grados de la
    ubicación geográfica de dicha dirección
    
    Args:
        direccion (str): Nombre completo de la calle con número, en formato "Calle, num"
        callejero (DataFrame): DataFrame con la información de las calles
    Returns:
        Tuple[float,float]: Par de float    coordsitud,longitud) de la dirección buscada, expresados en grados
    Raises:
        AdressNotFoundError: Si la dirección no existe en la base de datos
    Example:
        busca_direccion("Calle de Alberto Aguilera, 23", data)=(40.42998055555555,-3.7112583333333333)
        busca_direccion("Calle de Alberto Aguilera, 25", data)=(40.43013055555555,-3.7126916666666667)
    """
    vias = callejero["VIA_COMPLETA"].tolist()

    while True:

        # Top-5 coincidencias
        candidatos = process.extract(direccion, vias, limit=5)
        print("\nCoincidencias encontradas:")
        for i, (addr, score) in enumerate(candidatos, start=1):
            print(f"  {i}) {addr}  ({score}%)")

        eleccion = input(
            "Selecciona el número de la dirección (0 para volver a escribir, Enter vacío para cancelar): "
        ).strip()

        if eleccion == "":
            # cancelar selección → None
            return None

        if not eleccion.isdigit():
            print("Entrada no válida. Inténtalo de nuevo.")
            continue

        idx = int(eleccion)
        if idx == 0:
            continue

        if 1 <= idx <= len(candidatos):
            direccion_elegida = candidatos[idx - 1][0]
            fila = callejero[callejero["VIA_COMPLETA"] == direccion_elegida].iloc[0]
            lat = float(fila["LATITUD"])
            lon = float(fila["LONGITUD"])
            print(f"Has seleccionado: {direccion_elegida}")
            return lat, lon

        print("Número fuera de rango. Inténtalo de nuevo.")




############## Parte 4 ##############


def carga_grafo(file=None) -> nx.MultiDiGraph:
    """ Función que recupera el quiver de calles de Madrid de OpenStreetMap.
    Args: None
    Returns:
        nx.MultiDiGraph: Quiver de las calles de Madrid.
    Raises:
        ServiceNotAvailableError: Si no es posible recuperar el grafo de OpenStreetMap.
    """
    file = BASE_DIR / "madrid.graphml" if file is None else file
    try:
        if os.path.exists(file):
            print("Cargando grafo desde fichero")
            G = ox.load_graphml(file)
        else:
            print("Descargando grafo de OSM")
            G = ox.graph_from_place("Madrid, Spain", network_type="drive")
            ox.save_graphml(G, file)
            print(f"Grafo guardado como {file}")
    except:
        raise ServiceNotAvailableError

    return G



def procesa_grafo(multidigrafo:nx.MultiDiGraph) -> nx.DiGraph:
    """ Función que recupera el quiver de calles de Madrid de OpenStreetMap.
    Args:
        multidigrafo: multidigrafo de las calles de Madrid obtenido de OpenStreetMap.
    Returns:
        nx.DiGraph: Grafo dirigido y sin bucles asociado al multidigrafo dado.
    Raises: None
    """
    G = ox.convert.to_digraph(multidigrafo)
    loops = list(nx.selfloop_edges(G))
    if loops:
        G.remove_edges_from(loops)
    return G


def dibujar_grafo_osmnx(G):
    pos = {n: (G.nodes[n]["x"], G.nodes[n]["y"]) for n in G.nodes}

    print("Dibujando grafo procesado...")
    plt.figure(figsize=(12,12))

    nx.draw(G, pos=pos, node_size=1, width=0.1, edge_color="gray", arrows=True)

    plt.show()
    