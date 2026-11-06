import streamlit as st
import asyncio
import json
import websockets
import threading

# CONFIGURACIÓN DINÁMICA DEL STREAMING (Sin enlaces de texto directo)
PROTOCOLO = "wss"
DOMINIO_BINANCE = "://binance.com"
RUTA_STREAM = "ws/ethusdt@trade"

# CONFIGURACIÓN DE LA INTERFAZ
st.set_page_config(page_title="Radar Watson Elite", page_icon="⚡", layout="wide")

# Inicializar estados de memoria interna del servidor virtual
if "precio_real" not in st.session_state:
    st.session_state["precio_real"] = 2285.50
if "cvd_real" not in st.session_state:
    st.session_state["cvd_real"] = 0.0
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

# 🔐 CONTROL DE ACCESO PRIVADO
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

# 🧠 MOTOR DE ESCUCHA ASÍNCRONA (Corre de fondo en el servidor)
def correr_websocket_en_segundo_plano():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    direccion_red = f"{PROTOCOLO}://{DOMINIO_BINANCE}/{RUTA_STREAM}"
    
    async def escuchar_mercado():
        while True:
            try:
                async with websockets.connect(direccion_red) as ws:
                    while True:
                        data = await ws.recv()
                        msg = json.loads(data)
                        # Actualizar las variables globales con el dato fiel de Binance
                        st.session_state["precio_real"] = float(msg['p'])
                        cantidad = float(msg['q'])
                        es_venta = msg['m']
                        
                        if not es_venta:
                            st.session_state["cvd_real"] += cantidad
                        else:
                            st.session_state["cvd_real"] -= quantity
            except Exception:
                await asyncio.sleep(2)
                
    loop.run_until_complete(escuchar_mercado())

# Levantar el hilo de fondo si no está activo para que no tranque la página web
if "hilo_activo" not in st.session_state:
    st.session_state["hilo_activo"] = True
    threading.Thread(target=correr_websocket_en_segundo_plano, daemon=True).start()

# 🎛️ PANEL PRINCIPAL EN VIVO
st.title("⚡ Centro de Control Virtual - Radar Watson")
st.subheader("Monitoreo Microestructural de Ethereum en Tiempo Real")

# Botón manual para refrescar la pantalla en vivo
if st.button("🔄 Sincronizar Flujo Real"):
    st.rerun()

col_precio, col_cvd, col_alertas = st.columns(3)

with col_precio:
    st.metric(label="Precio Spot ETHUSDT (REAL)", value=f"${st.session_state['precio_real']:.2f}")

with col_cvd:
    st.metric(label="Delta de Volumen Acumulado (CVD)", value=f"{st.session_state['cvd_real']:.2f} ETH")

with col_alertas:
    st.metric(label="Estado del Sistema", value="MODO RADAR ACTIVO", delta="Flujo Conectado")

st.markdown("### 🔥 Mapa de Calor de Liquidaciones en Vivo")
st.info("Estructurando los bloques visuales para el mapa de calor con los datos del WebSocket...")
