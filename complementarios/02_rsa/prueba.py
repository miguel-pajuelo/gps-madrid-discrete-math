"""
decrypt_x.py

Script para descifrar el mensaje X.txt usando un ataque de texto elegido
sobre RSA sin padding.
"""

from rsa import ataque_texto_elegido

def leer_mensaje_cifrado(archivo: str) -> tuple[int, int, list[int]]:
    """Lee el archivo con el mensaje cifrado y extrae n, e y la lista de valores cifrados.
    
    Args:
        archivo (str): Ruta del archivo con el mensaje cifrado
    
    Returns:
        tuple: (n, e, cList) donde n y e son la clave pública y cList es la lista de enteros cifrados
    """
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    lineas = contenido.strip().split('\n')
    
    # Primera línea contiene "Clave pública: n e"
    clave_publica = lineas[0].split(': ')[1].split()
    n = int(clave_publica[0])
    e = int(clave_publica[1])
    
    # Buscar la línea que contiene "X:" y tomar todo lo que viene después
    encontrado_x = False
    numeros_texto = []
    
    for linea in lineas:
        if linea.strip().startswith('X:'):
            # Esta línea contiene "X:" seguido de números
            # Extraemos todo después de "X:"
            contenido_linea = linea.split('X:')[1].strip()
            if contenido_linea:
                numeros_texto.append(contenido_linea)
            encontrado_x = True
        elif encontrado_x and linea.strip():
            # Líneas después de "X:" que contienen números
            numeros_texto.append(linea.strip())
    
    # Unir todos los números y convertirlos a lista de enteros
    texto_completo = ' '.join(numeros_texto)
    cList = [int(num) for num in texto_completo.split()]
    
    return n, e, cList


def main():
    """Función principal que ejecuta el descifrado."""
    
    print("="*60)
    print("DESCIFRADO DE MENSAJE RSA SIN PADDING")
    print("="*60)
    
    # Leer el archivo
    archivo = "X.txt"
    print(f"\n[1] Leyendo archivo '{archivo}'...")
    
    try:
        n, e, cList = leer_mensaje_cifrado(archivo)
        
        print(f"\n[2] Clave pública extraída:")
        print(f"    n = {n}")
        print(f"    e = {e}")
        print(f"\n[3] Número de caracteres cifrados: {len(cList)}")
        
        # Ejecutar el ataque
        print(f"\n[4] Ejecutando ataque de texto elegido...")
        print("    (Esto puede tardar unos segundos...)")
        
        texto_descifrado = ataque_texto_elegido(cList, n, e)
        
        print(f"\n[5] ¡Descifrado exitoso!")
        print("="*60)
        print("\nMENSAJE DESCIFRADO:")
        print("="*60)
        print(texto_descifrado)
        print("="*60)
        
        # Guardar el resultado en un archivo
        with open("X_descifrado.txt", 'w', encoding='utf-8') as f:
            f.write(texto_descifrado)
        
        print(f"\n[6] Mensaje guardado en 'X_descifrado.txt'")
        
    except FileNotFoundError:
        print(f"\n[ERROR] No se encontró el archivo '{archivo}'")
    except ValueError as e:
        print(f"\n[ERROR] Error al descifrar: {e}")
    except Exception as e:
        print(f"\n[ERROR] Error inesperado: {e}")


if __name__ == "__main__":
    main()