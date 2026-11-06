# Radio Central - Puente de memoria interna para evitar congelamientos en la interfaz
import json

class RadioCentral:
    def __init__(self):
        # Archivo temporal local en el servidor para almacenar el último dato real
        self.ruta_memoria = "memoria_radio.json"

    def emitir_alerta(self, precio, cvd):
        """Guarda los datos reales del mercado en la memoria compartida"""
        datos = {
            "precio_real": float(precio),
            "cvd_real": float(cvd)
        }
        try:
            with open(self.ruta_memoria, "w") as f:
                json.dump(datos, f)
        except Exception:
            pass

    def sintonizar_radio(self):
        """Lee el último dato guardado por los radares para pasárselo a la pantalla"""
        try:
            with open(self.ruta_memoria, "r") as f:
                return json.load(f)
        except Exception:
            # Si el archivo no existe aún, devuelve los valores por defecto de Thony
            return {"precio_real": 2285.50, "cvd_real": 0.00}
