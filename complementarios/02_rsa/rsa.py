"""
rsa.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP03B
Integrantes:
    - Miguel Pajuelo Gomez
    - Jorge Ois de Pascual

Descripción:
Librería para la realización de cifrado y descifrado usando el algoritmo RSA.
"""
from modular import *
import random
from typing import Tuple,List


def generar_claves(min_primo:int,max_primo:int)-> Tuple[int,int,int]:
    """Toma dos primos entre min_primo (incluido) y max_primo (excluido) y devuelve
    n,e,d
    donde (n,e) es la clave pública y d la clave privada para RSA

    Args:
        min_primo (int): Límite inferior para los primo p1 y p2 usados en la clave
        max_primo (int): Límite superior para los primo p1 y p2 usados en la clave
    
    Returns:
        n (int): Módulo para RSA, formado por el producto de dos primos p1 y p2 tales que
            min_primo<=p1, p2 < max_primo
        e (int): Exponente de la clave pública para RSA con módulo n=p1*p2
        d (int): Exponente de la clave privada para RSA con módulo n

    Raises:
        ValueError: Si no es posible encontrar una pareja de primos distintos p1,p2 entre min_primo y max_primo
    """

    if min_primo < 2:
        raise ValueError("Limite inferior del intervalo demasiado pequeño")

    densidad_primos1 = int(min_primo* (1/math.log(min_primo)))
    densidad_primos2 = int(max_primo* (1/math.log(max_primo)))

    if densidad_primos2-densidad_primos1 < 10:
        raise ValueError("Los valores del intervalo deben sestar más separados")
    
    p = random.randint(min_primo, max_primo)
    q = random.randint(min_primo, max_primo)

    while not es_primo(p) or not es_primo(q) or p == q:
        if not es_primo(p):
            p = random.randint(min_primo, max_primo)

        if not es_primo(q):
            q = random.randint(min_primo, max_primo)

        if p == q:
            p = random.randint(min_primo, max_primo)

    n = p*q
    fi_n = (p-1)*(q-1)
    e = random.randint(2, fi_n - 1)

    while mcd(e, fi_n) != 1:
        e = random.randint(2, fi_n - 1)

    d = inversa_mod_p(e, fi_n)
    
    return n, e, d



def aplicar_padding(m:int,digitos_padding:int)->int:
    """Dado un mensaje y un número de dígitos de padding, añade
    digitos_padding cifras aleatorias a la derecha del mensaje
    
    Args:
        m (int): Mensaje sin padding
        digitos_padding (int): Número no negativo de cifras de padding
    
    Returns:
        int: entero formado por los dígitos de m seguidos de digitos_padding cifras aleatorias.

    Raises: None

    Example:
        aplicar_padding(24,2)=2419
        aplicar_padding(24,2)=2403
        aplicar_padding(24,3)=24718
        aplicar_padding(24,3)=24845
        aplicar_padding(24,0)=24
    """
    if digitos_padding < 0:
        raise ValueError("digitos_padding debe ser un entero no negativo")
    if m < 0:
        raise ValueError("m debe ser un entero no negativo")

    mensaje = str(m)

    for _ in range(digitos_padding):
        mensaje += str(random.randint(0,9))
    
    return int(mensaje)


def eliminar_padding(m:int,digitos_padding:int)->int:
    """Dado un mensaje con padding de digitos_padding cifras al
    final del mismo, elimina dichas cifras aleatorias y devuelve
    el resto de cifras del mensaje

    Args:
        m (int): Mensaje con padding
        digitos_padding (int): Número no negativo de cifras de padding
    
    Returns:
        int: entero resultante de eliminar las últimas digitos_padding cifras de m.

    Raises: None
    
    Example:
        eliminar_padding(2454,1)=245
        eliminar_padding(2454,2)=24
        eliminar_padding(2454,3)=2
        eliminar_padding(2432,2)=24
        eliminar_padding(2432,0)=2432
    """

    if digitos_padding < 0:
        raise ValueError("digitos_padding debe ser un entero no negativo")
    
    if m < 0:
        raise ValueError("m debe ser un entero no negativo")

    if digitos_padding == 0:
        return m

    mensaje = str(m)
    if digitos_padding >= len(mensaje):
        return 0
    return int(mensaje[:-digitos_padding])  


