import yfinance as yf
import matplotlib.pyplot as plt

# List of stock tickers
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']

# Download the market capitalization of these companies
data = yf.Tickers(tickers)
market_caps = {}

for ticker in tickers:
    market_caps[ticker] = data.tickers[ticker].info['marketCap']

# Convert to billions for easier viewing
market_caps = {key: value / 1e9 for key, value in market_caps.items()}

# Labels and sizes for the pie chart
labels = list(market_caps.keys())
sizes = list(market_caps.values())

# Plotting the pie chart
plt.figure(figsize=(7,7))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title('Market Capitalization of Major Tech Companies (in Billions)')
plt.axis('equal')  # Equal aspect ratio ensures that the pie is drawn as a circle.
plt.show()
