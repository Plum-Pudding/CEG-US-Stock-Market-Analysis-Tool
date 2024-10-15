import yfinance as yf
import pandas as pd

# list the selected 20 tickers
tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN', 'NVDA', 'AMD', 'INTC', 'META', 'JPM', 'V', 'JNJ', 'PG', 'KO', 'PFE', 'XOM', 'DIS', 'PEP', 'T', 'NFLX']

# download historical data for each ticker and save to CSV
for ticker in tickers:
    stock = yf.Ticker(ticker)
    history = stock.history(period = '10y') # fetching 10 years of historical data
    history.to_csv(f'{ticker}_10y_history.csv') # save to CSV file
    