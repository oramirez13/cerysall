import os  # Librería para interactuar con el Sistema Operativo (limpiar pantalla, ejecutar comandos).
import subprocess  # Permite ejecutar procesos externos y capturar su salida.
import requests  # Fundamental para realizar peticiones HTTP/HTTPS a servidores web.
import whois  # Librería para consultar información de registro de dominios.
import dns.resolver  # Parte de dnspython, utilizada para resolver registros DNS (A, MX, TXT, etc.).
from colorama import (
    Fore,
    init,
)  # Permite dar formato y colores a la salida de la terminal.

# Inicializa colorama para que los códigos de color se limpien automáticamente tras cada print.
init(autoreset=True)

# --- Configuración de Diccionarios "Top 20" (Optimización) ---
# Definimos listas estáticas para que el script sea portátil y no dependa de archivos externos .txt.
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
    "portal",
    "vpn",
    "support",
    "webmail",
    "remote",
    "secure",
    "apps",
    "cloud",
    "m",
    "shop",
    "git",
]

TOP_DIRECTORIES = [
    "admin",
    "login",
    "wp-admin",
    "api",
    "v1",
    "v2",
    "backup",
    "db",
    "config",
    "includes",
    "js",
    "css",
    "img",
    "uploads",
    "shell",
    "temp",
    "test",
    "old",
    "dev",
    ".env",
]


def clear():
    """Limpia la consola detectando si el sistema es Windows (nt) o Unix/Linux."""
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    """Imprime el arte ASCII del programa con colores cian y magenta."""
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


# --- Funciones de Reconocimiento ---


def ping():
    """Verifica si un host está vivo enviando paquetes ICMP."""
    target = input(Fore.YELLOW + "\n[+] Ingresa la IP o dominio objetivo: ")
    print(Fore.YELLOW + f"[i] Enviando paquetes ICMP a {target}...\n")
    # Windows usa '-n' para el conteo de paquetes, Linux/Unix usa '-c'.
    param = "-n" if os.name == "nt" else "-c"
    # Ejecuta el comando ping del sistema operativo.
    os.system(f"ping {param} 4 {target}")


def escanear_puertos():
    """Llama a Nmap para identificar puertos abiertos."""
    target = input(Fore.YELLOW + "\n[+] Ingresa la IP o dominio para Nmap: ")
    print(
        Fore.YELLOW
        + f"[i] Ejecutando escaneo rápido (Top 100 puertos) en {target}...\n"
    )
    # -Pn: No intenta ping previo (útil si el host bloquea ICMP).
    # -F: Modo rápido, escanea los 100 puertos más comunes en lugar de 1000.
    os.system(f"nmap -Pn -F {target}")


def escanear_subdominios():
    """Intenta resolver subdominios comunes para ampliar la superficie de ataque."""
    dominio = input(Fore.YELLOW + "\n[+] Ingresa el dominio (ej: ejemplo.com): ")
    print(
        Fore.YELLOW
        + f"[i] Buscando los {len(TOP_SUBDOMAINS)} subdominios más comunes...\n"
    )

    for sub in TOP_SUBDOMAINS:
        url = f"http://{sub}.{dominio}"
        try:
            # Realiza una petición GET; si el subdominio no existe, lanzará una excepción de conexión.
            requests.get(url, timeout=2)
            print(Fore.GREEN + f"[+] Activo: {url}")
        except requests.ConnectionError:
            # Si el subdominio no resuelve o no hay servidor web, simplemente continúa.
            pass
        except requests.Timeout:
            # Si el servidor tarda demasiado en responder, lo ignoramos.
            pass


def whois_lookup():
    """Obtiene datos del registrador y registros de dirección IP (DNS)."""
    dominio = input(Fore.YELLOW + "\n[+] Ingresa el dominio objetivo: ")
    print(Fore.YELLOW + "\n[i] Consultando WHOIS...")
    try:
        # Consulta la base de datos pública de registros de dominios.
        w = whois.whois(dominio)
        print(Fore.GREEN + f"Registrador: {w.registrar}")
        print(Fore.GREEN + f"País: {w.country}")
    except:
        print(Fore.RED + "[-] No se pudo obtener información WHOIS.")

    print(Fore.YELLOW + "\n[i] Consultando registros DNS (Tipo A)...")
    try:
        # Busca específicamente el registro 'A' (mapeo de nombre a dirección IPv4).
        respuestas = dns.resolver.resolve(dominio, "A")
        for rdata in respuestas:
            print(Fore.GREEN + f"[+] IP encontrada: {rdata}")
    except:
        print(Fore.RED + "[-] Error en la resolución DNS.")


def escanear_directorios():
    """Busca archivos o carpetas ocultas en el servidor web (Fuzzing)."""
    objetivo = input(Fore.YELLOW + "\n[+] Ingresa la URL (ej: http://ejemplo.com): ")
    # Asegura que la URL tenga el protocolo para que 'requests' funcione correctamente.
    if not objetivo.startswith("http"):
        objetivo = "http://" + objetivo

    print(Fore.YELLOW + f"[i] Escaneando {len(TOP_DIRECTORIES)} rutas críticas...\n")

    for ruta in TOP_DIRECTORIES:
        url = f"{objetivo.rstrip('/')}/{ruta}"
        try:
            # allow_redirects=False es clave: evita que un error 404 sea redirigido a un 200 (falso positivo).
            r = requests.get(url, timeout=3, allow_redirects=False)

            # Clasifica el hallazgo según el Código de Estado HTTP.
            if r.status_code == 200:
                print(Fore.GREEN + f"[+] [200 OK] -> {url}")
            elif r.status_code in [301, 302]:
                print(Fore.BLUE + f"[*] [Redirección {r.status_code}] -> {url}")
            elif r.status_code == 403:
                print(Fore.RED + f"[!] [Prohibido 403] -> {url}")
        except requests.RequestException:
            # Captura cualquier error de red (pérdida de conexión, etc.).
            pass


# --- Menú de Control ---


def menu():
    """Bucle principal que gestiona la interacción con el usuario."""
    while True:
        clear()  # Limpia la pantalla en cada iteración para mantener el orden.
        banner()  # Muestra el logo.
        print(Fore.GREEN + "[1] Ping de conectividad")
        print(Fore.GREEN + "[2] Escaneo de puertos (Nmap)")
        print(Fore.GREEN + "[3] Escaneo de subdominios (Top 20)")
        print(Fore.GREEN + "[4] WHOIS & DNS Lookup")
        print(Fore.GREEN + "[5] Escaneo de directorios web (Top 20)")
        print(Fore.RED + "[6] Salir\n")

        opcion = input(Fore.YELLOW + "Selecciona una opción: ")

        # Estructura de control para ejecutar la función seleccionada.
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
            print(Fore.RED + "\nCerrando herramientas de reconocimiento...")
            break  # Rompe el bucle 'while' y finaliza el programa.
        else:
            print(Fore.RED + "\n[!] Selección inválida.")

        # Pausa la ejecución para que el usuario pueda leer los resultados antes de limpiar.
        input(Fore.YELLOW + "\nPresiona ENTER para volver al menú...")


# Punto de entrada estándar de Python.
if __name__ == "__main__":
    menu()
