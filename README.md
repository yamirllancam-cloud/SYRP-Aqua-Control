# 🌱 SYRP-Aqua-Control

## 🗳️ Descripción

**SYRP-Aqua-Control** es un ecosistema inteligente de monitoreo y automatización de riego diseñado para optimizar el consumo de agua en cultivos domésticos o pequeños invernaderos.

Combina una interfaz web moderna en tiempo real con un controlador de hardware robusto basado en Arduino, permitiendo control automático, manual y almacenamiento histórico de datos.

---

## ✨ Características Principales

- 🌡️ **Monitoreo Multivariable**
  - Temperatura ambiente
  - Humedad del aire
  - Humedad del suelo
  - Nivel crítico del tanque

- 🤖 **Control por Histéresis**
  - Evita activaciones falsas de la bomba
  - Reduce el desgaste del relé
  - Mejora la estabilidad del sistema

- 💾 **Persistencia de Datos**
  - Almacenamiento automático en base de datos SQLite
  - Registro histórico de lecturas
  - Exportación de datos en CSV

- 🎮 **Modos de Operación**
  - **Manual** → Control directo de la bomba desde el dashboard
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
- Verificar que el puerto COM seleccionado sea el correcto en el archivo principal.
- Presionar **Conectar** en el dashboard.

## 📊 Dashboard

- 🟢 Verde → Valores dentro del rango óptimo.
- 🔴 Rojo → Estado de alerta o riesgo.

## 🎮 Control

- Activar **Modo Manual** para encender/apagar la bomba manualmente.
- En **Modo Automático**, el sistema ejecuta la lógica basada en sensores y umbrales definidos.

## 📥 Historial

- Visualización gráfica en tiempo real.
- Tabla con últimos registros almacenados.
- Descarga de datos en formato **CSV**.

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
Si el nivel es **< 5 cm** → Bloqueo automático de la bomba para evitar funcionamiento en seco.

---

# 📊 Estructura del Repositorio

```
SYRP-Aqua-Control/
│
├── Proyecto_Verano.py          # Aplicación principal (Dashboard + lógica de control)
├── Arduino/
│   └── Arduino.ino             # Firmware del microcontrolador
│
├── requirements.txt            # Dependencias del proyecto Python
├── README.md                   # Documentación principal del proyecto
│
├── database.db                 # Base de datos SQLite (se genera automáticamente)
├── planta.png                  # Recursos gráficos del dashboard
│
└── .gitignore                  # Archivos excluidos del control de versiones
```

---

# 📞 Contacto

**Desarrollador:** yamir.llanca.m@uni.pe  
**Proyecto:** Sistema de Control de Riego Inteligente - Verano 2026  

---

# 🌱 SYRP-Aqua-Control  
### *Cuidando cada gota mediante tecnología e ingeniería.*