def cifrar_rsa(m:int,n:int,e:int,digitos_padding:int)->int:
    """Dado un mensaje m entero, un módulo y exponente que formen parte
    de una clave pública de RSA, con m<n*10^{-digitos_padding}, y un número
    de dígitos de padding, aplica el padding al mensaje y lo cifra
    usando RSA con módulo n y exponente e.
    
    Args:
        m (int): Mensaje original claro (sin padding)
        n (int): Módulo de la clave pública de RSA
        e (int): Exponente de la clave pública de RSA
        digitos_padding (int): Número no negativo de cifras de padding
    
    Returns:
        int: entero resultante de agregar el padding a m y aplicar RSA.

    Raises: None
    """

    if m < 0:
        raise ValueError("m debe ser un entero no negativo")
    
    if digitos_padding < 0:
        raise ValueError("digitos_padding debe ser un entero no negativo")

    m_pad = aplicar_padding(m, digitos_padding)

    return potencia_mod_p(m_pad, e, n)



def descifrar_rsa(c:int,n:int,d:int,digitos_padding:int)->int:
    """Dado un cifrado c entero que haya sido cifrado con RSA usando
    digitos_padding cifras de padding al final del mensaje y el 
    módulo y exponente privado, n y d que formen la clave privada de RSA cuya pareja se
    utilizó para cifrar c, descifra c y elimina el padding, devolviendo
    el mensaje original.

    Args:
        c (int): Mensaje original claro (sin padding)
        n (int): Módulo de la clave pública de RSA usado para cifrar
        d (int): Exponente de la clave privada de RSA cuya pareja se utilizó para cifrar c
        digitos_padding (int): Número no negativo de cifras de padding usados para cifrar c
    
    Returns:
        int: entero resultante de descifrar c usando RSA con módulo m y exponente e y después eliminar el padding al resultado.

    Raises: None
    """
    
    if digitos_padding < 0:
        raise ValueError("digitos_padding debe ser un entero no negativo")
    if c < 0:
        raise ValueError("c debe ser un entero no negativo")

    m_pad = potencia_mod_p(c, d, n)

    if digitos_padding == 0:
        return m_pad
    
    m = eliminar_padding(m_pad, digitos_padding)

    if m < 0:
        raise ValueError("Mensaje resultante inválido (negativo) después de eliminar padding")

    return m
    


def codificar_cadena(s:str)->List[int]:
    """Convierte una cadena de caracteres a la lista de
    enteros que representa el valor unicode cada uno de sus caracteres.

    Args:
        s (str): cadena en texto plano

    Returns:
        int: lista de enteros que representan el código unicode de cada carácter de la cadena s.

    Raises: None.

    Example:
        codificar_cadena("¡Hola mundo!")=[161, 72, 111, 108, 97, 32, 109, 117, 110, 100, 111, 33]
    """
    return [ord(c) for c in s]


def decodificar_cadena(m:List[int])->str:
    """Convierte una lista de enteros que representen caracteres unicode
    en la cadena que representan.
    
    Args:
        m (List[int]): lisa de enteros que representan los códigos unicode de una cadena de caracteres.
    
    Returns:
        str: cadena que representan

    Raises:
        ValueError: Si alguno de los enteros no representa un caracter unicode válido.
    
    Example:
        decodificar_cadena([161, 72, 111, 108, 97, 32, 109, 117, 110, 100, 111, 33])="¡Hola mundo!"
    """
    try:
        lista_s = [chr(n) for n in m]
        return "".join(lista_s)
    except:
        raise ValueError("La lista contiene valores que no representan caracteres Unicode válidos.")
    


