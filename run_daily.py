# run_daily.py

import asyncio
from telegram_utils import enviar_alerta
from model import entrenar_modelo
from utils import descargar_datos, calcular_indicadores

async def analizar_activo(ticker):
    print(f"📊 Analizando {ticker}...")
    data, close_series = descargar_datos(ticker)
    data = calcular_indicadores(data, close_series)
    modelo, muestra = entrenar_modelo(data)

    if modelo is not None:
        probabilidad = modelo.predict_proba(muestra)[0]
        mensaje = ""

        if probabilidad[1] > 0.85:
            mensaje = f"🟢 Alta probabilidad de alza en {ticker}\nProbabilidad: {probabilidad[1]:.2%}"

        elif probabilidad[0] > 0.85:
            mensaje = f"🔴 Alta probabilidad de baja en {ticker}\nProbabilidad: {probabilidad[0]:.2%}"

        if mensaje:
            await enviar_alerta(mensaje)

# Ejecutar análisis automático
async def main():
    activos = ["BTC-USD", "TSLA", "GC=F"]
    for ticker in activos:
        await analizar_activo(ticker)

if __name__ == "__main__":
    asyncio.run(main())