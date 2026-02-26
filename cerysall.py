import os
import subprocess
import requests
import whois
import dns.resolver
from colorama import Fore, init

init(autoreset=True)


# ------------------------
# Funciones básicas
# ------------------------


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    print(
        Fore.CYAN
        + r"""
     _____ ______ _______     _______          _ _    _ _
    / ____|  ____|  __ \ \   / / ____|   /\   | | |  | | |
   | |    | |__  | |__) \ \_/ / (___    /  \  | | |  | | |
   | |    |  __| |  _  / \   / \___ \  / /\ \ | | |  | | |
   | |____| |____| | \ \  | |  ____) |/ ____ \| |____| |____
    \_____|______|_|  \_\ |_| |_____//_/    \_\______|______|
    """
    )
    print(Fore.MAGENTA + "                    by orami – InfoSec ⚔\n")


# ------------------------
# Ping
# ------------------------


def ping():
    target = input(Fore.YELLOW + "\n[+] Ingresa la IP o dominio objetivo: ")
    print(Fore.YELLOW + f"[i] Haciendo ping a {target}...\n")
    os.system(f"ping -c 4 {target}")


# ------------------------
# Escaneo de puertos
# ------------------------


def escanear_puertos():
    target = input(
        Fore.YELLOW + "\n[+] Ingresa la IP o dominio objetivo para escanear con Nmap: "
    )
    print(Fore.YELLOW + f"[i] Escaneando puertos en {target} con Nmap...\n")
    os.system(f"nmap -Pn -sS -T4 {target}")


# ------------------------
# Escaneo de subdominios
# ------------------------


def escanear_subdominios():
    dominio = input(
        Fore.YELLOW + "\n[+] Ingresa el dominio objetivo (ej: ejemplo.com): "
    )
    diccionario = input(
        Fore.YELLOW + "[+] Ruta al diccionario de subdominios (ej: subdomains.txt): "
    )
    print(Fore.YELLOW + "[i] Escaneando subdominios...\n")

    try:
        with open(diccionario, "r", encoding="latin-1") as f:
            subdominios = f.read().splitlines()

        for sub in subdominios:
            url = f"http://{sub}.{dominio}"
            try:
                requests.get(url)
                print(Fore.GREEN + f"[+] Subdominio encontrado: {url}")
            except requests.ConnectionError:
                pass

    except FileNotFoundError:
        print(Fore.RED + "[-] No se encontró el diccionario.")


# ------------------------
# WHOIS + DNS
# ------------------------


def whois_lookup():
    dominio = input(Fore.YELLOW + "\n[+] Ingresa el dominio objetivo: ")
    print(Fore.YELLOW + f"[i] Realizando WHOIS lookup para {dominio}...\n")

    try:
        w = whois.whois(dominio)
        print(Fore.GREEN + str(w))
    except Exception:
        print(Fore.RED + "[-] Error en la búsqueda WHOIS.")

    print(Fore.YELLOW + f"\n[i] Realizando DNS lookup para {dominio}...\n")

    try:
        resultado = dns.resolver.resolve(dominio, "A")
        for ipval in resultado:
            print(Fore.GREEN + f"[+] Dirección IP: {ipval.to_text()}")
    except Exception:
        print(Fore.RED + "[-] Error en la búsqueda DNS.")


# ------------------------
# Escaneo de directorios
# ------------------------


def escanear_directorios():
    objetivo = input(
        Fore.YELLOW + "\n[+] Ingresa la URL objetivo (ej: http://ejemplo.com): "
    )
    diccionario = input(
        Fore.YELLOW + "[+] Ruta al diccionario de directorios (ej: wordlist.txt): "
    )
    print(Fore.YELLOW + "[i] Escaneando directorios...\n")

    try:
        with open(diccionario, "r", encoding="latin-1") as f:
            rutas = f.read().splitlines()

        for ruta in rutas:
            url = f"{objetivo.rstrip('/')}/{ruta}"
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    print(Fore.GREEN + f"[+] Encontrado: {url}")
            except requests.ConnectionError:
                pass

    except FileNotFoundError:
        print(Fore.RED + "[-] No se encontró el diccionario.")


# ------------------------
# Menú principal
# ------------------------


def menu():
    while True:
        clear()
        banner()

        print(Fore.GREEN + "[1] Ping de conectividad")
        print(Fore.GREEN + "[2] Escaneo de puertos con Nmap")
        print(Fore.GREEN + "[3] Escaneo de subdominios")
        print(Fore.GREEN + "[4] WHOIS & DNS Lookup")
        print(Fore.GREEN + "[5] Escaneo de directorios web")
        print(Fore.RED + "[6] Salir\n")

        opcion = input(Fore.YELLOW + "Selecciona una opción: ")

        if opcion == "1":
            ping()
        elif opcion == "2":
            escanear_puertos()
        elif opcion == "3":
            escanear_subdominios()
        elif opcion == "4":
            whois_lookup()
        elif opcion == "5":
            escanear_directorios()
        elif opcion == "6":
            print(Fore.RED + "\nSaliendo...")
            break
        else:
            print(Fore.RED + "\n[!] Opción no válida.")

        input(Fore.YELLOW + "\nPresiona ENTER para continuar...")


if __name__ == "__main__":
    menu()
