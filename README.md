# 🌱 SYRP-Aqua-Control - Sistema de Riego IoT

## 🗳️ Descripción

**SYRP-Aqua-Control** es un ecosistema inteligente de monitoreo y automatización de riego diseñado para optimizar el consumo de agua en cultivos domésticos o pequeños invernaderos.

Combina una interfaz web moderna en tiempo real con un controlador de hardware robusto basado en Arduino.

---

## ✨ Características Principales

- 🌡️ **Monitoreo Multivariable**
  - Temperatura ambiente
  - Humedad del aire
  - Humedad del suelo
  - Nivel crítico del tanque

- 🤖 **Control por Histéresis**
  - Evita activaciones falsas de la bomba
  - Protege la vida útil del hardware

- 💾 **Persistencia de Datos**
  - Almacenamiento automático en base de datos SQLite
  - Análisis histórico de lecturas

- 🎮 **Modos de Operación**
  - **Manual** → Control directo de la bomba
  - **Automático** → Control inteligente basado en sensores

- ⚠️ **Alertas de Seguridad**
  - Sensor fuera de la tierra
  - Tanque vacío
  - Protección contra funcionamiento en seco

---

## 🛠️ Tecnologías Utilizadas

### Backend
- Python 3.11
- PySerial (Comunicación Serial)

### Base de Datos
- SQLite3

### Frontend
- Streamlit
- Plotly
- Pandas

### Hardware
- Arduino (C++ / Wiring)
- Sensor DHT11
- Higrómetro de suelo
- Sensor ultrasónico

### Protocolo
- Comunicación Serial bidireccional
- Baud rate: `9600`

---

## 🚀 Instalación y Configuración

### 🔹 Prerrequisitos

- Python 3.9+
- Arduino IDE
- Driver CH340 (o similar para el puerto serial)

---

### 🔹 Configuración Local

#### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/yamirllancam-cloud/SYRP-Aqua-Control.git
cd SYRP-Aqua-Control
```

#### 2️⃣ Cargar el Hardware

- Abrir `Arduino/Arduino.ino` en el IDE de Arduino.
- Seleccionar la placa (Uno / Nano / Mega).
- Subir el firmware a la placa.

#### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 4️⃣ Ejecutar la aplicación

```bash
streamlit run Proyecto_Verano.py
```

---

# 📋 Uso del Sistema

## 🔌 Conexión

- Conectar el Arduino vía USB.
- Verificar que el puerto COM seleccionado sea el correcto.

## 📊 Dashboard

- 🟢 Verde → Valores óptimos.
- 🔴 Rojo → Alerta.

## 🎮 Control

- Activar **"Modo Manual"** para riego inmediato.
- En **Modo Automático**, el sistema ejecuta la lógica basada en sensores.

## 📥 Historial

- Descargar datos en formato **CSV** desde la tabla inferior del dashboard.

---

# 🔧 Arquitectura del Sistema

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Python App    │    │    Hardware     │
│  (Streamlit)    │◄──►│   (PySerial)     │◄──►│    (Arduino)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                      │                       │
         │             ┌────────▼────────┐     ┌────────▼────────┐
         └────────────►│    SQLite3      │     │  Sensores/Relé  │
                       │   (Database)    │     │  (Humedad/Temp) │
                       └─────────────────┘     └─────────────────┘
```

---

# 🔐 Lógica de Control (Histéresis)

El sistema utiliza un margen de seguridad para evitar encendidos y apagados constantes de la bomba:

### 🔹 Umbral Crítico
Si **Humedad < 30%** → Activar riego.

### 🔹 Umbral de Parada
Solo detener riego cuando **Humedad > 60%**.

### 🔹 Seguridad del Tanque
Si el nivel es **< 5 cm** → Bloqueo automático de la bomba.

---

# 📊 Estructura del Repositorio

```
SYRP-Aqua-Control/
│
├── Proyecto_Verano.py        # Dashboard + lógica principal
├── Arduino/
│   └── Arduino.ino           # Firmware del microcontrolador
├── requirements.txt          # Dependencias
├── database.db               # Base de datos (auto-generada)
├── planta.png                # Activos visuales
└── README.md
```

---

# 📞 Contacto

**Desarrollador:** yamir.llanca.m@uni.pe  
**Proyecto:** Sistema de Control de Riego Inteligente - Verano 2026  

---

# 🌱 SYRP-Aqua-Control  
### *Cuidando cada gota mediante tecnología e ingeniería.*
