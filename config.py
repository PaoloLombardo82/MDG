# config.py

ACTIVOS_ANALIZAR = {
    "Criptos": ["BTC-USD", "ETH-USD", "XRP-USD"],
    "Acciones": ["AAPL", "TSLA", "NVDA"],
    "Materias Primas": ["GC=F", "CL=F"],
    "ETFs": ["SPY", "QQQ"]
}

ALL_TICKERS = [ticker for sublist in ACTIVOS_ANALIZAR.values() for ticker in sublist]