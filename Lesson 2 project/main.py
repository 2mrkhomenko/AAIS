import yfinance as yf


# Download recent Microsoft stock data.
stock = yf.Ticker("MSFT")
history = stock.history(period="1mo")

print("Recent Microsoft stock prices:")
print(history[["Open", "High", "Low", "Close", "Volume"]].tail())

# Example: calculate the average closing price.
if not history.empty:
	average_close = history["Close"].mean()
	print(f"\nAverage closing price over this period: ${average_close:.2f}")
else:
	print("No data was returned. Check your internet connection or ticker symbol.")
