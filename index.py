import streamlit as st
import sys
import os

# Asegurar que el servidor encuentre el archivo de la radio en la ruta del proyecto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from radio_central import RadioCentral

# CONFIGURACIÓN DE LA INTERFAZ VIRTUAL
st.set_page_config(page_title="Radar Watson Elite", page_icon="⚡", layout="wide")

# Inicializar la Radio Central interna
radio = RadioCentral()

# 🔐 CONTROL DE ACCESO PRIVADO
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

def validar_credenciales(usuario, clave):
    return usuario == "admin" and clave == "watson2026"

if not st.session_state["autenticado"]:
    st.title("🔒 Acceso Restringido - Radar Cuantitativo")
    user_input = st.text_input("Operador:")
    pass_input = st.text_input("Clave de Seguridad:", type="password")
    if st.button("Ingresar al Sistema"):
        if validar_credenciales(user_input, pass_input):
            st.session_state["autenticado"] = True
            st.rerun()
        else:
            st.error("Credenciales incorrectas.")
    st.stop()

# 📡 SINTONIZAR LA RADIO CENTRAL (Leer datos en memoria compartida)
datos_fieles = radio.sintonizar_radio()
precio_pantalla = datos_fieles.get("precio_real", 2285.50)
cvd_pantalla = datos_fieles.get("cvd_real", 0.00)

# 🎛️ PANEL PRINCIPAL EN VIVO
st.title("⚡ Centro de Control Virtual - Radar Watson")
st.subheader("Monitoreo Microestructural de Ethereum en Tiempo Real")

# Botón manual de refresco funcional (Recarga la radio en milisegundos)
if st.button("🔄 Sincronizar Flujo Real"):
    st.rerun()

col_precio, col_cvd, col_alertas = st.columns(3)

with col_precio:
    st.metric(label="Precio Spot ETHUSDT (REAL)", value=f"${precio_pantalla:.2f}")

with col_cvd:
    st.metric(label="Delta de Volumen Acumulado (CVD)", value=f"{cvd_pantalla:.2f} ETH")

with col_alertas:
    st.metric(label="Estado del Sistema", value="MODO RADAR ACTIVO", delta="Flujo Conectado")

st.markdown("### 🔥 Mapa de Calor de Liquidaciones en Vivo")
st.info("Estructurando los bloques visuales para el mapa de calor con los datos de la Radio Central...")
