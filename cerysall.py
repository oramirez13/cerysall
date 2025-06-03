     1  import os
     2  import socket
     3  import subprocess
     4  import requests
     5  import whois
     6  import dns.resolver
     7  from colorama import Fore, Style, init
       
     8  init(autoreset=True)
       
     9  def clear():
    10      os.system('cls' if os.name == 'nt' else 'clear')
       
    11  def banner():
    12      print(Fore.CYAN + r'''
    13     _____ ______ _______     _______          _ _    _ _
    14    / ____|  ____|  __ \ \   / / ____|   /\   | | |  | | |
    15   | |    | |__  | |__) \ \_/ / (___    /  \  | | |  | | |
    16   | |    |  __| |  _  / \   / \___ \  / /\ \ | | |  | | |
    17   | |____| |____| | \ \  | |  ____) |/ ____ \| |____| |____
    18    \_____|______|_|  \_\ |_| |_____//_/    \_\______|______|
    19  ''')
    20      print(Fore.MAGENTA + "                    by orami – CyberSec ⚔\n")
       
    21  def ping():
    22      target = input(Fore.YELLOW + "\n[+] Ingresa la IP o dominio objetivo: ")
    23      print(Fore.YELLOW + f"[i] Haciendo ping a {target}...\n")
    24      os.system(f"ping -c 4 {target}")
       
    25  def escanear_puertos():
    26      target = input(Fore.YELLOW + "\n[+] Ingresa la IP o dominio objetivo para escanear con Nmap: ")
    27      print(Fore.YELLOW + f"[i] Escaneando puertos en {target} con Nmap...\n")
    28      os.system(f"nmap -Pn -sS -T4 {target}")
       
    29  def escanear_subdominios():
    30      dominio = input(Fore.YELLOW + "\n[+] Ingresa el dominio objetivo (ej: ejemplo.com): ")
    31      diccionario = input(Fore.YELLOW + "[+] Ruta al diccionario de subdominios (ej: subdomains.txt): ")
    32      print(Fore.YELLOW + "[i] Escaneando subdominios...\n")
    33      try:
    34          with open(diccionario, 'r', encoding='latin-1') as f:
    35              subdominios = f.read().splitlines()
    36          for sub in subdominios:
    37              url = f"http://{sub}.{dominio}"
    38              try:
    39                  requests.get(url)
    40                  print(Fore.GREEN + f"[+] Subdominio encontrado: {url}")
    41              except requests.ConnectionError:
    42                  pass
    43      except FileNotFoundError:
    44          print(Fore.RED + "[-] No se encontró el diccionario.")
       
    45  def whois_lookup():
    46      dominio = input(Fore.YELLOW + "\n[+] Ingresa el dominio objetivo: ")
    47      print(Fore.YELLOW + f"[i] Realizando WHOIS lookup para {dominio}...\n")
    48      try:
    49          w = whois.whois(dominio)
    50          print(Fore.GREEN + str(w))
    51      except:
    52          print(Fore.RED + "[-] Error en la búsqueda WHOIS.")
       
    53      print(Fore.YELLOW + f"\n[i] Realizando DNS lookup para {dominio}...\n")
    54      try:
    55          resultado = dns.resolver.resolve(dominio, 'A')
    56          for ipval in resultado:
    57              print(Fore.GREEN + f"[+] Dirección IP: {ipval.to_text()}")
    58      except:
    59          print(Fore.RED + "[-] Error en la búsqueda DNS.")
       
    60  def escanear_directorios():
    61      objetivo = input(Fore.YELLOW + "\n[+] Ingresa la URL objetivo (ej: http://ejemplo.com): ")
    62      diccionario = input(Fore.YELLOW + "[+] Ruta al diccionario de directorios (ej: wordlist.txt): ")
    63      print(Fore.YELLOW + "[i] Escaneando directorios...\n")
    64      try:
    65          with open(diccionario, 'r', encoding='latin-1') as f:
    66              rutas = f.read().splitlines()
    67          for ruta in rutas:
    68              url = f"{objetivo.rstrip('/')}/{ruta}"
    69              try:
    70                  r = requests.get(url)
    71                  if r.status_code == 200:
    72                      print(Fore.GREEN + f"[+] Encontrado: {url}")
    73              except requests.ConnectionError:
    74                  pass
    75      except FileNotFoundError:
    76          print(Fore.RED + "[-] No se encontró el diccionario.")
       
    77  def menu():
    78      while True:
    79          clear()
    80          banner()
    81          print(Fore.GREEN + "[1] Ping de conectividad")
    82          print(Fore.GREEN + "[2] Escaneo de puertos con Nmap")
    83          print(Fore.GREEN + "[3] Escaneo de subdominios")
    84          print(Fore.GREEN + "[4] WHOIS & DNS Lookup")
    85          print(Fore.GREEN + "[5] Escaneo de directorios web")
    86          print(Fore.RED + "[6] Salir\n")
       
    87          opcion = input(Fore.YELLOW + "Selecciona una opción: ")
       
    88          if opcion == '1':
    89              ping()
    90          elif opcion == '2':
    91              escanear_puertos()
    92          elif opcion == '3':
    93              escanear_subdominios()
    94          elif opcion == '4':
    95              whois_lookup()
    96          elif opcion == '5':
    97              escanear_directorios()
    98          elif opcion == '6':
    99              print(Fore.RED + "\nSaliendo...")
   100              break
   101          else:
   102              print(Fore.RED + "\n[!] Opción no válida.")
       
   103          input(Fore.YELLOW + "\nPresiona ENTER para continuar...")
       
   104  if __name__ == "__main__":
   105      menu()
