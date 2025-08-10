import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PortfolioManager.portfolio import DIAMOND
from DataManager.data import get_stock_price

def portfolio_analyzer():
    
    results = []
    
    for symbol in DIAMOND:
        stock_data = get_stock_price(symbol)
        if stock_data:
            results.append(stock_data)

    return results