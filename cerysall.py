<<<<<<< HEAD
import os  # Interactúa con el sistema operativo (limpiar pantalla, ejecución de comandos).
import subprocess  # Permite ejecutar comandos y capturar su salida de texto para analizarla.
import requests  # Librería para realizar peticiones HTTP y auditoría web.
import whois  # Realiza consultas a bases de datos de registro de dominios.
import dns.resolver  # Resuelve registros DNS específicos como A, MX o TXT.
from colorama import Fore, init  # Proporciona colores ANSI para la interfaz de usuario.

# Inicializa colorama para que los colores se restablezcan tras cada línea.
init(autoreset=True)

# Listas internas para escaneos rápidos (Top 20 comunes).
=======
import os
import subprocess

import dns.resolver
import requests
import whois
from colorama import Fore, init

# Esta linea activa colorama para que los colores funcionen en distintas terminales.
init(autoreset=True)

# Esta lista contiene algunos subdominios comunes para una busqueda rapida.
>>>>>>> 62d488d (Preparar cerysall para GitHub)
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
<<<<<<< HEAD
=======

# Esta lista contiene algunas rutas comunes para una revision web sencilla.
>>>>>>> 62d488d (Preparar cerysall para GitHub)
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
<<<<<<< HEAD
    """Limpia la terminal según el entorno (Windows o Linux)."""
=======
    # Esta funcion limpia la pantalla segun el sistema operativo.
>>>>>>> 62d488d (Preparar cerysall para GitHub)
    os.system("cls" if os.name == "nt" else "clear")


def banner():
<<<<<<< HEAD
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
=======
    # Este bloque imprime el titulo principal de la herramienta.
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

    # Este texto muestra el autor y el enfoque general del proyecto.
    print(Fore.MAGENTA + "                    by Orami - InfoSec\n")


def pause():
    # Esta funcion espera al usuario antes de regresar al menu principal.
    input(Fore.YELLOW + "\nPresiona ENTER para continuar...")


def get_target(message):
    # Esta funcion pide un dato al usuario y elimina espacios sobrantes.
    value = input(Fore.YELLOW + message).strip()

    # Si el usuario no escribe nada, devolvemos una cadena vacia.
    return value


def ping_con_deteccion():
    # Esta linea pide la IP o dominio objetivo.
    target = get_target("\n[+] Ingresa la IP o dominio objetivo: ")

    # Si el usuario no escribio nada, mostramos un aviso simple.
    if target == "":
        print(Fore.RED + "[-] Debes ingresar un objetivo valido.")
        return

    # Esta linea informa que el analisis iniciara.
    print(Fore.YELLOW + f"[i] Analizando host {target}...\n")

    # Esta variable cambia el parametro segun el sistema operativo.
    count_parameter = "-n" if os.name == "nt" else "-c"

    # Este comando arma la llamada a ping de forma segura.
    command = ["ping", count_parameter, "4", target]

    try:
        # Esta linea ejecuta el comando y captura la salida de texto.
        result = subprocess.run(command, capture_output=True, text=True, check=False)
    except FileNotFoundError:
        # Si ping no existe en el sistema, se informa al usuario.
        print(Fore.RED + "[-] El comando ping no esta disponible en este sistema.")
        return
    except Exception as error:
        # Este bloque atrapa errores inesperados de ejecucion.
        print(Fore.RED + f"[-] Error al ejecutar ping: {error}")
        return

    # Esta linea guarda la salida en minusculas para revisar el TTL facilmente.
    output = result.stdout.lower()

    # Esta linea imprime la respuesta original del comando.
    print(result.stdout)

    # Si encontramos ttl=128, se asume un host Windows de manera basica.
    if "ttl=128" in output:
        print(Fore.CYAN + "[*] Deteccion aproximada: Windows.")
        return

    # Si encontramos ttl=64, se asume un host Linux o Unix.
    if "ttl=64" in output:
        print(Fore.CYAN + "[*] Deteccion aproximada: Linux o Unix.")
        return

    # Si hubo salida pero no un TTL conocido, se informa de forma simple.
    if result.stdout.strip() != "":
        print(Fore.CYAN + "[*] El host respondio, pero el TTL no coincide con un valor comun.")
        return

    # Si no hubo salida util, se informa que el host no respondio.
    print(Fore.RED + "[-] El host no respondio al ping.")


def escanear_puertos():
    # Esta linea pide el objetivo que se usara con nmap.
    target = get_target("\n[+] Ingresa la IP o dominio: ")

    # Si el usuario deja el campo vacio, se detiene la opcion.
    if target == "":
        print(Fore.RED + "[-] Debes ingresar un objetivo valido.")
        return

    # Esta linea indica el inicio del escaneo.
    print(Fore.YELLOW + f"[i] Iniciando Nmap sobre {target}...\n")

    try:
        # Esta linea llama a nmap con una opcion basica y facil de entender.
        subprocess.run(["nmap", "-Pn", "-F", target], check=False)
    except FileNotFoundError:
        # Este mensaje aparece si nmap no esta instalado.
        print(Fore.RED + "[-] Nmap no esta instalado o no esta en el PATH.")
    except Exception as error:
        # Este bloque informa cualquier otro error.
        print(Fore.RED + f"[-] Error al ejecutar Nmap: {error}")


