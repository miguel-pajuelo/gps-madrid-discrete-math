# Procedencia y selección de versiones

Autores indicados en código y memorias: Miguel Pajuelo Gómez y Jorge Ois de Pascual. Los materiales pertenecen a las prácticas de Matemática Discreta de ICAI y conservan sus cabeceras académicas y el contexto de material docente.

## GPS, proyecto principal

Se seleccionan `gps.py`, `callejero.py`, `grafo_pesado.py`, `test_grafo.py`, los datos y la memoria de `Practica 3`. `callejero.py` se adapta para localizar los datos junto al módulo. En Dijkstra se añade un contador para desempatar prioridades sin comparar nodos de tipos diferentes: el script de ejemplo mezcla enteros y texto, y la cola original podía lanzar `TypeError`. Se mantiene la relajación y el cálculo de caminos del algoritmo. `gps.py` comprueba la cancelación de una dirección antes de desempaquetar sus coordenadas, evitando el error cuando `busca_direccion` devuelve `None`. Los requisitos originales se complementan con una versión compatible de NumPy y `scikit-learn`, usado por OSMnx para buscar nodos cercanos en coordenadas geográficas.

## Práctica 1

Se usa `P1G03B`, la versión de entrega, con su memoria y pruebas. Comparada con trabajo, conserva mejor el contrato de excepciones esperado por las pruebas: 74/85 pasan en entrega frente a 73/85 en trabajo. Ambas mantienen incompletos Bézout múltiple, raíces y ecuaciones cuadráticas; se documentan esas carencias. La versión de trabajo incorpora Pollard Rho y otros cambios y permanece en el archivo local, sin mezclarla con esta copia.

Los ejemplos y el notebook de exploración proceden de trabajo y son recursos complementarios. Su procedencia no implica que todos sus cálculos funcionen con la versión de entrega.

## Práctica 2

Se conserva la biblioteca `modular.py` propia de esta práctica junto a `rsa.py` y sus aplicaciones y pruebas. La práctica estaba originalmente dentro de `Practica 1`, pero se separa en esta copia porque es un bloque distinto. El GPS no depende de ella. Se excluyen los archivos originales de claves privadas y de usuarios; cada usuario de la aplicación puede generar los suyos localmente. `X.txt` es la entrada cifrada del ejercicio de ataque e incluye una clave pública; se conserva para que `prueba.py` tenga su recurso de entrada. El texto descifrado se genera localmente y no se distribuye como salida guardada.

## Cuadernos y datos

Las celdas de los cuatro notebooks se conservan; se retiran salidas y metadatos de ejecución. El notebook de grafos procede de `Practica 3/P3.ipynb`; el de exploración del GPS, de `Practica 3/.../prueba.ipynb`. Se conservan los datos originales del GPS y se documenta su procedencia en [gps/DATOS.md](gps/DATOS.md). No se copian entornos, cachés, ejecutables de intérpretes ni resultados masivos del benchmark.
