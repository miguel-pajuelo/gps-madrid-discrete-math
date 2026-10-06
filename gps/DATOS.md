# Datos del GPS

`madrid.graphml` y `direcciones.csv` se copian íntegros del material de la práctica 3. El grafo se carga con OSMnx y representa calles de Madrid; `callejero.py` incluye la descarga alternativa desde OpenStreetMap cuando no hay un GraphML local.

Cartografía: [© OpenStreetMap contributors](https://www.openstreetmap.org/copyright). El grafo vial se distribuye bajo [Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/1-0/). Esta atribución se refiere al grafo vial; la entrega no identifica en sus archivos el enlace de descarga ni las condiciones específicas de la tabla `direcciones.csv`, por lo que no se le asigna una procedencia adicional no comprobada.

El CSV contiene direcciones y coordenadas y se lee con separador `;` y codificación Latin-1. El código usa `VIA_CLASE`, `VIA_PAR`, `VIA_NOMBRE`, `NUMERO`, `LATITUD` y `LONGITUD`. El grafo estático y las direcciones documentan el ejercicio; no acreditan que la red vial ni sus velocidades reflejen el estado actual.

Ambos archivos superan 25 MiB y permanecen por debajo de 100 MiB. Para subir la carpeta completa, usar Git desde el ordenador: la [documentación de GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) limita las cargas por navegador a 25 MiB y los archivos de Git normal a 100 MiB. Esta carpeta no necesita Git LFS para sus archivos actuales.
