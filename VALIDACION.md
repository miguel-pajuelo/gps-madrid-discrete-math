# Comprobaciones de preparación

Fecha: 6 de octubre de 2026. Python 3.12.14; NumPy 1.26.4, Matplotlib 3.8.4, pandas 2.2.2, NetworkX 3.2.1, OSMnx 2.0.1, scikit-learn 1.5.2 y SciPy 1.13.1 en la comprobación del GPS.

## GPS

- Callejero cargado: 213.811 direcciones.
- GraphML local cargado: 31.388 nodos y 61.742 aristas.
- Una ruta por distancia, otra por tiempo y otra por tiempo con penalización de semáforos se han contrastado con NetworkX sobre el mismo grafo procesado: sus costes coinciden.
- La búsqueda de un nodo cercano y la generación de instrucciones se han ejecutado con datos locales. No se ha descargado nueva cartografía.
- Dijkstra, Prim y Kruskal se han contrastado en un grafo pequeño con el resultado de NetworkX. Se comprueba también un destino desconectado.
- Se comprueba el desempate de Dijkstra con nodos de tipos diferentes, y el script original `test_grafo.py` se ejecuta sin error.
- La cancelación de origen y destino se comprueba sin ejecutar la interfaz gráfica.

Estas pruebas verifican los casos indicados; no certifican todas las rutas de Madrid, las velocidades de las calles, la exactitud física del tiempo de viaje ni las ventanas de Matplotlib. La prueba por semáforos valida el modelo del ejercicio, no datos de semáforos reales.

## Prácticas complementarias

| Suite original | Correctas | Fallidas | Estado |
|---|---:|---:|---|
| IMatLab / modular, versión de entrega | 74 | 11 | Funciones incompletas documentadas. |
| RSA, versión de la práctica 2 | 58 | 0 | Casos existentes comprobados. |

Los fallos de la práctica 1 afectan a `bezout_n`, `raiz_mod_p` y `ecuacion_cuadratica` y sus comandos de IMatLab. Se mantienen las pruebas fallidas; no se ocultan ni se completan las funciones durante esta preparación. El candidato de trabajo dio 73 correctas y 12 fallidas, por una diferencia adicional en el contrato de excepciones de la inversa modular.

## Notebooks

Los cuatro notebooks conservan sus celdas originales; se retiran las salidas antiguas y los contadores de ejecución. Su estructura se valida con `nbformat`. No se ha ejecutado cada notebook completo: son cuadernos originales de exploración, y algunos dependen de funciones incompletas o de estado interactivo.

Para comprobar uno de ellos localmente, instalar Jupyter e ipykernel en el entorno del bloque, situarse en la carpeta del notebook y ejecutar `python -m jupyter nbconvert --execute --to notebook --output notebook_validado NOMBRE.ipynb`. Revisar los resultados y gráficos del archivo generado; esta preparación no presenta esos cuadernos como experimentos reproducidos.
