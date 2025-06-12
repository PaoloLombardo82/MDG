# app.py

import streamlit as st  # ✅ Importa aquí para evitar NameError
from utils import descargar_datos, calcular_indicadores
from model import entrenar_modelo
from news_nlp import buscar_noticias, analizar_sentimiento
from graficos import generar_grafico
from config import ACTIVOS_ANALIZAR

st.set_page_config(page_title="📈 Botmagia", layout="wide")
st.title("📱 Analizador Bursátil Móvil")