# Data Manager Documentation

The Data Manager component is responsible for fetching, processing, and managing stock market data for the StockAnalyser project.

## Overview

The data manager provides a clean interface for retrieving real-time stock data using the Yahoo Finance API. It handles data validation, error management, and formatting to ensure consistent data throughout the application.

## Files

- `stock_data.py` - Core data fetching functionality

---

## stock_data.py

### Functions

#### `fetch_stock_data(symbol: str)`

**Purpose:**
Fetches real-time stock data for a given symbol and calculates key metrics including current price, price changes, and percentage changes.

**Parameters:**
- `symbol` (str): Stock ticker symbol (e.g., 'AAPL', 'GOOGL')

**Returns:**
- `dict` or `None`: Stock data dictionary with the following structure:
  ```python
  {
      'symbol': str,           # Stock ticker symbol
      'company_name': str,     # Full company name
      'current_price': float,  # Current stock price
      'absolute_change': float, # Price change from previous day
      'percentage_change': float, # Percentage change from previous day
      'timestamp': str         # Time when data was fetched (HH:MM:SS)
  }
  ```
  Returns `None` if data fetching fails or insufficient data is available.

**How it works:**
1. **Data Retrieval**: Uses Yahoo Finance API (yfinance) to get historical stock data
2. **Data Validation**: Checks if sufficient historical data is available (minimum 2 days)
3. **Calculations**: Computes current price, absolute change, and percentage change
4. **Company Name Resolution**: Maps ticker symbols to full company names using the DIAMOND portfolio
5. **Formatting**: Rounds prices and percentages according to configuration settings
6. **Error Handling**: Catches and reports any errors during the fetching process

**Dependencies:**
- `yfinance`: For fetching stock data from Yahoo Finance
- `datetime`: For timestamp generation
- `portfolio_manager.portfolio.DIAMOND`: Company name mapping
- `config.ANALYSE_CONFIG`: Configuration settings

**Configuration Used:**
- `HISTORY_PERIOD`: Time period for historical data (default: '2d')
- `MIN_REQUIRED_DAYS`: Minimum days of data required (default: 2)
- `PRICE_DECIMAL_PLACES`: Decimal places for price formatting (default: 2)
- `PERCENTAGE_DECIMAL_PLACES`: Decimal places for percentage formatting (default: 2)

**Error Handling:**
- Network connectivity issues
- Invalid stock symbols
- Insufficient historical data
- API rate limiting
- Data parsing errors

**Output Format:**
The function provides real-time console feedback:
- `📡 Fetching data for SYMBOL...` - Start of data fetch
- `✅ SYMBOL: $PRICE (+X.X%)` - Successful fetch with key metrics
- `❌ Insufficient data for SYMBOL` - Not enough historical data
- `❌ Error fetching SYMBOL: error_message` - Fetch failure with reason

**Performance Considerations:**
- API calls are synchronous and may take 1-3 seconds per symbol
- Yahoo Finance has rate limiting - avoid excessive requests
- Historical data is fetched but only recent prices are used
- Consider implementing caching for frequently accessed symbols

**Integration Points:**
- Used by `portfolio_manager.analyser.analyze_portfolio()`
- Relies on `portfolio_manager.portfolio.DIAMOND` for company names
- Uses `config.ANALYSE_CONFIG` for formatting and validation settings

**Best Practices:**
- Always check return value for `None` before using data
- Handle network timeouts gracefully
- Consider implementing retry logic for failed requests
- Monitor API usage to avoid rate limiting
- Validate input symbols before making API calls
