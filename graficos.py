# graficos.py

import plotly.graph_objs as go
from datetime import datetime
import os

def generar_grafico(data, ticker):
    """Genera un gráfico interactivo del precio y RSI"""

    # Verificar si se han calculado los indicadores necesarios
    if 'RSI' not in data.columns:
        from utils import calcular_indicadores
        close_series = data['close'].squeeze()
        data = calcular_indicadores(data, close_series)

    # Crear gráfico interactivo
    fig = go.Figure()

    # Precio Close
    fig.add_trace(go.Scatter(x=data.index, y=data['close'], name='Precio', line=dict(color='black')))
    
    # Medias Móviles (SMA 20 y SMA 50)
    if 'SMA_20' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], name='SMA 20', line=dict(color='blue')))
    
    if 'SMA_50' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], name='SMA 50', line=dict(color='orange')))

    fig.update_layout(
        title=f"Precio y Medias Móviles de {ticker}",
        xaxis_title="Fecha",
        yaxis_title="Precio USD",
        template="plotly_white"
    )

    # Añadir RSI si está disponible
    if 'RSI' in data.columns:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['RSI'],
            name='RSI',
            yaxis="y2",
            line=dict(color='red')
        ))

        fig.update_layout(
            yaxis2=dict(
                title="RSI",
                overlaying="y",
                side="right",
                range=[0, 100],
                showgrid=False
            )
        )

        fig.add_hline(y=30, line_dash="dash", line_color="green")
        fig.add_hline(y=70, line_dash="dash", line_color="red")

    return fig