from datetime import datetime
import yfinance as yf
from PortfolioManager.portfolio import DIAMOND

def get_stock_price(symbol):

    print(f"  📡 Collecting data for {symbol}...")

    try:
        stock = yf.Ticker(symbol)
        
        history = stock.history(period="2d")
        
        if len(history) < 2:
            print(f"     ❌ Pas assez de données pour {symbol}")
            return None

        current_price = history['Close'].iloc[-1]
        previous_price = history['Close'].iloc[-2]

        absolute_variation = current_price - previous_price
        percentage_variation = (absolute_variation / previous_price) * 100
        
        company_name = DIAMOND.get(symbol, symbol)
        
        result = {
            'symbol': symbol,
            'name': company_name,
            'price': round(current_price, 2),
            'absolute_variation': round(absolute_variation, 2),
            'percentage_variation': round(percentage_variation, 2),
            'time': datetime.now().strftime('%H:%M:%S')
        }
        
        print(f"     ✅ {symbol}: ${result['price']} ({result['percentage_variation']:+.1f}%)")
        return result
        
    except Exception as error:
        print(f"      ❌ Erreur pour {symbol}: {error}")
        return None
