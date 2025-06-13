import plotly.graph_objs as go

def generar_grafico(data, ticker):
    """Genera un gráfico interactivo del precio y RSI"""
    fig = go.Figure()

    # Precio Close
    fig.add_trace(go.Scatter(x=data.index, y=data['close'], name='Precio'))

    # Medias Móviles (si están disponibles)
    if 'SMA_20' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], name='SMA 20'))
    if 'SMA_50' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], name='SMA 50'))

    fig.update_layout(title=f"Precio y Medias Móviles de {ticker}")

    # Añadir RSI si está disponible
    if 'RSI' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], name='RSI'))
        fig.update_layout(
            yaxis2=dict(title="RSI", overlaying="y", side="right", range=[0, 100])
        )
        fig.add_hline(y=30, line_dash="dash", line_color="green")
        fig.add_hline(y=70, line_dash="dash", line_color="red")

    return fig