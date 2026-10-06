"""
grafo.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP03B
Integrantes:
    - Miguel Pajuelo Gomez
    - Jorge Ois de Pascual

Descripción:
Librería para el análisis de grafos pesados.
"""

from typing import List,Tuple,Dict,Callable,Union
import networkx as nx
import sys

import heapq #Librería para la creación de colas de prioridad
from itertools import count

INFTY=sys.float_info.max #Distincia "infinita" entre nodos de un grafo

"""
En las siguientes funciones, las funciones de peso son funciones que reciben un grafo o digrafo y dos vértices y devuelven un real (su peso)
Por ejemplo, si las aristas del grafo contienen en sus datos un campo llamado 'valor', una posible función de peso sería:

def mi_peso(G:nx.Graph,u:object, v:object):
    return G[u][v]['valor']

y, en tal caso, para calcular Dijkstra con dicho parámetro haríamos

camino=dijkstra(G,mi_peso,origen, destino)


"""

def dijkstra(G:Union[nx.Graph, nx.DiGraph], peso:Union[Callable[[nx.Graph,object,object],float], Callable[[nx.DiGraph,object,object],float]], origen:object)-> Dict[object,object]:
    """ Calcula un Árbol de Caminos Mínimos para el grafo pesado partiendo
    del vértice "origen" usando el algoritmo de Dijkstra. Calcula únicamente
    el árbol de la componente conexa que contiene a "origen".
    
    Args:
        origen (object): vértice del grafo de origen
    Returns:
        Dict[object,object]: Devuelve un diccionario que indica, para cada vértice alcanzable
            desde "origen", qué vértice es su padre en el árbol de caminos mínimos.
    Raises:
        TypeError: Si origen no es "hashable".
    Example:
        Si G.dijksra(1)={2:1, 3:2, 4:1} entonces 1 es padre de 2 y de 4 y 2 es padre de 3.
        En particular, un camino mínimo desde 1 hasta 3 sería 1->2->3.
    """
    try:
        hash(origen)
    except TypeError:
        raise TypeError("Origen no es hasheable")

    if origen not in G:
        raise ValueError("El origen no pertenece al grafo")

    # Inicializamos padres, visitados y distancias
    padre = {v: None for v in G.nodes}
    visitado = {v: False for v in G.nodes}
    dist = {v: float("inf") for v in G.nodes}

    dist[origen] = 0.0

    # Cola de prioridad (distancia, vértice)
    # El contador desempata sin comparar los nodos, que pueden ser de tipos distintos.
    orden = count()
    cola: list[tuple[float, int, object]] = []
    heapq.heappush(cola, (dist[origen], next(orden), origen))

    # Bucle principal de Dijkstra
    while cola:
        d_v, _, v = heapq.heappop(cola)

        # Si ya está visitado, lo ignoramos
        if visitado[v]:
            continue

        visitado[v] = True

        # Relajamos las aristas salientes de v
        for x in G.neighbors(v):
            w_vx = peso(G, v, x)
            if dist[x] > dist[v] + w_vx:
                dist[x] = dist[v] + w_vx
                padre[x] = v
                heapq.heappush(cola, (dist[x], next(orden), x))

    # Devolvemos solo los vértices alcanzables distintos del origen
    return {v: padre[v] for v in G.nodes if visitado[v] and v != origen}




