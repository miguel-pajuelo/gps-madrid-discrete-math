from rsa import generar_claves
import os

MAX_CODE = 7 #digitos maximos usados por unicode

if __name__ == "__main__":

    nombre = input("Introduce tu nombre: ").strip()
    while not nombre:
        print("Nombre vacío. Introduce un nombre válido.")
        nombre = input("Introduce tu nombre: ").strip()

    min_val = input("Introduce el valor min [int]: ").strip()
    while not min_val.isdigit():
        print("Valor no válido del valor min")
        min_val = input("Introduce un valor válido [int]: ").strip()
    min_val = int(min_val)

    max_val = input("Introduce el valor max [int]: ").strip()
    while not max_val.isdigit():
        print("Valor no válido del valor max")
        max_val = input("Introduce un valor válido [int]: ").strip()
    max_val = int(max_val)

    if min_val > max_val:
        print("min_val no puede ser mayor que max_val")
        raise SystemExit(1)
    
    try:
        n, e, d = generar_claves(min_val, max_val)
        maximum_padding = len(str(n)) + MAX_CODE
    except Exception as err:
        print(f"Error generando claves RSA: {err}")

    

    num_pad = input(F"Introduce la cantidad de dígitos de padding [MAX PADDING PARA N SELECCIONADA = {maximum_padding}] [int]: ").strip()
    while not num_pad.isdigit():    
        print("Valor no válido de dígitos de padding")
        num_pad = input("Introduce un valor válido [int]: ").strip()
    num_pad = int(num_pad)

    if num_pad > maximum_padding:
        print(f"Valor no válido de dígitos de padding, debe ser menor o igual a {maximum_padding}")
        num_pad = input("Introduce un valor válido [int]: ").strip()
    num_pad = int(num_pad)

    carpeta = "Usuarios"
    os.makedirs(carpeta, exist_ok=True)

    ruta_pub = os.path.join(carpeta, f"pub_{nombre}.txt")
    ruta_priv = os.path.join(carpeta, f"priv_{nombre}.txt")


    with open(ruta_pub, "w", encoding="utf-8") as f:
        f.write(f"{n}\n")
        f.write(f"{e}\n")
        f.write(f"{num_pad}\n")


    with open(ruta_priv, "w", encoding="utf-8") as f:
        f.write(f"{d}")


    print(f"Guardados:\n - {ruta_pub}\n - {ruta_priv}")

