"""
gps.py

Miguel Pajuelo Gómez & Jorge Ois de Pascual

Aplicación de navegación para la práctica de Matemática Discreta - IMAT (ICAI).

Usa:
- callejero.py: carga de direcciones, grafo OSM y velocidades por tipo de vía
- grafo_pesado.py: Dijkstra y camino mínimo
"""

from typing import List, Tuple, Optional
import math

import re
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from callejero import *
from grafo_pesado import camino_minimo

P_SEMAFORO = 0.8
TIEMPO_PARADA = 30
TIEMPO_TOTAL = P_SEMAFORO*TIEMPO_PARADA

DEFAULT_SPEED = 50

def peso_distancia(G: nx.Graph, u: object, v: object) -> float:
    """
    Peso = longitud en metros de la arista (u, v).
    """
    return G[u][v]["length"]

def peso_tiempo(G: nx.Graph, u: object, v: object) -> float:
    """
    Peso = tiempo (en segundos) para recorrer la arista (u, v)
    a la velocidad máxima de la vía.
    """
    longitud = float(G[u][v].get("length", 0.0))

    velocidad = G[u][v].get("maxspeed", None)

    if isinstance(velocidad, list):
        velocidad = velocidad[0]

    if isinstance(velocidad, str):
        nums = re.findall(r"\d+", velocidad)
        if nums:
            velocidad = float(nums[0])
        else:
            velocidad = None

    if isinstance(velocidad, (int, float)):
        velocidad = float(velocidad)

    if velocidad is None:
        tipo = G[u][v].get("highway", None)
        if isinstance(tipo, list):
            tipo = tipo[0]
        velocidad = float(MAX_SPEEDS.get(tipo, DEFAULT_SPEED))

    velocidad_ms = velocidad * 1000.0 / 3600.0

    return longitud / velocidad_ms

def peso_tiempo_semaforos(G: nx.Graph, u: object, v: object) -> float:
    """
    Peso = tiempo esperado (segundos) = tiempo de vía + retardo esperado por semáforo.

    Suponemos que cada arista implica atravesar un cruce con probabilidad p de parar 30 s.
    (modelo sencillo por arista).
    """
    return peso_tiempo(G, u, v) + TIEMPO_TOTAL 


def calcular_giro(G: nx.Graph, u: object, v: object, w: object) -> str:
    """
    Determina si el giro en 'v' al pasar de u->v a v->w es a la izquierda, derecha o recto,
    usando la señal del ángulo entre vectores.

    Devuelve "izquierda", "derecha" o "recto".
    """
    x1, y1 = G.nodes[u]["x"], G.nodes[u]["y"]
    x2, y2 = G.nodes[v]["x"], G.nodes[v]["y"]
    x3, y3 = G.nodes[w]["x"], G.nodes[w]["y"]

    
    in_vec = (x2 - x1, y2 - y1) # Vector entrada
    out_vec = (x3 - x2, y3 - y2) # Vector salida

    cross = in_vec[0] * out_vec[1] - in_vec[1] * out_vec[0]
    dot = in_vec[0] * out_vec[0] + in_vec[1] * out_vec[1]

    ang = math.atan2(cross, dot)

    if ang > 0.3:
        return "izquierda"
    elif ang < -0.3:
        return "derecha"
    else:
        return "recto"


def generar_instrucciones(G: nx.Graph, camino: List[object]) -> List[str]:
    """
    A partir de una lista de nodos [n0, n1, ..., nk], genera instrucciones de navegación:

    - Distancia a recorrer por cada calle.
    - Nombre de la siguiente calle.
    - Giro a izquierda/derecha cuando se cambia de calle.
    """

    instrucciones = []

    if len(camino) < 2:
        instrucciones.append("Ya estás en tu destino.")
        return instrucciones

    edges_info = []
    for u, v in zip(camino[:-1], camino[1:]):
        length = float(G[u][v].get("length", 0.0))
        street = G[u][v].get("name", "(vía sin nombre)")
        edges_info.append((u, v, length, street))

    current_street = edges_info[0][3]
    current_dist = edges_info[0][2]

    for i in range(1, len(edges_info)):
        u_prev, v_prev, length_prev, street_prev = edges_info[i - 1]
        u, v, length, street = edges_info[i]

        if street == current_street:
            current_dist += length
        else:
            instrucciones.append(f"Sigue {int(round(current_dist))} m por {current_street}.")

            if i >= 2:
                u_before = edges_info[i - 2][0]
            else:
                u_before = u_prev
            
            giro = calcular_giro(G, u_before, u_prev, v)

            if giro == "recto":
                instrucciones.append(f"Sigue recto y entra en {street}.")
            else:
                instrucciones.append(f"Gira a la {giro} hacia {street}.")
            
            current_street = street
            current_dist = length

    instrucciones.append(f"{round(current_dist)} m por {current_street} hasta tu destino.")

    return instrucciones


