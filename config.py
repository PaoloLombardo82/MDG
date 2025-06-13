# config.py

ACTIVOS_ANALIZAR = {
    "Criptos": ["BTC-USD", "ETH-USD", "XRP-USD", "ADA-USD"],
    "Acciones": ["AAPL", "TSLA", "NVDA", "MSFT"],
    "Materias Primas": ["GC=F", "CL=F", "SI=F", "NG=F"],
    "ETFs": ["SPY", "QQQ", "VTI", "VOO"]
}

# Para uso local
ALL_TICKERS = [ticker for sublist in ACTIVOS_ANALIZAR.values() for ticker in sublist]