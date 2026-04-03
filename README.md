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

```bash
python cerysall.py
```

*Nota: En sistemas Linux, algunas funciones de Nmap (como el Stealth Scan) pueden requerir privilegios de root (`sudo`).*

---

## Autor
**ORAMI (2025)**
Estudiante de Ciberseguridad | Desarrollo Web 

---

## Licencia
Este proyecto es para fines exclusivamente educativos y de hacking ético. El autor no se hace responsable del mal uso de la herramienta. Distribuido bajo Licencia MIT.
```
