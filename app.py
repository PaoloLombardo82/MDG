# app.py

import streamlit as st
from utils import descargar_datos, calcular_indicadores
from model import entrenar_modelo
from graficos import generar_grafico
from telegram_utils import enviar_alerta
import asyncio
from config import ACTIVOS_ANALIZAR

st.set_page_config(page_title="📈 Botmagia", layout="wide")
st.title("⚡ Analizador Bursátil en Tiempo Real")

# Mostrar categorías y activos
categorias = st.multiselect("Categoría", list(ACTIVOS_ANALIZAR.keys()), default=["Criptos"])
activo_seleccionado = st.selectbox("Elige un activo:", [
    ticker for categoria in categorias for ticker in ACTIVOS_ANALIZAR[categoria]
])

if st.button("🔍 Analizar"):
    with st.spinner(f"Analizando {activo_seleccionado}..."):
        try:
            # Descargar datos minutales
            data, close_series = descargar_datos(activo_seleccionado, periodo='1d', intervalo='1m')
            if data.empty:
                st.warning("⚠️ No se encontraron datos suficientes para este activo.")
            else:
                # Calcular indicadores técnicos
                data = calcular_indicadores(data, close_series)

                if data.empty or len(data) < 2:
                    st.error("❌ No hay datos suficientes para hacer predicciones")
                else:
                    # Entrenar modelo y predecir
                    modelo, muestra = entrenar_modelo(data)
                    if modelo is None or muestra is None:
                        st.warning("⚠️ No se pudo entrenar el modelo")
                    else:
                        probabilidad = modelo.predict_proba(muestra)[0]

                        col1, col2 = st.columns(2)
                        col1.metric("Probabilidad de alza", f"{probabilidad[1]:.2%}")
                        col2.metric("Probabilidad de baja", f"{probabilidad[0]:.2%}")

                        # Gráfico interactivo
                        fig = generar_grafico(data, activo_seleccionado)
                        st.plotly_chart(fig, use_container_width=True)

                        # Enviar alerta si hay señal clara
                        umbral = 0.85
                        if probabilidad[1] > umbral:
                            mensaje = f"🟢 ¡Alza inminente en {activo_seleccionado}!\n"
                            mensaje += f"📈 Probabilidad: {probabilidad[1]:.2%}"
                            asyncio.run(enviar_alerta(mensaje))
                            st.success("✅ Alerta de alza enviada por Telegram")

                        elif probabilidad[0] > umbral:
                            mensaje = f"🔴 ¡Baja inminente en {activo_seleccionado}!\n"
                            mensaje += f"📉 Probabilidad: {probabilidad[0]:.2%}"
                            asyncio.run(enviar_alerta(mensaje))
                            st.success("✅ Alerta de baja enviada por Telegram")

                        else:
                            st.info("🟡 Señal no concluyente → Sin alerta")

        except Exception as e:
            st.error(f"❌ Error al analizar {activo_seleccionado}: {e}")