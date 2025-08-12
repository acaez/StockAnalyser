from datetime import datetime
import yfinance as yf
from portfolio_manager.portfolio import DIAMOND
from config import ANALYSE_CONFIG

def fetch_stock_data(symbol: str):
    """
    Fetch real-time stock data and calculate price changes.
    
    Parameters:
    - symbol: Stock ticker symbol (e.g., 'AAPL')
    
    Returns:
    - dict: Stock data with prices, changes, and metadata, or None if failed
    """

    print(f"  📡 Fetching data for {symbol}...")
    try:
        stock = yf.Ticker(symbol)
        history = stock.history(period=ANALYSE_CONFIG['HISTORY_PERIOD'])
        if len(history) < ANALYSE_CONFIG['MIN_REQUIRED_DAYS']:
            print(f"     ❌ Insufficient data for {symbol}")
            return None

        current_price = history['Close'].iloc[-1]
        previous_price = history['Close'].iloc[-2]
        absolute_change = current_price - previous_price
        percentage_change = (absolute_change / previous_price) * 100
        company_name = DIAMOND.get(symbol, symbol)
        stock_data = {
            'symbol': symbol,
            'company_name': company_name,
            'current_price': round(current_price, ANALYSE_CONFIG['PRICE_DECIMAL_PLACES']),
            'absolute_change': round(absolute_change, ANALYSE_CONFIG['PRICE_DECIMAL_PLACES']),
            'percentage_change': round(percentage_change, ANALYSE_CONFIG['PERCENTAGE_DECIMAL_PLACES']),
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }
        print(f"     ✅ {symbol}: ${stock_data['current_price']} ({stock_data['percentage_change']:+.1f}%)")
        return stock_data
    except Exception as error:
        print(f"      ❌ Error fetching {symbol}: {error}")
        return None