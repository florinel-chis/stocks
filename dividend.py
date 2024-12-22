import yfinance as yf

def calculate_shares_for_daily_expense(stock_symbol, daily_expense):
    """
    Calculates the number of shares needed to cover a daily expense with dividends.

    Args:
        stock_symbol (str): The stock symbol (e.g., "AAPL", "MSFT", "MCD").
        daily_expense (float): The daily expense you want to cover (e.g., cost of a coffee).

    Returns:
        dict or None: A dictionary containing relevant information, including shares needed,
                     or None if the data is not available or if there's an error.
    """
    try:
        ticker = yf.Ticker(stock_symbol)
        info = ticker.info

        if 'dividendYield' not in info or info['dividendYield'] is None or 'currentPrice' not in info or info['currentPrice'] is None:
            return None  # No dividend yield or price available, cannot calculate
    
        dividend_yield = info['dividendYield']
        stock_price = info['currentPrice']
        annual_dividend_per_share = stock_price * dividend_yield
        daily_dividend_per_share = annual_dividend_per_share / 365
        shares_needed = daily_expense / daily_dividend_per_share if daily_dividend_per_share > 0 else float('inf') # to prevent ZeroDivisionError

        return {
            "stock_symbol": stock_symbol,
            "stock_price": stock_price,
            "dividend_yield": dividend_yield * 100, #Percentage format
            "annual_dividend_per_share": annual_dividend_per_share,
            "daily_dividend_per_share": daily_dividend_per_share,
            "shares_needed": shares_needed if shares_needed != float('inf') else "Infinite (or zero dividend)", # to prevent infinity showing
            "daily_expense": daily_expense
        }

    except Exception as e:
        print(f"Error fetching data for {stock_symbol}: {e}")
        return None


if __name__ == "__main__":
    stock_symbol = input("Enter the stock symbol: ").upper()
    try:
         daily_expense = float(input("Enter the daily expense you want to cover: "))
    except ValueError:
       print("Invalid input. Please enter a numerical value for daily expense.")
       exit()


    result = calculate_shares_for_daily_expense(stock_symbol, daily_expense)

    if result:
        print(f"\n--- Stock Information for {result['stock_symbol']} ---")
        print(f"Stock Price: ${result['stock_price']:.2f}")
        print(f"Dividend Yield: {result['dividend_yield']:.2f}%")
        print(f"Annual Dividend per Share: ${result['annual_dividend_per_share']:.4f}")
        print(f"Daily Dividend per Share: ${result['daily_dividend_per_share']:.4f}")
        print(f"Daily Expense: ${result['daily_expense']:.2f}")
        if isinstance(result["shares_needed"],str):
              print(f"Shares Needed: {result['shares_needed']}")
        else:
              print(f"Shares Needed: {result['shares_needed']:.2f}")

    else:
        print(f"Could not retrieve data for {stock_symbol}. Please check the ticker symbol or the input data")