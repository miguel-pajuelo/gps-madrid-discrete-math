"""
imatlab.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP03B
Integrantes:
    - Jorge Ois de Pascual
    - Miguel Pajuelo Gomez

Descripción:
Sistema interactivo IMAT-LAB de resolución de ecuaciones en aritmética modular.

Interfaz de acceso interactivo o por lotes a la librería modular.py. Si este script se ejecuta sin par´ametros,
lanzar´a la interfaz de usuario para el modo interactivo.
"""


from typing import TextIO
import modular
import re
import sys
from modular import *

def titulo():
    print(""" 
  _____ __  __       _   _           _     
 |_   _|  \/  |     | | | |         | |    
   | | | \  / | __ _| |_| |     __ _| |__  
   | | | |\/| |/ _` | __| |    / _` | '_ \ 
  _| |_| |  | | (_| | |_| |___| (_| | |_) |
 |_____|_|  |_|\__,_|\__|______\__,_|_.__/     
por Miguel Pajuelo y Jorge Ois         
          """)


def run_commands(fin:TextIO,fout:TextIO):
    """ Ejecuta línea a línea los comandos leídos de fin y escribe resultados en fout. """

    patron_primo = re.compile(r'primo\((-?\d+)\)')
    patron_primos = re.compile(r'primos\((-?\d+),\s*(-?\d+)\)')
    patron_coprimo = re.compile(r'coprimos\((-?\d+),\s*(-?\d+)\)')
    patron_mcd = re.compile(r'mcd\((.*?)\)')
    patron_factorizar = re.compile(r'factorizar\((-?\d+)\)')
    patron_pow = re.compile(r'pow\((-?\d+),\s*(-?\d+),\s*(-?\d+)\)')
    patron_inv = re.compile(r'inv\((-?\d+),\s*(-?\d+)\)')
    patron_euler = re.compile(r'euler\((-?\d+)\)')
    patron_legendre  = re.compile(r'legendre\((-?\d+),\s*(-?\d+)\)')
    patron_Legendre  = re.compile(r'Legendre\((-?\d+),\s*(-?\d+)\)')
    patron_sistemas = re.compile(r'resolverSistema\((.*)\)')
    patron_raiz = re.compile(r'raiz\((-?\d+),\s*(-?\d+)\)')
    patron_ecCuadratica = re.compile(r'ecCuadratica\((-?\d+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\)')
    patron_bezout = re.compile(r'bezout\((-?\d+),\s*(-?\d+)\)')



    for linea in fin:
        if linea.strip() == "":
            break
        if linea == "--h":
            print('''
                Lista de comandos disponibles:\n
                    - primo(int): retorna si un número es o no primo\n
                    - primos(int, int): Retorna la lista de primos contenidos entre el primer y segundo entero\n
                    - coprimos(int, int): Retorna si dos números son o no coprimos\n
                    - mcd(int, int): Retorna el máximo común divisor de dos enteros\n
                    - mcd_n(lista): Retorna el máximo común divisor de una lista de enteros\n
                    - factorizar(int): Retorna la factorización prima de un número entero\n
                    - pow(int, int, int): Retorna la potencia modular (mod p)\n
                    - inv(int, int): Retorna la inversa de un número módulo p\n
                    - euler(int): Retorna el valor de la función φ(n) de Euler\n
                    - legendre(int, int): Retorna el símbolo de Legendre (a/p)\n
                    - resolverSistema([a; b; p], ...): Resuelve un sistema de congruencias lineales\n
                    - raiz(int, int): Calcula raíces cuadradas módulo p\n
                    - ecCuadratica(int, int, int, int): Resuelve ecuaciones cuadráticas módulo p\n
                    - bezout(int, int): Retorna (d, x, y) tal que d = mcd(a, b) = ax + by\n
                    - python imatlab.py [fichero_entrada fichero_salida]
            ''')
            break

        
        linea = linea.rstrip()
        primo = patron_primo.findall(linea)
        primos = patron_primos.findall(linea)
        coprimo = patron_coprimo.findall(linea)
        mcd_match = patron_mcd.findall(linea)
        factorizar_match = patron_factorizar.findall(linea)
        pow_match = patron_pow.findall(linea)
        inv = patron_inv.findall(linea)
        euler_match = patron_euler.findall(linea)
        legendre_match = patron_legendre.findall(linea)
        Legendre_match = patron_Legendre.findall(linea)
        sistemas_match = patron_sistemas.findall(linea)
        raiz_match = patron_raiz.findall(linea)
        ec_match = patron_ecCuadratica.findall(linea)
        bezout_match = patron_bezout.findall(linea)

        if Legendre_match:
            fout.write("NOP")

        if primo:
            for p in primo:
                numero = int(p)
                if es_primo(numero):
                    fout.write("Sí")
                else:
                    fout.write("No")

        elif coprimo:
            for a, b in coprimo:
                num1, num2 = int(a), int(b)
                if coprimos(num1,num2):
                    fout.write("Sí")
                else:
                    fout.write("No")
                
        elif primos:
            for a, b in primos:
                num1, num2 = int(a), int(b)
                lista = lista_primos(num1, num2)
                if lista:
                    fout.write(", ".join(str(x) for x in lista))
                else:
                    fout.write("NE")

        elif mcd_match:
            for bloque in mcd_match:
                nums_str = re.findall(r"-?\d+", bloque)
                if not nums_str:
                    fout.write("NE")
                    continue

                valores = [int(x) for x in nums_str]

                if len(valores) == 1:
                    fout.write(str(abs(valores[0])))

                elif len(valores) == 2:
                    a, b = abs(valores[0]), abs(valores[1])
                    fout.write(str(mcd(a, b)))

                else:
                    fout.write(str(mcd_n([abs(x) for x in valores])))
                    

        elif factorizar_match:
            for f in factorizar_match:
                f = int(f)
                if f in (-1, 0, 1):
                    fout.write(str(f))
                else:
                    fact = factorizar(f)
                    fout.write(", ".join([f"{p}: {e}" for p,e in fact.items()]))

        elif pow_match:
            for a,b,c in pow_match:
                try:
                    fout.write(str(potencia_mod_p(int(a),int(b),int(c))))
                except:
                    fout.write("NE")


        elif inv:
            for a,b in inv:
                try:
                    fout.write(str(inversa_mod_p(int(a), int(b))))
                except:
                    fout.write("NE")

        elif euler_match:
            for a in euler_match:
                num = int(a)
                fout.write(str(euler(num)))

        elif legendre_match:
            for a,b in legendre_match:
                if b == "0":
                    fout.write('NE')
                else:
                    fout.write(str(legendre(int(a), int(b))))

        elif sistemas_match:
            inside = sistemas_match[0]
            try:
                patron = re.compile(r'\[(-?\d+);(-?\d+);(-?\d+)\]')
                triples = re.findall(patron, inside)
                if not triples:
                    fout.write("NE")
                else:
                    alist, blist, plist = [], [], []
                    for a_str, b_str, p_str in triples:
                        alist.append(int(a_str))
                        blist.append(int(b_str))
                        plist.append(int(p_str))
                    r, m = resolver_sistema_congruencias(alist, blist, plist)
                    fout.write(f"{r} (mod {m})")
            except:
                fout.write("NE\n")



        elif raiz_match:
            for a,b in raiz_match:
                try:
                    r = raiz_mod_p(int(a),int(b))
                    if isinstance(r, tuple):
                        fout.write(", ".join(map(str,r)))
                    else:
                        fout.write(str(r))
                except:
                    fout.write("NE")

        elif bezout_match:
            pass

        elif ec_match:
            for a,b,c,p in ec_match:
                try:
                    x1,x2 = ecuacion_cuadratica(int(a),int(b),int(c),int(p))
                    fout.write(f"{x1}, {x2}")
                except:
                    fout.write("NE")

        else:
            print("Comando no reconocido o campo de entrada no válido. Introduzca --h para acceder al menú de comandos")

        fout.write("\n")


if __name__ == "__main__":
    titulo()
    #MODO INTERACTIVO
    if len(sys.argv) == 1:
        while True:
            try:
                linea = input("Comando: ")
            except EOFError:
                break
            if linea.strip() == "":
                break
            run_commands([linea], sys.stdout)

    #MODO BATCH
    elif len(sys.argv) == 3:
        with open(sys.argv[1], "r") as fin, open(sys.argv[2], "w") as fout:
            run_commands(fin, fout)
    else:
        print(f"Uso: python imatlab.py [fichero_entrada fichero_salida]")

