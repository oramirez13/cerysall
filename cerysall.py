import os  # Interactúa con el sistema operativo (limpiar pantalla, ejecución de comandos).
import subprocess  # Permite ejecutar comandos y capturar su salida de texto para analizarla.
import requests  # Librería para realizar peticiones HTTP y auditoría web.
import whois  # Realiza consultas a bases de datos de registro de dominios.
import dns.resolver  # Resuelve registros DNS específicos como A, MX o TXT.
from colorama import Fore, init  # Proporciona colores ANSI para la interfaz de usuario.

# Inicializa colorama para que los colores se restablezcan tras cada línea.
init(autoreset=True)

# Listas internas para escaneos rápidos (Top 20 comunes).
TOP_SUBDOMAINS = [
    "www",
    "mail",
    "ftp",
    "admin",
    "blog",
    "dev",
    "staging",
    "api",
    "test",
    "vpn",
]
TOP_DIRECTORIES = [
    "admin",
    "login",
    "wp-admin",
    "api",
    "backup",
    "db",
    "config",
    "test",
    ".env",
]


def clear():
    """Limpia la terminal según el entorno (Windows o Linux)."""
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    """Muestra el logo del proyecto en la terminal."""
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


# ---------------------------------------------------------
# Función de Ping con Detección de OS
# ---------------------------------------------------------
def ping_con_deteccion():
    """Realiza un ping y analiza el TTL para adivinar el OS del objetivo."""
    target = input(Fore.YELLOW + "\n[+] Ingresa la IP o dominio objetivo: ")
    print(Fore.YELLOW + f"[i] Analizando host {target}...\n")

    # Configuramos el comando según el OS del host (Arch Linux usa -c).
    param = "-n" if os.name == "nt" else "-c"
    comando = ["ping", param, "4", target]

    try:
        # Ejecutamos el ping y capturamos la respuesta.
        resultado = subprocess.run(comando, capture_output=True, text=True)
        salida = resultado.stdout
        print(salida)

        # Análisis de TTL: Windows suele usar 128, Linux/Unix usa 64.
        if "ttl=" in salida.lower():
            if "ttl=128" in salida.lower():
                print(
                    Fore.CYAN
                    + "[*] Detección: El objetivo parece ser un sistema WINDOWS."
                )
            elif "ttl=64" in salida.lower():
                print(
                    Fore.CYAN
                    + "[*] Detección: El objetivo parece ser un sistema LINUX/UNIX."
                )
            else:
                print(Fore.CYAN + "[*] Detección: OS desconocido (TTL inusual).")
        else:
            print(
                Fore.RED
                + "[-] El host no respondió al ping (posible Firewall bloqueando ICMP)."
            )

    except Exception as e:
        print(Fore.RED + f"[-] Error en la ejecución: {e}")


def escanear_puertos():
    """Escaneo rápido con Nmap ignorando el bloqueo de ping (-Pn)."""
    target = input(Fore.YELLOW + "\n[+] Ingresa la IP o dominio: ")
    print(Fore.YELLOW + f"[i] Iniciando Nmap sobre {target}...\n")
    os.system(f"nmap -Pn -F {target}")


def escanear_subdominios():
    """Busca subdominios activos mediante peticiones HTTP."""
    dominio = input(Fore.YELLOW + "\n[+] Dominio (ej: ejemplo.com): ")
    for sub in TOP_SUBDOMAINS:
        url = f"http://{sub}.{dominio}"
        try:
            requests.get(url, timeout=2)
            print(Fore.GREEN + f"[+] Encontrado: {url}")
        except:
            pass


def whois_lookup():
    """Muestra datos WHOIS y registros IP A."""
    dominio = input(Fore.YELLOW + "\n[+] Dominio: ")
    try:
        w = whois.whois(dominio)
        print(Fore.GREEN + f"[+] Registrar: {w.registrar} | País: {w.country}")
        res = dns.resolver.resolve(dominio, "A")
        for ip in res:
            print(Fore.GREEN + f"[+] IPv4: {ip}")
    except:
        print(Fore.RED + "[-] Error en consulta WHOIS/DNS.")


def escanear_directorios():
    """Fuzzing de directorios web con manejo de códigos de estado."""
    url_base = input(Fore.YELLOW + "\n[+] URL (ej: http://192.168.1.1): ")
    if not url_base.startswith("http"):
        url_base = "http://" + url_base

    for ruta in TOP_DIRECTORIES:
        url = f"{url_base.rstrip('/')}/{ruta}"
        try:
            # allow_redirects=False evita falsos positivos por redirección.
            r = requests.get(url, timeout=2, allow_redirects=False)
            if r.status_code == 200:
                print(Fore.GREEN + f"[+] [200 OK] -> {url}")
            elif r.status_code in [301, 302]:
                print(Fore.BLUE + f"[*] [Redir {r.status_code}] -> {url}")
        except:
            pass


def menu():
    """Bucle principal de la herramienta."""
    while True:
        clear()
        banner()
        print(Fore.GREEN + "[1] Ping y Detección de OS")
        print(Fore.GREEN + "[2] Escaneo de puertos (Nmap)")
        print(Fore.GREEN + "[3] Escaneo de subdominios")
        print(Fore.GREEN + "[4] WHOIS & DNS Lookup")
        print(Fore.GREEN + "[5] Escaneo de directorios web")
        print(Fore.RED + "[6] Salir\n")

        op = input(Fore.YELLOW + "Selecciona una opción: ")
        if op == "1":
            ping_con_deteccion()
        elif op == "2":
            escanear_puertos()
        elif op == "3":
            escanear_subdominios()
        elif op == "4":
            whois_lookup()
        elif op == "5":
            escanear_directorios()
        elif op == "6":
            break
        else:
            print(Fore.RED + "[!] Opción inválida.")
        input(Fore.YELLOW + "\nENTER para continuar...")


if __name__ == "__main__":
    menu()