def escanear_subdominios():
    # Esta linea pide el dominio base para construir las pruebas.
    domain = get_target("\n[+] Dominio base (ejemplo.com): ")

    # Si el dominio esta vacio, no continuamos.
    if domain == "":
        print(Fore.RED + "[-] Debes ingresar un dominio valido.")
        return

    # Esta bandera permite saber si se encontro al menos un subdominio.
    found_any = False

    # Este ciclo prueba cada subdominio comun definido arriba.
    for subdomain in TOP_SUBDOMAINS:
        # Esta linea forma la URL completa a consultar.
        url = f"http://{subdomain}.{domain}"

        try:
            # Esta linea intenta conectarse al sitio.
            response = requests.get(url, timeout=3)
        except requests.RequestException:
            # Si falla la conexion, simplemente pasamos al siguiente intento.
            continue

        # Si el servidor respondio, mostramos el codigo y la URL.
        print(Fore.GREEN + f"[+] Encontrado: {url} | Estado: {response.status_code}")
        found_any = True

    # Si no se encontro nada, lo indicamos al usuario.
    if not found_any:
        print(Fore.RED + "[-] No se encontraron subdominios activos en la lista basica.")


def whois_lookup():
    # Esta linea solicita el dominio que se consultara.
    domain = get_target("\n[+] Dominio: ")

    # Si el valor esta vacio, detenemos la opcion.
    if domain == "":
        print(Fore.RED + "[-] Debes ingresar un dominio valido.")
        return

    try:
        # Esta linea hace la consulta WHOIS del dominio.
        result = whois.whois(domain)

        # Estas lineas extraen dos datos faciles de leer.
        registrar = result.registrar or "No disponible"
        country = result.country or "No disponible"

        # Esta linea muestra la informacion principal.
        print(Fore.GREEN + f"[+] Registrar: {registrar} | Pais: {country}")
    except Exception as error:
        # Si falla WHOIS, se informa el error real.
        print(Fore.RED + f"[-] Error en WHOIS: {error}")

    try:
        # Esta linea consulta los registros A del dominio.
        records = dns.resolver.resolve(domain, "A")
    except Exception as error:
        # Si falla DNS, se informa aparte para no ocultar el problema.
        print(Fore.RED + f"[-] Error en DNS: {error}")
        return

    # Este ciclo imprime cada direccion IPv4 encontrada.
    for record in records:
        print(Fore.GREEN + f"[+] IPv4: {record}")


def escanear_directorios():
    # Esta linea pide la URL base que se usara para el escaneo web.
    base_url = get_target("\n[+] URL base (ej: http://192.168.1.1): ")

    # Si el usuario no escribe nada, se detiene el flujo.
    if base_url == "":
        print(Fore.RED + "[-] Debes ingresar una URL valida.")
        return

    # Si falta el protocolo, se agrega http:// para simplificar el uso.
    if not base_url.startswith("http://") and not base_url.startswith("https://"):
        base_url = "http://" + base_url

    # Esta bandera ayuda a saber si alguna ruta respondio.
    found_any = False

    # Este ciclo prueba las rutas frecuentes.
    for directory in TOP_DIRECTORIES:
        # Esta linea une la URL base con la ruta a revisar.
        url = f"{base_url.rstrip('/')}/{directory}"

        try:
            # Esta peticion evita seguir redirecciones para ver el estado real.
            response = requests.get(url, timeout=3, allow_redirects=False)
        except requests.RequestException:
            # Si falla la conexion, continuamos con la siguiente ruta.
            continue

        # Si la respuesta fue 200, se reporta como ruta encontrada.
        if response.status_code == 200:
            print(Fore.GREEN + f"[+] [200 OK] {url}")
            found_any = True

        # Si la respuesta fue una redireccion simple, tambien se muestra.
        elif response.status_code in [301, 302]:
            print(Fore.BLUE + f"[*] [Redireccion {response.status_code}] {url}")
            found_any = True

    # Si ninguna ruta dio respuesta util, se informa al final.
    if not found_any:
        print(Fore.RED + "[-] No se encontraron rutas activas en la lista basica.")


def menu():
    # Este bucle mantiene viva la aplicacion hasta que el usuario elija salir.
    while True:
        # Esta linea limpia la pantalla en cada vuelta del menu.
        clear()

        # Esta linea muestra el encabezado principal.
        banner()

        # Estas lineas imprimen las opciones disponibles.
        print(Fore.GREEN + "[1] Ping y deteccion de sistema operativo")
        print(Fore.GREEN + "[2] Escaneo basico de puertos con Nmap")
        print(Fore.GREEN + "[3] Busqueda de subdominios comunes")
        print(Fore.GREEN + "[4] Consulta WHOIS y registros A")
        print(Fore.GREEN + "[5] Escaneo de directorios web comunes")
        print(Fore.RED + "[6] Salir\n")

        # Esta linea guarda la opcion elegida por el usuario.
        option = input(Fore.YELLOW + "Selecciona una opcion: ").strip()

        # Cada bloque llama una funcion concreta segun la opcion.
        if option == "1":
            ping_con_deteccion()
            pause()
        elif option == "2":
            escanear_puertos()
            pause()
        elif option == "3":
            escanear_subdominios()
            pause()
        elif option == "4":
            whois_lookup()
            pause()
        elif option == "5":
            escanear_directorios()
            pause()
        elif option == "6":
            # Esta linea cierra el programa de forma limpia.
            print(Fore.MAGENTA + "Saliendo de Cerysall...")
            break
        else:
            # Si la opcion no existe, se informa al usuario.
            print(Fore.RED + "[!] Opcion invalida.")
            pause()


if __name__ == "__main__":
    # Esta condicion permite ejecutar el menu solo cuando el archivo se corre directamente.
>>>>>>> 62d488d (Preparar cerysall para GitHub)
    menu()
