import yfinance as yf
import pandas as pd
import ta
import time

def descargar_datos(ticker="BTC-USD", periodo="2y", intentos=3):
    """Descarga datos históricos del activo seleccionado"""
    for i in range(intentos):
        print(f"🔄 Descargando datos de {ticker}... (intento {i+1})")
        try:
            data = yf.download(ticker, period=periodo, auto_adjust=True, progress=False)
            if len(data) == 0:
                raise ValueError("Datos vacíos devueltos por Yahoo Finance")

            data = data[['Close']].dropna()
            data.columns = ['close']
            close_series = data['close'].squeeze()
            return data, close_series

        except Exception as e:
            print(f"⚠️ Error en intento {i+1}: {e}")
            if i < intentos - 1:
                print("⏳ Reintentando en 5 segundos...")
                time.sleep(5)

    print("❌ No se pudo descargar datos después de varios intentos")
    return pd.DataFrame(), pd.Series()

def calcular_indicadores(data, close_series):
    """Calcula RSI, MACD, SMA_20, SMA_50"""
    if data.empty or len(data) < 20:
        print("❌ No hay suficientes datos para calcular indicadores")
        return data

    print("📊 Calculando indicadores técnicos...")
    data['RSI'] = ta.momentum.RSIIndicator(close_series, window=14).rsi()
    data['MACD'] = ta.trend.MACD(close_series).macd()
    data['SMA_20'] = close_series.rolling(window=20).mean()
    data['SMA_50'] = close_series.rolling(window=50).mean()
    data = data.dropna()
    return data