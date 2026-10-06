# Biblioteca modular e IMatLab

Práctica 1 de Matemática Discreta, Miguel Pajuelo Gómez y Jorge Ois de Pascual. Se conserva la versión de entrega `P1G03B`.

`modular.py` reúne funciones de aritmética modular; `imatlab.py` permite usarlas mediante comandos interactivos o por lotes. Es una aplicación de Python y no requiere MATLAB de MathWorks. La biblioteca utiliza módulos de la biblioteca estándar.

Desde esta carpeta:

```sh
python imatlab.py
python imatlab.py ejemplosComandos.txt salida_local.txt
python -m pytest tests
```

Instalar `pytest` desde el `requirements-dev.txt` de la raíz si se quieren ejecutar las pruebas. Las pruebas existentes dan **74 correctas y 11 fallidas**: `bezout_n`, `raiz_mod_p` y `ecuacion_cuadratica` están incompletas. Los comandos de raíces y ecuaciones cuadráticas de `ejemplosComandos.txt` no producen todas las salidas esperadas de `ejemplosSalida.txt`.

`imatlab_benchmark.py` conserva sus ocho archivos de entrada junto al código. Las salidas del benchmark se generan localmente y se excluyen de Git; no se ha repetido ese benchmark completo ni se han certificado sus tiempos. `exploracion_modular.ipynb` conserva un cuaderno del ejercicio, cuya ejecución completa tampoco se ha repetido. La memoria está en [documentacion/memoria_modular_imatlab.pdf](../../documentacion/memoria_modular_imatlab.pdf).

Este bloque es independiente del GPS y no debe compartir su módulo `modular.py` con RSA, que conserva otra versión.
