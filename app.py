import streamlit as st
from utils import descargar_datos, calcular_indicadores
from model import entrenar_modelo
from graficos import generar_grafico
from config import ACTIVOS_ANALIZAR

st.set_page_config(page_title="📈 Botmagia", layout="wide")
st.title("📱 Analizador Bursátil Móvil")

categorias = st.multiselect("Categoría", list(ACTIVOS_ANALIZAR.keys()), default=["Criptos"])

tickers_a_analizar = []
for categoria in categorias:
    tickers_a_analizar.extend(ACTIVOS_ANALIZAR[categoria])

activo_seleccionado = st.selectbox("Elige un activo:", tickers_a_analizar)

if st.button("🔍 Analizar"):
    with st.spinner(f"Analizando {activo_seleccionado}..."):
        try:
            data, close_series = descargar_datos(activo_seleccionado)
            data = calcular_indicadores(data, close_series)

            if data.empty:
                st.error("❌ No se encontraron datos suficientes para este activo.")
            else:
                modelo, muestra = entrenar_modelo(data)
                if modelo is None:
                    st.warning("⚠️ No se pudo entrenar el modelo")
                else:
                    probabilidad = modelo.predict_proba(muestra)[0]
                    col1, col2 = st.columns(2)
                    col1.metric("Probabilidad de alza", f"{probabilidad[1]:.2%}")
                    col2.metric("Probabilidad de baja", f"{probabilidad[0]:.2%}")

                    fig = generar_grafico(data, activo_seleccionado)
                    st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error al analizar {activo_seleccionado}: {e}")