def mostrar_ruta(G_base: nx.Graph, camino: List[object]) -> None:
    """
    Dibuja el grafo completo en gris y la ruta indicada en rojo.
    """
    pos = {n: (G_base.nodes[n]["x"], G_base.nodes[n]["y"]) for n in G_base.nodes}

    plt.figure(figsize=(12, 12))

    # Grafo base
    nx.draw(
        G_base,
        pos=pos,
        node_size=1,
        width=0.3,
        edge_color="lightgray",
        arrows=False,
    )

    # Ruta
    edges_ruta = list(zip(camino[:-1], camino[1:]))
    nx.draw_networkx_edges(
        G_base,
        pos=pos,
        edgelist=edges_ruta,
        width=2.0,
        edge_color="red",
        arrows=True,
    )
    nx.draw_networkx_nodes(
        G_base,
        pos=pos,
        nodelist=camino,
        node_size=5,
        node_color="blue",
    )

    plt.title("Ruta seleccionada")
    plt.axis("off")
    plt.tight_layout()
    plt.show()



def main():
    print("=== Navegador Madrid (Práctica Discreta) ===")

    # 1) Carga de callejero y grafo
    print("Cargando callejero de direcciones...")
    df_callejero = carga_callejero()

    print("Cargando grafo de calles.")
    G_multi = carga_grafo()
    G = procesa_grafo(G_multi)

    # 2) Selección de direcciones
    while True:
        print("\nIntroduce origen y destino (Enter vacío para terminar).")

        origen_raw = input("Origen: ").strip()
        if origen_raw == "":
            print("Fin de la aplicación.")
            break
        origen = busca_direccion(origen_raw, df_callejero)
        if origen is None:
            continue
        origen_lat, origen_lon = origen

        destino_raw = input("Destino: ").strip()
        if destino_raw == "":
            print("Fin de la aplicación.")
            break

        destino = busca_direccion(destino_raw, df_callejero)
        if destino is None:
            continue
        destino_lat, destino_lon = destino

        # Nodos más cercanos en el grafo
        try:
            nodo_origen = ox.distance.nearest_nodes(G_multi, origen_lon, origen_lat)
            nodo_destino = ox.distance.nearest_nodes(G_multi, destino_lon, destino_lat)
        except Exception as e:
            print(f"Error localizando nodos en el grafo: {e}")
            continue

        if nodo_origen not in G or nodo_destino not in G:
            print("No se ha encontrado un camino entre origen y destino en el grafo.")
            continue

        # 3) Selección de modo de ruta
        print("\nModo de cálculo de ruta:")
        print("  1) Ruta más corta (distancia en metros)")
        print("  2) Ruta más rápida (tiempo sin semáforos)")
        print("  3) Ruta más rápida (tiempo esperado con semáforos)")

        modo = input("Elige opción [1-3]: ").strip()

        if modo == "1":
            peso = peso_distancia
            modo = "metros"
        elif modo == "2":
            peso = peso_tiempo
            modo = "tiempo sin semáforos"
        elif modo == "3":
            peso = peso_tiempo_semaforos
            modo = "tiempo esperado con semáforos"
        else:
            print("Opción no válida.")
            continue

        # 4) Calculo de la ruta
        try:
            camino = camino_minimo(G, peso, nodo_origen, nodo_destino)
        except Exception as e:
            print(f"Error calculando el camino mínimo: {e}")
            continue

        if not camino:
            print("No existe un camino entre origen y destino.")
            continue

        print(f"Ruta mas rapida ({modo}) calculada. Nodos en el camino: {len(camino)}")

        # 5) Lista de instrucciones
        instrucciones = generar_instrucciones(G, camino)

        for i, instr in enumerate(instrucciones, start=1):
            print(f" {i}. {instr}")
        
        #6) Mostrar ruta 
        mostrar_ruta(G_multi, camino)

if __name__ == "__main__":
    main()
