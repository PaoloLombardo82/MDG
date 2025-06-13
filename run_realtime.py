# run_realtime.py

import asyncio
import time
from utils import descargar_datos, calcular_indicadores
from model import entrenar_modelo
from telegram_utils import enviar_alerta

async def analizar_activo(ticker):
    try:
        data, close_series = descargar_datos(ticker, periodo="1d", intervalo="1m")
        data = calcular_indicadores(data, close_series)
        modelo, muestra = entrenar_modelo(data)

        if modelo is not None and len(muestra) > 0:
            probabilidad = modelo.predict_proba(muestra)[0]

            if probabilidad[1] > 0.85:
                mensaje = f"⚡ ¡Alza inminente en {ticker}!\n📈 Probabilidad: {probabilidad[1]:.2%}"
                await enviar_alerta(mensaje)

            elif probabilidad[0] > 0.85:
                mensaje = f"⚠️ ¡Baja inminente en {ticker}!\n📉 Probabilidad: {probabilidad[0]:.2%}"
                await enviar_alerta(mensaje)

    except Exception as e:
        print(f"❌ Error al analizar {ticker}: {e}")

# Bucle infinito de análisis
while True:
    asyncio.run(analizar_activo("BTC-USD"))
    print("⏳ Esperando 60 segundos antes del próximo análisis...")
    time.sleep(60)  # espera 1 minuto antes de volver a analizar