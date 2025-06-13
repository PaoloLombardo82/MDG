# app.py

import streamlit as st
from utils import descargar_datos, calcular_indicadores
from model import entrenar_modelo
from news_nlp import buscar_noticias, analizar_sentimiento
from graficos import generar_grafico
from config import ACTIVOS_ANALIZAR

st.set_page_config(page_title="📈 Botmagia", layout="wide")
st.title("📱 Analizador Bursátil Móvil")

import config
st.markdown("🔹 Selecciona un activo:")
activo_seleccionado = st.selectbox(" ", config.ALL_TICKERS)
if st.button("🔍 Analizar"):
    with st.spinner(f"Analizando {activo_seleccionado}..."):
        try:
            data, close_series = descargar_datos(activo_seleccionado)
            st.markdown("🔹 Datos descargados:")
            st.write(data.tail())

            data = calcular_indicadores(data, close_series)
            st.markdown("🔹 Indicadores técnicos:")
            st.write(data[['close', 'RSI', 'SMA_20', 'SMA_50']].tail())

            modelo, muestra = entrenar_modelo(data)
            probabilidad = modelo.predict_proba(muestra)[0]

            query = activo_seleccionado.replace("-USD", "").replace("-F", "")
            noticias = buscar_noticias(query)
            polaridad = analizar_sentimiento(noticias)

            ajuste_nlp = 0.1 * polaridad
            prob_alza = max(0.05, min(0.95, probabilidad[1] + ajuste_nlp))
            prob_baja = 1 - prob_alza

            col1, col2 = st.columns(2)
            col1.metric("Probabilidad de alza", f"{prob_alza:.2%}")
            col2.metric("Probabilidad de baja", f"{prob_baja:.2%}")

            fig = generar_grafico(data, activo_seleccionado)
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("📰 Últimas noticias")
            for n in noticias[:5]:
                st.markdown(f"- {n}")

            st.markdown(f"🔹 Sentimiento: {'🟢 Positivo' if polaridad > 0.2 else '🔴 Negativo' if polaridad < -0.2 else '🟡 Neutro'}")

        except Exception as e:
            st.error(f"❌ Error al analizar {activo_seleccionado}: {e}")