"""
modular.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP03B
Integrantes:
    - Miguel Pajuelo Gomez
    - Jorge Ois de Pascual

Descripción:
Librería para la realización de cálculos y resolución de problemas de aritmética modular.
"""

from typing import Tuple, List, Dict
import math
import random
from functools import reduce

class IncompatibleEquationError(Exception):
    pass



def es_primo(n:int)->bool:
    """ Reciba un entero n y devuelva verdadero si es un número primo y falso en caso contrario

    Args:
        n (int): Entero
    
    Returns:
        true si el entero es un número primo.
        false en caso contrario.

    Raises: None
    
    Examples:
        es_primo(5)=True
        es_primo(4)=False
    """
    #Quitamos casos base
    if n == 1 or n == 0:
        return False
    if n < 2:
        return False
    if n in (2,3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41):
        return True
    if n % 2== 0:
        return False

    #para convertir el Algoritmo Miller-Rabin en determinista hay que probarlo contra bases conocidas


    lista_k = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
    numero_SW = 3317044064679887385961981 
    #numero que hasta el cual Sorenson y Webster descubrieron para el que se puede probar con los primeros 12 primos, es decir numero para el cual es determinista
    edge = False
    if n < numero_SW: edge = True 
    
    # esta parte crea un nuvo numero s = n-1 y lo reduce hasta quitar todos los multiplos de 2
    # tal que te quede un nuvo numero que sea 2^r * d r siendo los factores de dos quitados y
    # d siendo el numero impar final
    r = 0
    s = n-1
    while s % 2 == 0:
        r +=1
        s = s // 2

    for k in lista_k:
        x = potencia_mod_p(k,s,n)
        if x == 1 or x == n-1:
            continue # se salta esta interacion de k
        for _ in range(r-1):
            x = potencia_mod_p(x,2,n)
            if x == n-1:
                break

        else: return False

    return True
    

def lista_primos(a,b)-> list[int]:
    ''' Recibe dos enteros a y b y devuelva la lista de números primos en el intervalo [a, b)

    Args:
        a (int): Elemento inicial del intervalo (incluido)
        b (int): Elemento final del intervalo (no incluido)
    
    Returns:
        List[int]: lista ordenada de primos mayores o iguales que a y menores que b.

    Raises: None
    
    Examples:
        lista_primos(1,11)=[2,3,5,7]
    '''

    if a >= b:
        return []

    if b < 2:
        return []
    
    es_primo = [True] * (b+1)
    es_primo[0] = es_primo[1] = False

    for p in range(2, int(math.sqrt(b) + 1)):
        if es_primo[p]:
            for j in range(p*p, b+1, p):
                es_primo[j] = False
    
    return [i for i in range(max(2, a), b) if es_primo[i]]


def factorizar(n:int)->dict[int,int]:
    ''' Recibe  un entero n y devuelve un diccionario cuyas claves son los primos que dividen a n y sus valores los
    correspondientes exponentes en la descomposición en producto de factores primos de n.
    Args:
        n (int): Entero que se desea factorizar.
    
    Returns:
        Dict[int,int]: Diccionario en el que las claves son primos positivos p_i que dividen a n y, para cada p_i,
            su valor asociado es el máximo exponente e_i tal que p_i^(e_i) divide a n. Si n=0, devuelve un diccionario vacío.

    Raises: None

    Examples:
        factorizar(12)={2: 2, 3: 1}
        factorizar(0)={}
    '''
    factores = {}

    if n == 0:
        return {}
    
    if n < 0:
        n = abs(n)
    
    while n % 2 == 0:
        factores[2] = factores.get(2, 0) + 1
        n //= 2

    while n % 3 == 0:
        factores[3] = factores.get(3, 0) + 1
        n //= 3

    p = 5
    step = 2
    while p * p <= n and n > 1:
        while n % p == 0:
            factores[p] = factores.get(p, 0) + 1
            n //= p
        p += step
        step = 6 - step

    if n > 1:
        factores[n] = factores.get(n, 0) + 1

    return factores


def mcd(a:int,b:int = 0)->int:
    ''' Calcula el máximo común divisor de dos enteros a y b.
    Args:
        a (int): Primer entero.
        b (int): Segundo entero.
    
    Returns:
        int: devuelve el máximo común divisor de a y b

    Raises: None

    Examples:
        mcd(10,15)=5
    '''
    a, b = abs(a), abs(b)
    if a == 0:
        return b
    if b == 0:
        return a
    if a == b:
        return abs(a)
    if max(a,b) % min(a,b) == 0:
        return min(a,b)
    while b != 0:
        a, b = b, a % b
    return a


