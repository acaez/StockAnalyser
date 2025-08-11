from PortfolioManager.portfolio import DIAMOND
from DataManager.data import get_stock_price

def analyzer():
    
    results = []
    
    for symbol in DIAMOND:
        stock_data = get_stock_price(symbol)
        if stock_data:
            results.append(stock_data)

    return results