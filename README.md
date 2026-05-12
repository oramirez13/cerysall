# Cerysall

Cerysall es una herramienta de consola escrita en Python para practicar tareas básicas de reconocimiento de red y web.

## Screenshots

![Cerysall](img/Screenshot_20260226_152442.png)
![Cerysall](img/Screenshot_20260402_214739.png)
![Cerysall](img/Screenshot_20260402_214824.png)
![Cerysall](img/Screenshot_20260402_215813.png)
![Ping con detección de OS](img/cerysall_ip_ping.png)
![Escaneo nmap](img/cerysall_nmap.png)

## Funciones

- Ping con detección básica de sistema operativo por TTL.
- Escaneo rápido de puertos con `nmap`.
- Búsqueda de subdominios comunes.
- Consulta `WHOIS` y registros `A`.
- Revisión básica de directorios web frecuentes.

## Requisitos

- Python 3.11 o superior
- `nmap` instalado en el sistema para la opción de escaneo de puertos

## Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

```bash
python cerysall.py
```

## Estructura

- `cerysall.py`: archivo principal del proyecto.
- `requirements.txt`: dependencias de Python.
- `img/`: capturas opcionales del proyecto.

## Nota

Este proyecto está pensado para aprendizaje y práctica en entornos controlados.
