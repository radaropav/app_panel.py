import asyncio
import json
import websockets

# CONFIGURACIÓN DEL ENTORNO CRUDO (Sin enlaces de texto directo para evitar roturas de interfaz)
PROTOCOLO = "wss"
DOMINIO_EXCHANGE = "://binance.com"
ENDPOINT_STREAM = "ws/ethusdt@trade"

class RadarMercado:
    def __init__(self):
        self.cvd_acumulado = 0.0
        self.umbral_bloque_ballena = 500.0  # Filtrar bloques institucionales (>500 ETH)

    async def conectar_radar(self):
        # Ensamblaje dinámico de la dirección de red
        direccion_red = f"{PROTOCOLO}://{DOMINIO_EXCHANGE}/{ENDPOINT_STREAM}"
        print("🚀 Inicializando trinchera cuántica... Conectando al flujo crudo de ETHUSDT.")
        
        while True:
            try:
                async with websockets.connect(direccion_red) as ws:
                    print("📡 Conexión fiel establecida con el stream de datos. Escaneando tras bambalinas...")
                    while True:
                        data = await ws.recv()
                        msg = json.loads(data)
                        
                        # Extracción de la cinta de ejecuciones en tiempo real (Time & Sales)
                        precio = float(msg['p'])
                        cantidad = float(msg['q'])
                        es_venta_market = msg['m']  # True si es venta agresiva, False si es compra agresiva
                        
                        # 🧮 Cálculo matemático del CVD (Cumulative Volume Delta)
                        if not es_venta_market:
                            self.cvd_acumulado += cantidad  # Presión de compra agresiva
                        else:
                            self.cvd_acumulado -= cantidad  # Presión de venta agresiva
                            
                        # 🐋 Radar de bloques gigantes (Huellas institucionales)
                        if cantidad >= self.umbral_bloque_ballena:
                            tipo_orden = "SHORT" if es_venta_market else "LONG"
                            print(f"⚠️ [ALERTA BALLENA] Ejecución pesada {tipo_orden}: {cantidad} ETH a ${precio} USDT | CVD: {self.cvd_acumulado:.2f}")
                            
                            # En el siguiente paso, este bloque enviará la señal directa a Redis
                            
            except (websockets.exceptions.ConnectionClosed, Exception) as e:
                print(f"❌ Conexión interrumpida: {e}. Reiniciando canal de forma independiente en 2 segundos...")
                await asyncio.sleep(2)

if __name__ == "__main__":
    radar = RadarMercado()
    try:
        asyncio.run(radar.conectar_radar())
    except KeyboardInterrupt:
        print("🛑 Radar detenido manualmente por el operador.")
