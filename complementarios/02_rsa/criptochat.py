import sys
import os
from rsa import *

def public_user_keys(user_name)->Tuple[int,int,int]:
    ruta_pub = os.path.join("Usuarios", f"pub_{user_name}.txt")
    try:
        with open(ruta_pub, "r", encoding="utf-8") as f:
            n = f.readline()
            e = f.readline()
            pad = f.readline()
    except:
        raise FileNotFoundError("Nombre de usuario no válido")
    return int(n), int(e), int(pad)

def priv_user_key(user_name):
    ruta_priv = os.path.join("Usuarios", f"priv_{user_name}.txt")
    try:
        with open(ruta_priv, "r", encoding="utf-8") as f:
            d = f.readline()
    except:
        raise FileNotFoundError("Nombre de usuario no válido")
    return int(d)

def request():
    query = input("¿Qué desea? [C - cifrar | D - descifrar | S - salir]: ").lower()
    while query not in ("c", "s", "d"):
        query = input("Input no válido. Introduzca una entrada válida [C - cifrar | D - descifrar | S - salir]: ")
    return query

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        raise SystemError("Debes introducir los nombres de los dos usuarios como argumento en la terminal")
    user1 = args[1]
    user2 = args[2]

    user1_pub = public_user_keys(user1)
    user1_priv = priv_user_key(user1)

    user2_pub = public_user_keys(user2)

    query = request()
    while True:
        if query == "s":
            print("Gracias por confiar en CriptoImat")
            os._exit(0)

        if query == "c":
            message = input("Introduzca el mensaje a cifrar en texto plano: ")
            cypher = cifrar_cadena_rsa(message, user2_pub[0], user2_pub[1], user2_pub[2])
            print(" ".join(str(i) for i in cypher))

        if query == "d":
            cypher = input("Introduzca el mensaje a descifrar: ").strip()
            c_list = [int(x) for x in cypher.split()]
            message = descifrar_cadena_rsa(c_list, user1_pub[0], user1_priv, user1_pub[2])
            print(repr(message))


        query = request()
    