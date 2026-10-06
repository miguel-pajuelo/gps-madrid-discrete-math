# RSA y aplicaciones didácticas

Práctica 2 de Matemática Discreta, Miguel Pajuelo Gómez y Jorge Ois de Pascual. `rsa.py` utiliza la versión de `modular.py` conservada en esta misma carpeta.

Incluye generación de claves, padding decimal, cifrado y descifrado de enteros y cadenas, recuperación de una clave por factorización y un ataque didáctico a caracteres cifrados sin padding. Usa la biblioteca estándar de Python.

Desde esta carpeta se puede comprobar un cifrado de ejemplo, sin crear archivos de claves:

```sh
python -c "import rsa; n,e,d=rsa.generar_claves(1000,10000); c=rsa.cifrar_cadena_rsa('Hola',n,e,1); print(rsa.descifrar_cadena_rsa(c,n,d,1))"
```

Para usar la interfaz de terminal, crear usuarios de prueba con `python registrarusuario.py` y ejecutar `python criptochat.py usuario1 usuario2`. Los archivos de claves se guardan en `Usuarios/` y se excluyen de Git. La aplicación cifra y descifra en terminal; no envía mensajes por red.

`python prueba.py` ejecuta el ataque didáctico sobre el `X.txt` incluido, que contiene el cifrado del ejercicio y una clave pública. Escribe `X_descifrado.txt` localmente, excluido de Git. No se distribuyen las claves privadas ni los mensajes de los usuarios originales. El notebook conserva una exploración matemática con las salidas antiguas retiradas.

Las **58 pruebas existentes pasan**. Ejecutarlas con `python -m pytest tests` después de instalar `pytest`. Estas pruebas verifican casos académicos; `random` y el padding decimal no ofrecen garantías de criptografía de producción. El GPS es independiente de este bloque.
