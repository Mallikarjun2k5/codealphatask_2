import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def get_stock_price(ticker):
    """Fetches the latest stock price using yfinance."""
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")['Close'].iloc[-1]
        return price
    except Exception as e:
        print(f"Error fetching price for {ticker}: {e}")
        return None

def portfolio_tracker():
    """Main function to manage and display stock portfolio."""
    portfolio = {}
    
    # Input stocks and shares
    print("Enter your stocks (type 'done' to finish):")
    while True:
        ticker = input("Enter stock ticker (e.g., AAPL) or 'done': ").upper()
        if ticker == 'DONE':
            break
        shares = input(f"Enter number of shares for {ticker}: ")
        try:
            shares = float(shares)
            if shares <= 0:
                print("Shares must be positive.")
                continue
            portfolio[ticker] = {'shares': shares}
        except ValueError:
            print("Invalid input. Please enter a valid number of shares.")
    
    if not portfolio:
        print("Portfolio is empty!")
        return
    
    # Fetch prices and calculate values
    total_value = 0
    data = {'Stock': [], 'Quantity': [], 'Price': [], 'Value': [], 'Allocation (%)': []}
    
    for ticker in portfolio:
        price = get_stock_price(ticker)
        if price is not None:
            portfolio[ticker]['price'] = price
            value = price * portfolio[ticker]['shares']
            portfolio[ticker]['value'] = value
            total_value += value
            data['Stock'].append(ticker)
            data['Quantity'].append(portfolio[ticker]['shares'])
            data['Price'].append(round(price, 2))
            data['Value'].append(round(value, 2))
    
    # Calculate allocation percentages
    for value in data['Value']:
        allocation = (value / total_value) * 100 if total_value > 0 else 0
        data['Allocation (%)'].append(round(allocation, 2))
    
    # Create DataFrame for summary
    df = pd.DataFrame(data)
    print("\nPortfolio Summary:")
    print(df)
    print(f"\nTotal Portfolio Value: ${total_value:.2f}")
    
    # Plot pie chart for allocation
    if total_value > 0:
        plt.figure(figsize=(8, 8))
        plt.pie(data['Allocation (%)'], labels=data['Stock'], autopct='%1.1f%%')
        plt.title('Portfolio Allocation')
        plt.show()

# Run the portfolio tracker
print("Welcome to Stock Portfolio Tracker!")
portfolio_tracker()