def bezout(n:int, m:int) -> Tuple[int,int,int]:
    '''Calcula el máximo común divisor d de dos enteros a y b junto con dos enteros x e y tales que
            d=ax+by

    Args:
        a (int): Primer entero.
        b (int): Segundo entero.
    
    Returns: (d,x,y)
        d (int): Máximo común divisor.
        x (int): Coeficiente de a.
        y (int): Coeficiente de b.

    Raises: None

    Examples:
        bezout(6,10)=(2,2,-1)
    '''
    if m == 0:
        if n >= 0:
            return (n, 1, 0)
        else:
            return (-n, -1, 0)
        
    d, x1, y1 = bezout(m, n % m)

    x = y1
    y = x1 - (n // m) * y1
    
    return (d, x, y)


def mcd_n(nlist:List[int])->int:
    '''Dados una lista de enteros, devuelve el máximo divisor común a todos ellos.
    Args:
        nList (List[int]): Lista de enteros.        
    
    Returns:
        int: devuelve el máximo entero que divide a todos los enteros de la lista.

    Raises: None

    Examples:
        mcd([4,10,14])=2
    '''

    return reduce(mcd,nlist)


def bezout_n(nlist:List[int])->Tuple[int,List[int]]:
    #Opcional
    '''Dada una lista de enteros [a_1,...,a_n], devuelve el máximo divisor común d a todos ellos y una
    lista de coeficientes [x_1,...,x_n] tal que
        d=a_1*x_1+...a_n*x_n

    Args:
        nList (List[int]): Lista de enteros.        
    
    Returns: (d,X)
        d (int): Máximo entero que divide a todos los enteros de la lista.
        X (List[int]): Lista de coeficientes [x_1,...,x_n].

    Raises: None

    Examples
        bezout_n([4,10,14])=(2,[-2,1,0])
    '''
    pass


def coprimos(n:int,m:int)->bool:
    '''Determina si dos enteros son coprimos.
    Args:
        a (int): Primer entero.
        b (int): Segundo entero.
    
    Returns:
        bool: Verdadero si son coprimos y falso si no.

    Raises: None

    Examples:
        coprimos(14,20)=False
        coprimos(14,15)=True
    '''
    return mcd(n,m) == 1


def potencia_mod_p(base:int, exp:int, p:int) -> int:
    '''Calcula potencias módulo p.

    Args:
        base (int): Base de la potencia.
        exp (int): Exponente al que se eleva la base.
        p (int): Módulo.
    
    Returns:
        int: Resto de dividir base^exp módulo p.

    Raises:
        ZeroDivisionError: Si el módulo es 0 o si la base y el exponente
        son ambos 0 al mismo tiempo.

    Examples:
        potencia_mod_p(2,3,7)=1
    '''
    # se va a calcular usando exponienciacion binaria
    # esto se hace transformando el exponente en suma de sus componentes binarios
    # y quedandote solo con los 1, esto se hace con exp%2 y exp//2, en el caso de
    # que sea 1 el resultadp se multiplica por la base y luego se hace modulo p
    # A la base tambien se le cuadras y aplica modulo m, se 1 o no el bit del 
    # exponente
    if p == 0:
        raise ZeroDivisionError("módulo 0 no permitido")
    if base == 0 and exp == 0:
        raise ZeroDivisionError("0^0 indefinido")

    base = base % p
    if exp < 0:
        inv = inversa_mod_p(base, p)  # lanza si no existe
        base = inv
        exp = -exp

    resultado = 1
    while exp > 0:
        if exp % 2 == 1:
            resultado = (resultado * base) % p
        base = (base * base) % p
        exp //= 2
    return resultado
    

def inversa_mod_p(n:int,p:int)->int:
    '''Calcula la inversa de un número n módulo p.

    Args:
        n (int): Número que se desea invertir
        p (int): Módulo.
    
    Returns:
        int: Entero x entre 0 y p-1 tal que n*x es congruente con 1 módulo p.

    Raises:
        ZeroDivisionError: Si el módulo es 0 o si n no es invertible módulo p.
    
    Examples:
        inversa_mod_p(2,7)=4
    '''
    if p == 0:
        raise ZeroDivisionError("módulo 0 no permitido")
    n %= p
    if n == 0:
        raise ZeroDivisionError("inversa no existe")

    # Ruta más rápida (CPython en C). Lanza ValueError si gcd(n,p) != 1.
    try:
        return pow(n, -1, p)
    except ValueError:
        pass  # cae al extendido

    # Euclides extendido iterativo, sin recursión ni estructuras extra
    a, b = n, p
    x0, x1 = 1, 0
    while b:
        q = a // b
        a, b = b, a - q * b
        x0, x1 = x1, x0 - q * x1
    if a != 1:
        raise ZeroDivisionError("inversa no existe")
    return x0 % p


def euler(n:int)->int:
    '''Calcula la función phi de Euler de un entero positivo n, es decir, cuenta cúantos enteros positivos
    menores que n son coprimos con n.

    Args:
        n (int): Número entero positivo.
    
    Returns:
        int: Función phi de Euler de n.

    Raises: None

    Examples:
        euler(7)=6
        euler(15)=8
    '''

    if n == 1:
        return 1
    respuesta = 1
    factores_dict = factorizar(n)

    for factor in factores_dict:
        expo = factores_dict[factor]
        if expo == 1:
            respuesta *= factor - 1
        else:
            respuesta *= (factor -1) * factor**(expo - 1)

    return respuesta
    

def legendre(n:int,p:int)->int:
    """ Dado un entero n y un número primo p, calcula el símbolo de Legendre de n módulo p.

    Args:
        n (int): Número entero.
        p (int): Número primo.
    
    Returns:
        int: Símbolo de Legendre de Euler de n módulo p:
            0 si es múltiplo de p
            1 si es un cuadrado perfecto (distinto de 0), módulo p
            -1 en caso contrario.

    Raises:
        ZeroDivisionError: Si el módulo p es 0.

    Examples:
        legendre(2,5)=-1
        legendre(2,7)=1
        legendre(10,5)=0
    """
    if p == 0:
        raise ZeroDivisionError("p no puede ser 0")
    n = n % p
    if n == 0:
        return 0
    r = potencia_mod_p(n, (p - 1) // 2, p)
    if r == 1:
        return 1
    if r == p - 1:
        return -1
    return 0



def resolver_sistema_congruencias(alist:List[int],blist:List[int],plist:List[int])->Tuple[int,int]:
    """ Dadas tres listas de números enteros [a_1,...,a_n], [b_1,...,b_n] y [p_1,...,p_n], resuelve el sistema de congruencias
    
    a_i * x = b_i (mod p_i)   i=1,...,n
    
    devolviendo un entero r y un módulo m tales que las soluciones del sistema corresponden a todos los enteros
    x congruentes con r módulo m.

    Args:
        alist (List[int]): Lista de coeficientes de la variable x, [a_1,...,a_n].
        blist (List[int]): Lista de términos independientes [b_1,...,b_n].
        plist (List[int]): Lista de módulos [p_1,...,p_n]
    
    Returns: (r,m)
        r (int): Entero entre 0 y m-1.
        m (int): Entero positivo, módulo de la solución.

    Raises:
        IncompatibleEquationError: Si no es posible resolver el sistema.

    Examples:
        resolverSistema([2;3;5])=(4,5)
        resolverSistema([2;4;6])=(2,3)
        resolverSistema([1;1;3],[4;7;11])=(10,33)        
    """
    if not (len(alist) == len(blist) == len(plist)):
        raise IncompatibleEquationError("Listas de distinto tamaño")
    
    congruencias = []
    for a, b, p in zip(alist, blist, plist):
        g = mcd(a, p)
        if b % g != 0:
            raise IncompatibleEquationError("Sistema incompatible")
        a, b, p = a // g, b // g, p // g
        r = (inversa_mod_p(a, p) * b) % p
        congruencias.append((r, p))

    r, m = congruencias[0]
    for ri, mi in congruencias[1:]:
        d, s, t = bezout(m, mi)
        if (ri - r) % d != 0:
            raise IncompatibleEquationError("Sistema incompatible")
        r = (r + s * ((ri - r) // d) * m) % (m * mi // d)
        m = m * mi // d

    return r % m, m





def raiz_mod_p(n:int,p:int)->int:
    """ Encuentra, si existe, una raíz cuadrada para un entero n módulo un número primo p.

    Args:
        n (int): Entero del que se desea hallar la raíz.
        p (int): Módulo. Se asume que es un número primo.
    
    Returns:
        int: Entero x entre 0 y p-1 tal que x^2 = n (mod p).

    Raises:
        IncompatibleEquationError: Si no es posible hallar dicha raíz.

    Examples:
        raiz_mod_p(2,7)=3
    """
    #Opcional 
    pass





def ecuacion_cuadratica(a:int,b:int,c:int,p:int)->Tuple[int,int]:
    """ Halla, si es posible, las dos posibles soluciones de la ecuación cuadrática ax^2+bx+c=0 (mod p).
    Devuelve una tupla con las dos raíces (distintas o una misma raíz repetida en caso de ser doble).

    Args:
        a (int): Coeficiente de x^2.
        b (int): Coeficiente de x.
        c (int): Término independiente.
        p (int): Módulo. Se asume que es un número primo.
    
    Returns: (x1,x2)
        x1 (int): Primera solución. Entero entre 0 y p-1.
        x2 (int): Segunda solución. Entero entre 0 y p-1.

    Raises:
        IncompatibleEquationError: Si no es posible resolver la ecuación.

    Examples:
        ecuacion_cuadratica(4,1,3,11)
        ecuacion_cuadratica(4,1,5,11)=(3, 5)
        ecuacion_cuadratica(1,2,1,11)=(10,10)
    """
    #Opcional
    pass



