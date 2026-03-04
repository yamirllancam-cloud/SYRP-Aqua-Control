import streamlit as st
import serial
import pandas as pd
import time
from datetime import datetime
import collections
import plotly.express as px
import sqlite3
#1CAPA DE DATOS (SQLite)
class DatabaseManager:
    def __init__(self, db_name='riego_data.db'):
        self.db_name = db_name
        self._init_db()
    def _init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS registros 
                            (fecha_hora TEXT, temp REAL, hum_a REAL, hum_s INTEGER, nivel INTEGER, bomba TEXT)''')
    def guardar_registro(self, datos, estado_bomba):
        try:
            with sqlite3.connect(self.db_name) as conn:
                conn.execute("INSERT INTO registros VALUES (?,?,?,?,?,?)",
                             (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                              datos['Temp_Ambiente'], datos['Hum_Ambiente'],
                              datos['Hum_Suelo'], datos['Nivel_Agua'], estado_bomba))
        except:
            pass
    def obtener_ultimos(self, limite=15):
        try:
            with sqlite3.connect(self.db_name) as conn:
                return pd.read_sql_query(f"SELECT * FROM registros ORDER BY fecha_hora DESC LIMIT {limite}", conn)
        except:
            return pd.DataFrame()
#2CAPA DE HARDWARE(Comunicación Arduino)
class ArduinoHandler:
    def __init__(self, puerto, baudios=9600):
        self.puerto = puerto
        self.baudios = baudios
        self.conexion = self._conectar()
    def _conectar(self):
        try:
            return serial.Serial(self.puerto, self.baudios, timeout=1)
        except:
            return None
    def leer_sensores(self):
        if not self.conexion: return None
        try:
            if self.conexion.in_waiting > 0:
                linea = self.conexion.readline().decode('utf-8', errors='ignore').strip()
                if "|" in linea and ":" in linea:
                    raw = dict(item.split(":") for item in linea.split("|"))
                    return {
                        "Temp_Ambiente": float(raw.get('T', 0)),
                        "Hum_Ambiente": float(raw.get('HA', 0)),
                        "Hum_Suelo": int(float(raw.get('HS', 0))),
                        "Nivel_Agua": int(float(raw.get('N', 0))),
                        "Hora": datetime.now().strftime("%H:%M:%S")
                    }
        except:
            pass
        return None
    def enviar_comando(self, comando):
        if self.conexion:
            self.conexion.write(f"{comando}\n".encode())
#3CAPA LÓGICA(Reglas de Negocio/Histéresis)
class ControladorRiego:
    def __init__(self, puerto='COM3'):
        self.hardware = ArduinoHandler(puerto)
        self.db = DatabaseManager()
        self.historial = collections.deque(maxlen=50)
        self.bomba_encendida = False
    def procesar_control(self, modo, umbral, margen, datos):
        h_suelo = datos['Hum_Suelo']
        # Seguridad: Evitar riego si el sensor no detecta suelo
        if h_suelo <= 2:
            if self.bomba_encendida: self.apagar_bomba()
            return "ALERTA", "⚠️ SENSOR FUERA DE TIERRA"
        # Lógica de histéresis
        if modo == "Automático":
            if h_suelo < umbral and not self.bomba_encendida:
                self.encender_bomba()
            elif h_suelo >= (umbral + margen) and self.bomba_encendida:
                self.apagar_bomba()
            msg = "BOMBA: ENCENDIDA (AUTO) 🌊" if self.bomba_encendida else "ESTADO: EN ESPERA ✅"
            return "OK", msg
        else:
            msg = "BOMBA: ENCENDIDA (MANUAL) 🌊" if self.bomba_encendida else "BOMBA: APAGADA (MANUAL)"
            return "MANUAL", msg
    def encender_bomba(self):
        self.hardware.enviar_comando("R:ON")
        self.bomba_encendida = True
    def apagar_bomba(self):
        self.hardware.enviar_comando("R:OFF")
        self.bomba_encendida = False
#4CAPA DE INTERFAZ(Estética y Renderizado)
class SYRPAquaUI:
    def __init__(self, controlador):
        self.ctrl = controlador
        self._configurar_estilos()
    def _configurar_estilos(self):
        st.set_page_config(page_title="SYRP-Aqua Control", layout="wide")
        st.markdown("""
            <style>
            .stApp { background-color: #0b0d11; }
            /* Estilo para los números grandes y claros */
            [data-testid="stMetricValue"] {
                font-size: 48px !important;
                font-weight: 800 !important;
                color: #00ff88 !important;
                text-shadow: 0px 0px 15px rgba(0, 255, 136, 0.4);
            }
            [data-testid="stMetricLabel"] {
                font-size: 18px !important;
                color: #ffffff !important;
                font-weight: 500;
            }
            div[data-testid="stMetric"] {
                background: rgba(255,255,255,0.04);
                border: 2px solid #00ff88;
                border-radius: 12px;
                padding: 15px;
            }
            .status-card { 
                padding: 20px; border-radius: 10px; text-align: center; 
                font-size: 24px; font-weight: bold; border: 2px solid #00ff88; 
                color: #00ff88; background: rgba(0,255,136,0.1); 
            }
            .warning-card { 
                padding: 20px; border-radius: 10px; text-align: center; 
                font-size: 24px; font-weight: bold; border: 2px solid #ff4b4b; 
                color: #ff4b4b; background: rgba(255,75,75,0.1); 
            }
            </style>
        """, unsafe_allow_html=True)

    def renderizar_estructura(self):
        st.title("🌱 SYRP-Aqua-Control")
        tab1, tab2 = st.tabs(["📊 Panel de Control", "🗄️ Historial de Datos"])
        with tab1:
            m1, m2, m3, m4 = st.columns(4)
            self.ph_temp = m1.empty()
            self.ph_hum_a = m2.empty()
            self.ph_hum_s = m3.empty()
            with m4:
                st.markdown(
                    "<p style='color:white; font-size:16px; margin-bottom:5px; font-weight:600;'>Nivel del Tanque</p>",
                    unsafe_allow_html=True)
                self.ph_pb_nivel = st.progress(0)
                self.ph_txt_nivel = st.empty()
            st.markdown("<br>", unsafe_allow_html=True)
            c_izq, c_der = st.columns([2.5, 1])
            self.ph_grafica = c_izq.empty()
            with c_der:
                st.subheader("⚙️ Configuración")
                self.ph_status = st.empty()
                st.markdown("---")
                modo = st.radio("Modo de Operación", ["Automático", "Manual"], horizontal=True)
                umbral = st.slider("Umbral de Riego %", 0, 100, 60)
                if modo == "Manual":
                    st.info("Control de Actuadores")
                    b1, b2 = st.columns(2)
                    if b1.button("🌊 ENCENDER", use_container_width=True, type="primary"):
                        self.ctrl.encender_bomba()
                    if b2.button("🛑 APAGAR", use_container_width=True):
                        self.ctrl.apagar_bomba()
        with tab2:
            st.subheader("Registros en Base de Datos")
            self.ph_tabla_db = st.empty()
        return modo, umbral
    def actualizar_datos_pantalla(self, datos, info, historial, umbral):
        # Actualizar valores métricos
        self.ph_temp.metric("Temperatura", f"{datos['Temp_Ambiente']}°C")
        self.ph_hum_a.metric("Humedad Aire", f"{datos['Hum_Ambiente']}%")
        self.ph_hum_s.metric("Humedad Suelo", f"{datos['Hum_Suelo']}%")
        # Nivel visual del tanque
        nivel_norm = max(0, min(datos['Nivel_Agua'] / 100, 1.0))
        self.ph_pb_nivel.progress(nivel_norm)
        self.ph_txt_nivel.markdown(
            f"<p style='text-align:right; color:#00ff88; font-weight:900; font-size:20px;'>{datos['Nivel_Agua']}%</p>",
            unsafe_allow_html=True)
        # Estado del sistema
        clase = "warning-card" if info[0] == "ALERTA" else "status-card"
        self.ph_status.markdown(f'<div class="{clase}">{info[1]}</div>', unsafe_allow_html=True)
        # Gráfica de monitoreo
        df = pd.DataFrame(list(historial))
        fig = px.area(df, x="Hora", y="Hum_Suelo", template="plotly_dark")
        fig.add_hline(y=umbral, line_dash="dash", line_color="#ff4b4b", annotation_text="Punto de Riego")
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(range=[0, 105], title="Humedad (%)"),
            margin=dict(l=0, r=0, t=30, b=0), height=450
        )
        fig.update_traces(line_color='#00ff88', fillcolor='rgba(0, 255, 136, 0.1)')
        self.ph_grafica.plotly_chart(fig, use_container_width=True)
        # Tabla de persistencia
        df_db = self.ctrl.db.obtener_ultimos(15)
        self.ph_tabla_db.dataframe(df_db, use_container_width=True)
#5INICIALIZACIÓN Y BUCLE PRINCIPAL
if __name__ == "__main__":
    @st.cache_resource
    def bootstrap():
        return ControladorRiego('COM3')
    ctrl = bootstrap()
    app = SYRPAquaUI(ctrl)
    # Renderizar estructura estática
    modo_sel, umbral_sel = app.renderizar_estructura()
    if ctrl.hardware.conexion:
        while True:
            datos_raw = ctrl.hardware.leer_sensores()
            if datos_raw:
                # Lógica de riego
                info_sis = ctrl.procesar_control(modo_sel, umbral_sel, 10, datos_raw)
                # Almacenar en memoria y DB
                ctrl.historial.append(datos_raw)
                ctrl.db.guardar_registro(datos_raw, "ENCENDIDO" if ctrl.bomba_encendida else "APAGADO")
                # Actualizar interfaz
                app.actualizar_datos_pantalla(datos_raw, info_sis, ctrl.historial, umbral_sel)

            time.sleep(1)  # Telemetría de 1Hz es ideal
    else:
        st.error("❌ Conexión Serial Fallida. Verifica que el Arduino esté en COM3.")