<<<<<<< HEAD
# CerySall - Infra Recon Tool

CerySall es una herramienta modular de reconocimiento desarrollada en Python. Está diseñada para automatizar las fases iniciales de un Pentest, permitiendo obtener una visión rápida de la superficie de ataque de un objetivo.

## Características Principales

* **Conectividad ICMP**: Verificación de estado del host (Ping) con detección automática de sistema operativo (Windows/Linux).
* **Escaneo de Puertos**: Integración con Nmap para identificar servicios activos (Top 100 ports).
* **Fuzzing de Subdominios**: Identificación de subdominios críticos mediante una lista optimizada de los 20 más comunes.
* **Inteligencia de Dominios**: Consultas WHOIS (registro) y resolución de registros DNS Tipo A.
* **Web Enumeration**: Descubrimiento de directorios y archivos sensibles (.env, backup, admin) con manejo inteligente de códigos de estado HTTP.

## Requisitos Previos

1. **Python 3.10+**: Es necesario instalar la versión más reciente de Python.
2. **Nmap**: El sistema debe tener Nmap instalado y disponible en el PATH para las funciones de escaneo de puertos.

## Instalación

Se debe clonar el repositorio y utilizar un entorno virtual para gestionar las dependencias:

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: .\venv\Scripts\activate

# Instalar librerías necesarias
pip install -r requirements.txt
```

## Uso

Para iniciar la herramienta, se debe ejecutar el script principal:
=======
# Cerysall

Cerysall es una herramienta de consola escrita en Python para practicar tareas básicas de reconocimiento de red y web.

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
>>>>>>> 62d488d (Preparar cerysall para GitHub)

```bash
python cerysall.py
```

<<<<<<< HEAD
*Nota: En sistemas Linux, algunas funciones de Nmap (como el Stealth Scan) pueden requerir privilegios de root (`sudo`).*

---

## Autor
**ORAMI (2025)**
Estudiante de Ciberseguridad | Desarrollo Web 

---

## Licencia
Este proyecto es para fines exclusivamente educativos y de hacking ético. El autor no se hace responsable del mal uso de la herramienta. Distribuido bajo Licencia MIT.
```
=======
## Estructura

- `cerysall.py`: archivo principal del proyecto.
- `requirements.txt`: dependencias de Python.
- `img/`: capturas opcionales del proyecto.

## Nota

Este proyecto está pensado para aprendizaje y práctica en entornos controlados.
>>>>>>> 62d488d (Preparar cerysall para GitHub)
