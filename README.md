# GPS de Madrid y aplicaciones de Matemática Discreta

Proyecto académico de **Miguel Pajuelo Gómez y Jorge Ois de Pascual**, ICAI, Universidad Pontificia Comillas.

El proyecto principal es un navegador de Madrid que convierte direcciones en nodos de un grafo y calcula rutas mediante Dijkstra. Se acompañan dos prácticas independientes: una biblioteca de aritmética modular con interfaz IMatLab y aplicaciones didácticas de RSA.

## Cómo recorrer este repositorio

| Bloque | Contenido | Relación con el GPS |
|---|---|---|
| [gps/](gps/) | Callejero, grafo de Madrid, Dijkstra, rutas e instrucciones. | Proyecto final de la asignatura. |
| [01_modular_imatlab/](complementarios/01_modular_imatlab/) | Biblioteca modular, consola IMatLab, benchmark, ejemplos y pruebas. | Práctica complementaria; el GPS no la importa. |
| [02_rsa/](complementarios/02_rsa/) | RSA, padding, cifrado de cadenas, registro de usuarios y chat. | Práctica complementaria; utiliza su propia `modular.py`. |
| [documentacion/](documentacion/) | [Memoria del GPS](documentacion/memoria_gps.docx) y [memoria de la práctica 1](documentacion/memoria_modular_imatlab.pdf). | Documentos originales seleccionados. |

IMatLab es una interfaz escrita en Python; no requiere MATLAB de MathWorks. Las prácticas 1 y 2 aportan otros contenidos de la asignatura, pero no son dependencias de ejecución de la práctica 3. Mantenerlas separadas evita mezclar sus bibliotecas `modular.py`, que son versiones diferentes. Consultar [PROCEDENCIA.md](PROCEDENCIA.md).

## Ejecutar el GPS

Se conserva el entorno de requisitos del proyecto, con Python 3.12 como versión usada en la comprobación local. Crear y activar un entorno nuevo:

```sh
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# Linux:   . .venv/bin/activate
python -m pip install -r requirements.txt
python gps/gps.py
```

El programa solicita origen y destino, ofrece coincidencias de direcciones y permite elegir ruta por distancia, tiempo o tiempo con penalización estimada de semáforos. Después genera instrucciones y dibuja el recorrido.

La copia incluye `gps/direcciones.csv` y `gps/madrid.graphml`; con ese grafo, la carga normal no necesita descargar de nuevo Madrid. El tiempo de recorrido procede de longitudes y velocidades de vía. La penalización de semáforos añade un valor esperado de 24 segundos por arista: es un modelo didáctico, no tráfico observado ni navegación en tiempo real.

`grafo_pesado.py` incluye Dijkstra, reconstrucción del camino, Prim y Kruskal. Sus algoritmos deben usarse con las condiciones del ejercicio, por ejemplo pesos no negativos para Dijkstra. El grafo vial procede de OpenStreetMap; véase [gps/DATOS.md](gps/DATOS.md).

## Ejecutar IMatLab

La práctica 1 usa la biblioteca estándar de Python. Desde `complementarios/01_modular_imatlab`:

```sh
python imatlab.py
python imatlab.py ejemplosComandos.txt salida_local.txt
```

Ejemplos de comandos: `primo(7)`, `factorizar(8)`, `mcd(12,18)` e `inv(3,7)`. El benchmark y el notebook conservan el contexto de los ejercicios.

El material original tiene funciones incompletas: `bezout_n`, `raiz_mod_p` y `ecuacion_cuadratica`. Las pruebas de la versión seleccionada dan **74 correctas y 11 fallidas**. Por ello se presenta como práctica académica con límites conocidos, no como biblioteca modular completa. Las funciones no se han reescrito durante el empaquetado. `ejemplosSalida.txt` contiene las salidas esperadas del ejercicio; algunas, como raíces y ecuaciones cuadráticas, no se reproducen con las funciones incompletas.

## Ejecutar RSA y las aplicaciones didácticas

Desde `complementarios/02_rsa`, ejecutar `python registrarusuario.py` para crear usuarios de prueba y después `python criptochat.py usuario1 usuario2` para cifrar o descifrar texto mediante los archivos de claves de esos usuarios. El chat es una interfaz de cifrado/descifrado en terminal, no un servicio de mensajería en red.

Las claves y mensajes de los usuarios originales no se incluyen. `X.txt` conserva el texto cifrado del ejercicio y su clave pública para ejecutar el ataque didáctico con `python prueba.py`; el resultado se genera localmente como `X_descifrado.txt`, excluido de Git. Las **58 pruebas existentes de RSA pasan**. Este resultado verifica los casos de la práctica; el padding decimal y el uso de `random` no acreditan seguridad criptográfica de producción.

## Pruebas y notebooks

Instalar `requirements-dev.txt` para las pruebas. Ejecutar cada suite desde su carpeta para mantener las bibliotecas separadas:

```sh
# Desde complementarios/01_modular_imatlab:
python -m pytest tests
# Desde complementarios/02_rsa:
python -m pytest tests
```

Los cuatro notebooks se incluyen como cuadernos de exploración con sus celdas originales y sin salidas antiguas. Para ejecutarlos, instalar Jupyter, abrir cada notebook desde su propia carpeta y usar el entorno con las dependencias de ese bloque. Sus cálculos no se han certificado mediante una nueva ejecución completa. El estado del GPS, las pruebas y los notebooks se detalla en [VALIDACION.md](VALIDACION.md).