def cifrar_cadena_rsa(s:str,n:int,e:int,digitos_padding:int)->List[int]:
    """Cifra carácter a carácter una cadena de caracteres usando RSA con clave púbica (n,e)
    y digitos_padding cifras de padding al final del mensaje y devuelve la lista de enteros
    que representan el mensaje cifrado correspondiente.
    Args:
        s (str): texto claro
        n (int): módulo para RSA
        e (int): clave pública para RSA
        digitos_padding (int): número no negativo de dígitos de padding que deben usarse para el cifrado del mensaje.
    
    Returns:
        List[int]: lista de enteros que representa el mensaje cifrado con RSA para la clave dada.

    Raises: None
    """
    m_list = codificar_cadena(s)

    c_list = [cifrar_rsa(m,n,e,digitos_padding) for m in m_list]

    return c_list
    


def descifrar_cadena_rsa(cList:List[int],n:int,d:int,digitos_padding:int)->str:
    """Dado un mensaje cifrado con RSA usando la clave pública cuya clave privada asociada es (n,d)
    y digitos_padding cifras de padding al final del mensaje, devuelve la cadena orignal.
    Args:
        cList (List[int]): lisa de enteros que representan el mensaje cifrado
        n (int): módulo para RSA
        d (int): clave privada para RSA
        digitos_padding (int): número no negativo de dígitos de padding usados para el cifrado de cList.
    
    Returns:
        str: cadena que representa el texto claro correspondiente al mensaje cifrado cList.

    Raises:
        ValueError: Si, tras decodificar, alguno de los enteros del mensaje no representa un caracter unicode válido.    
    """
    try:
        mList = [descifrar_rsa(c, n, d, digitos_padding) for c in cList]

        return decodificar_cadena(mList)

    except:
        raise NameError(f"Error al descifrar la cadena RSA")


def romper_clave(n:int,e:int)->int:
    """A partir de una clave pública válida (n,e), recupera la clave privada d tal que
    de = 1 (mod phi(n)).
    
    Args:
        n (int): módulo para RSA
        e (int): clave pública para RSA
    
    Returns:
        int: clave privada d

    Raises:
        ValueError: Si no existe ninguna clave privada d compatible con la clave pública (n,e).
    """

    factores = factorizar(n)

    if len(factores) != 2:
        raise ValueError(f"Se esperaban exactamente dos factores primos, se obtuvieron: {factores}")

    items = list(factores.items())
    p, exp_p = items[0]
    q, exp_q = items[1]

    if exp_p != 1 or exp_q != 1:
        raise ValueError(f"Exponentes de los factores deben ser 1 para RSA estándar, se obtuvo {factores}")

    if p * q != n and q * p != n:
        raise ValueError(f"Los factores {p}, {q} no multiplican a n={n}")

    fi_n = (p - 1) * (q - 1)

    try:
        d = inversa_mod_p(e, fi_n)
    except ValueError:
        raise ValueError(f"No existe inverso modular de e={e} módulo φ(n)={fi_n}")
    
    return d



def ataque_texto_elegido(cList: List[int], n: int, e: int) -> str:
    """Ejecuta un ataque de texto claro elegido sobre un mensaje que ha sido cifrado
    con RSA plano sin usar padding a partir de su clave pública.
    
    Args:
        cList (List[int]): lista de enteros que representan el mensaje cifrado
        n (int): módulo para RSA
        e (int): clave pública para RSA
    
    Returns:
        str: texto plano descifrado para el mensaje cifrado cList
    
    Raises:
        ValueError: Si el mensaje no se corresponde con ningún texto plano que haya 
                    sido codificado con RSA sin padding.
    """
    # Crea el diccionario de valores ASCII y su contraparte cifrada
    valores = {}
    for i in range(1, 256):
        valores[i] = cifrar_rsa(i, n, e, 0)

    # Invierte las llaves y los valore
    valores_invertido = {}
    for clave, valor in valores.items():
        valores_invertido[valor] = clave
    
    # Intercambia los numeros cifrados por sus versiones descifradas
    try:
        lista_des = [valores_invertido[c] for c in cList]
    except:
        raise ValueError
    
    # Aplica chr a todos los elemntos de la lista
    lista_char = map(chr,lista_des)

    # Junta la lista en una string
    sep = ""
    texto = sep.join(lista_char)
    return texto



