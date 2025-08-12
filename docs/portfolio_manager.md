# Portfolio Manager Documentation

The Portfolio Manager component handles portfolio definition, stock analysis, and performance tracking for the StockAnalyser project.

## Overview

The portfolio manager defines the stocks to track, orchestrates data fetching, and provides analysis capabilities. It serves as the core business logic layer that connects data fetching with portfolio analysis.

## Files

- `portfolio.py` - Portfolio definition and stock mappings
- `analyser.py` - Portfolio analysis and data processing

---

## portfolio.py

### Constants

#### `DIAMOND`

**Purpose:**
Defines the core portfolio of stocks to track, mapping ticker symbols to full company names.

**Type:** `dict[str, str]`

**Current Portfolio:**
- `GOOGL`: Google (Alphabet Inc.)
- `AAPL`: Apple Inc.
- `META`: Meta Platforms (formerly Facebook)
- `AMZN`: Amazon.com Inc.
- `MSFT`: Microsoft Corporation
- `NVDA`: NVIDIA Corporation
- `TSLA`: Tesla Inc.

**Usage:**
- **Symbol Validation**: Ensures only tracked stocks are analyzed
- **Display Names**: Provides user-friendly company names for reports
- **Portfolio Scope**: Defines which stocks are included in analysis
- **Data Mapping**: Links ticker symbols to readable company names

**How to Modify:**
To add or remove stocks from the portfolio:
```python
DIAMOND = {
    'EXISTING': 'Company',
    'NEW_TICKER': 'New Company Name',  # Add new stock
    # Remove unwanted stocks by deleting their entries
}
```

**Integration Points:**
- Used by `data_manager.stock_data.fetch_stock_data()` for company name resolution
- Used by `analyser.analyze_portfolio()` to determine which stocks to fetch
- Can be extended to include additional metadata (sectors, weights, etc.)

---

## analyser.py

### Functions

#### `analyze_portfolio()`

**Purpose:**
Orchestrates the analysis of the entire portfolio by fetching data for all stocks defined in the DIAMOND portfolio and compiling the results.

**Parameters:**
None

**Returns:**
- `list[dict]`: List of stock data dictionaries for successfully fetched stocks
  ```python
  [
      {
          'symbol': str,
          'company_name': str,
          'current_price': float,
          'absolute_change': float,
          'percentage_change': float,
          'timestamp': str
      },
      # ... more stock data
  ]
  ```

**How it works:**
1. **Portfolio Iteration**: Loops through all stocks defined in the DIAMOND portfolio
2. **Data Fetching**: Calls `fetch_stock_data()` for each stock symbol
3. **Result Compilation**: Collects successful data fetches into a results list
4. **Error Resilience**: Continues processing even if individual stocks fail to fetch
5. **Clean Results**: Only includes stocks with valid data in the final results

**Error Handling:**
- Gracefully handles individual stock fetch failures
- Continues processing remaining stocks if one fails
- Returns partial results if some stocks are unavailable
- Maintains portfolio analysis even with network issues

**Performance Characteristics:**
- **Sequential Processing**: Fetches stocks one by one (not parallel)
- **Time Complexity**: O(n) where n is the number of stocks in portfolio
- **Network Dependent**: Performance depends on API response times
- **Memory Efficient**: Minimal memory footprint for results storage

**Console Output:**
During execution, the function provides real-time feedback through the underlying `fetch_stock_data()` calls:
```
📡 Fetching data for AAPL...
   ✅ AAPL: $150.25 (+2.5%)
📡 Fetching data for GOOGL...
   ✅ GOOGL: $125.80 (-1.2%)
```

**Dependencies:**
- `portfolio_manager.portfolio.DIAMOND`: Source of stock symbols to analyze
- `data_manager.stock_data.fetch_stock_data`: Data fetching functionality

**Integration Points:**
- Called by main application to get portfolio analysis
- Results can be passed to display managers for formatting
- Data can be used by technical analysis indicators
- Results suitable for statistical analysis and reporting

**Extensibility:**
The function can be extended to include:
- Parallel processing for faster data fetching
- Portfolio-level statistics (total value, average change, etc.)
- Filtering options (by sector, performance, etc.)
- Caching mechanisms for recent data
- Historical trend analysis

**Best Practices:**
- Call during market hours for most accurate data
- Consider caching results for repeated calls
- Monitor execution time for large portfolios
- Handle empty results gracefully in calling code
- Consider implementing progress indicators for large portfolios
