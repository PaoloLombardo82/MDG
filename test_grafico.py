# test_grafico.py

from utils import descargar_datos, calcular_indicadores
from graficos import generar_grafico

# Paso 1: Descargar datos
data, close_series = descargar_datos("BTC-USD")

# Paso 2: Calcular indicadores técnicos
data = calcular_indicadores(data, close_series)

# Paso 3: Generar gráfico interactivo
fig = generar_grafico(data, "BTC-USD")

# Paso 4: Mostrar gráfico en navegador
fig.show()