def camino_minimo(G:Union[nx.Graph, nx.DiGraph], peso:Union[Callable[[nx.Graph,object,object],float], Callable[[nx.DiGraph,object,object],float]] ,origen:object,destino:object)->List[object]:
    """ Calcula el camino mínimo desde el vértice origen hasta el vértice
    destino utilizando el algoritmo de Dijkstra.
    
    Args:
        G (nx.Graph o nx.Digraph): grafo a grado dirigido
        peso (función): función que recibe un grafo o grafo dirigido y dos vértices del mismo y devuelve el peso de la arista que los conecta
        origen (object): vértice del grafo de origen
        destino (object): vértice del grafo de destino
    Returns:
        List[object]: Devuelve una lista con los vértices del grafo por los que pasa
            el camino más corto entre el origen y el destino. El primer elemento de
            la lista es origen y el último destino.
    Example:
        Si dijksra(G,peso,1,4)=[1,5,2,4] entonces el camino más corto en G entre 1 y 4 es 1->5->2->4.
    Raises:
        TypeError: Si origen o destino no son "hashable".
    """
    for v, nombre in ((origen, "origen"), (destino, "destino")):
        try:
            hash(v)
        except TypeError:
            raise TypeError(f"{nombre} no es hasheable")

    if origen not in G or destino not in G:
        raise ValueError("origen o destino no pertenecen al grafo")

    if origen == destino:
        return [origen]

    padres = dijkstra(G, peso, origen)

    if destino not in padres:
        return []   # no hay camino

    camino = [destino]
    actual = destino
    while actual != origen:
        actual = padres[actual]
        camino.append(actual)

    camino.reverse()
    return camino


def prim(G:nx.Graph, peso:Callable[[nx.Graph,object,object],float])-> Dict[object,object]:
    """ Calcula un Árbol Abarcador Mínimo para el grafo pesado
    usando el algoritmo de Prim.
    
    Args: None
    Returns:
        G (nx.Graph): grafo
        peso (función): función que recibe un grafo y dos vértices del grafo y devuelve el peso de la arista que los conecta
        Dict[object,object]: Devuelve un diccionario que indica, para cada vértice del
            grafo, qué vértice es su padre en el árbol abarcador mínimo.
    Raises: None
    Example:
        Si prim(G,peso)={1: None, 2:1, 3:2, 4:1} entonces en un árbol abarcador mínimo tenemos que:
            1 es una raíz (no tiene padre)
            1 es padre de 2 y de 4
            2 es padre de 3
    """
    if len(G.nodes) == 0:
        return {}

    padre: Dict[object, object] = {v: None for v in G.nodes}
    coste_minimo: Dict[object, float] = {v: float("inf") for v in G.nodes}

    # Elegimos una raíz arbitraria
    raiz = next(iter(G.nodes))
    coste_minimo[raiz] = 0.0

    # Q: vértices aún no incorporados al AAM
    Q = list(G.nodes)

    while Q:
        # v = vértice de Q con menor coste_minimo
        v = min(Q, key=lambda u: coste_minimo[u])
        Q.remove(v)

        # Recorremos N_v ∩ Q
        for x in G.neighbors(v):
            if x not in Q:        # ya fijado
                continue
            w_vx = peso(G, v, x)
            if w_vx < coste_minimo[x]:
                coste_minimo[x] = w_vx
                padre[x] = v

    return padre
                

def kruskal(G:nx.Graph, peso:Callable[[nx.Graph,object,object],float])-> List[Tuple[object,object]]:
    """ Calcula un Árbol Abarcador Mínimo para el grafo
    usando el algoritmo de Kruskal.
    
    Args:
        G (nx.Graph): grafo
        peso (función): función que recibe un grafo y dos vértices del grafo y devuelve el peso de la arista que los conecta
    Returns:
        List[Tuple[object,object]]: Devuelve una lista [(s1,t1),(s2,t2),...,(sn,tn)]
            de los pares de vértices del grafo que forman las aristas
            del arbol abarcador mínimo.
    Raises: None
    Example:
        En el ejemplo anterior en que prim(G,peso)={1:None, 2:1, 3:2, 4:1} podríamos tener, por ejemplo,
        kruskal(G,peso)=[(1,2),(1,4),(3,2)]
    """
    # 1) Lista de aristas ordenada por su peso
    #    L = [(u,v), ...] con orden creciente por peso
    L = list(G.edges())
    L.sort(key=lambda e: peso(G, e[0], e[1]))

    # Componente C[v] = conjunto de vértices de su componente
    C = {v: {v} for v in G.nodes}

    aristas_aam: List[Tuple[object, object]] = []

    for (u, v) in L:
        if C[u] is not C[v]:         # componentes distintas
            aristas_aam.append((u, v))

            nueva_comp = C[u] | C[v]
            for w in nueva_comp:
                C[w] = nueva_comp

            if len(aristas_aam) == len(G.nodes) - 1:
                break

    return aristas_aam
