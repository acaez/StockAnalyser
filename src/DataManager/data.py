import yfinance as yf
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_stock_price(symbol):
    
    print(f"  📡 Récupération de {symbol}...")
    
    try:
        stock = yf.Ticker(symbol)
        
        history = stock.history(period="2d")
        
        if len(history) < 2:
            print(f"    ❌ Pas assez de données pour {symbol}")
            return None

        current_price = history['Close'].iloc[-1]  # Latest price
        previous_price = history['Close'].iloc[-2]  # Previous price

        absolute_variation = current_price - previous_price
        percentage_variation = (absolute_variation / previous_price) * 100
        
        from PortfolioManager.portfolio import DIAMOND
        company_name = DIAMOND.get(symbol, symbol)
        
        result = {
            'symbol': symbol,
            'name': company_name,
            'price': round(current_price, 2),
            'absolute_variation': round(absolute_variation, 2),
            'percentage_variation': round(percentage_variation, 2),
            'time': datetime.now().strftime('%H:%M:%S')
        }
        
        print(f"    ✅ {symbol}: ${result['price']} ({result['percentage_variation']:+.1f}%)")
        return result
        
    except Exception as error:
        print(f"    ❌ Erreur pour {symbol}: {error}")
        return None
