# 🌱 SYRP-Aqua-Control - Sistema de Riego IoT

  
🗳️ **Descripción**

SYRP-Aqua-Control es un ecosistema inteligente de monitoreo y automatización de riego diseñado para optimizar el consumo de agua en cultivos domésticos o pequeños invernaderos. Combina una interfaz web moderna en tiempo real con un controlador de hardware robusto basado en Arduino.

---

### ✨ Características Principales

* 🌡️ **Monitoreo Multivariable**: Lectura en tiempo real de temperatura ambiente, humedad del aire, humedad del suelo y nivel crítico del tanque.
* 🤖 **Control por Histéresis**: Algoritmo inteligente que evita activaciones falsas de la bomba, protegiendo la vida útil del hardware.
* 💾 **Persistencia de Datos**: Almacenamiento automático de lecturas en una base de datos SQLite para análisis histórico.
* 🎮 **Modos de Operación**: Selector dinámico entre modo **Manual** (control directo) y **Automático** (lógica de sensores).
* ⚠️ **Alertas de Seguridad**: Detección inteligente si el sensor de humedad está fuera de la tierra o si el tanque está vacío.

---

### 🛠️ Tecnologías Utilizadas

* **Backend**: Python 3.11, PySerial (Comunicación Serial)
* **Base de Datos**: SQLite3 (Almacenamiento local de sensores)
* **Frontend**: Streamlit (Dashboard interactivo), Plotly (Gráficos), Pandas
* **Hardware**: Arduino (C++ / Wiring), Sensores DHT11, Higrómetro, Ultrasónico
* **Protocolo**: Comunicación Serial bidireccional (Baud rate: 9600)

---

### 🚀 Instalación y Configuración

#### Prerrequisitos
* Python 3.9+ instalado.
* Arduino IDE (para cargar el firmware).
* Driver para el puerto serial (CH340 o similar).

#### Configuración Local

1. **Clona el repositorio**
   ```bash
   git clone [https://github.com/yamirllancam-cloud/SYRP-Aqua-Control.git](https://github.com/yamirllancam-cloud/SYRP-Aqua-Control.git)
   cd SYRP-Aqua-Control
   2. Carga el Hardware
Abre el archivo Arduino/Arduino.ino en el IDE de Arduino y cárgalo a tu placa (Uno/Nano/Mega).

3. Ejecuta la aplicación
Inicia el dashboard interactivo con el siguiente comando:

Bash
streamlit run Proyecto_Verano.py
📋 Uso del Sistema
Conexión: Asegúrate de que el Arduino esté conectado vía USB y el puerto COM sea el correcto.

Dashboard: Observa los indicadores de colores (Verde = Óptimo, Rojo = Alerta).

Control: Activa el switch "Modo Manual" si deseas regar fuera del horario automático.

Historial: Descarga los datos de los sensores en formato CSV desde la tabla inferior.

🔧 Arquitectura del Sistema
Plaintext
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Python App    │    │    Hardware     │
│  (Streamlit)    │◄──►│   (PySerial)     │◄──►│    (Arduino)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                      │                       │
         │             ┌────────▼────────┐     ┌────────▼────────┐
         └────────────►│    SQLite3      │     │  Sensores/Relé  │
                       │   (Database)    │     │  (Humedad/Temp) │
                       └─────────────────┘     └─────────────────┘
🔐 Lógica de Control (Histéresis)
El sistema utiliza un margen de seguridad para evitar que la bomba se encienda y apague constantemente:

Umbral Crítico: Si Humedad < 30%, activar riego.

Umbral de Parada: Solo detener riego cuando Humedad > 60%.

Seguridad: Si el nivel del tanque es < 5cm, la bomba se bloquea automáticamente para evitar que trabaje en seco.

📊 Estructura del Repositorio
Proyecto_Verano.py: Lógica principal y Dashboard de Streamlit.

Arduino/: Firmware oficial para la placa controladora.

requirements.txt: Librerías necesarias (pandas, plotly, streamlit, pyserial).

database.db: Base de datos generada automáticamente.

planta.png: Activos visuales de la interfaz.

📞 Contacto
Desarrollador: yamir.llanca.m@uni.pe

Proyecto: Sistema de Control de Riego Inteligente - Verano 2026

🌱 SYRP-Aqua-Control - Cuidando cada gota mediante tecnología e ingeniería.
