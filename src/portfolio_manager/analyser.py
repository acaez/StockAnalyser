from portfolio_manager.portfolio import DIAMOND
from data_manager.stock_data import fetch_stock_data

def analyze_portfolio():
    
    analysis_results = []
    
    for symbol in DIAMOND:
        stock_data = fetch_stock_data(symbol)
        if stock_data:
            analysis_results.append(stock_data)
    
    return analysis_results