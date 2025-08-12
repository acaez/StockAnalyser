# Configuration Documentation

The configuration system provides centralized settings management for the StockAnalyser project, ensuring consistent behavior across all components.

## Overview

The configuration module contains all application settings, default values, and parameters that control the behavior of data fetching, analysis, and display components. This centralized approach makes the application easy to customize and maintain.

## Files

- `config.py` - Main configuration settings

---

## config.py

### Configuration Objects

#### `ANALYSE_CONFIG`

**Purpose:**
Contains core settings that control data fetching, validation, and formatting throughout the application.

**Type:** `dict[str, any]`

**Settings:**

##### `HISTORY_PERIOD`
- **Type:** `str`
- **Default:** `'2d'`
- **Purpose:** Specifies how much historical data to fetch from Yahoo Finance
- **Valid Values:** 
  - `'1d'` - 1 day
  - `'2d'` - 2 days
  - `'5d'` - 5 days
  - `'1mo'` - 1 month
  - `'3mo'` - 3 months
  - `'6mo'` - 6 months
  - `'1y'` - 1 year
  - `'2y'` - 2 years
  - `'5y'` - 5 years
  - `'10y'` - 10 years
  - `'ytd'` - Year to date
  - `'max'` - Maximum available data
- **Usage:** Used by `fetch_stock_data()` to determine how much historical data to retrieve
- **Impact:** Affects API response time and data accuracy for change calculations

##### `MIN_REQUIRED_DAYS`
- **Type:** `int`
- **Default:** `2`
- **Purpose:** Minimum number of days of historical data required for valid analysis
- **Validation:** Must be ≤ days covered by `HISTORY_PERIOD`
- **Usage:** Used by `fetch_stock_data()` to validate data sufficiency
- **Impact:** Stocks with insufficient data are rejected from analysis
- **Rationale:** Need at least 2 days to calculate daily change (current vs previous)

##### `PRICE_DECIMAL_PLACES`
- **Type:** `int`
- **Default:** `2`
- **Purpose:** Number of decimal places for price formatting
- **Range:** Typically 0-4 for stock prices
- **Usage:** Used in `fetch_stock_data()` for rounding current prices and absolute changes
- **Impact:** Controls precision of price display and calculations
- **Examples:**
  - `0`: $150 (whole dollars)
  - `2`: $150.25 (cents precision)
  - `4`: $150.2547 (sub-cent precision)

##### `PERCENTAGE_DECIMAL_PLACES`
- **Type:** `int`
- **Default:** `2`
- **Purpose:** Number of decimal places for percentage formatting
- **Range:** Typically 1-3 for percentage changes
- **Usage:** Used in `fetch_stock_data()` for rounding percentage changes
- **Impact:** Controls precision of percentage change display
- **Examples:**
  - `1`: +2.5%
  - `2`: +2.53%
  - `3`: +2.534%

## Configuration Usage

### Accessing Configuration
```python
from config import ANALYSE_CONFIG

# Get specific settings
period = ANALYSE_CONFIG['HISTORY_PERIOD']
precision = ANALYSE_CONFIG['PRICE_DECIMAL_PLACES']
```

### Modifying Configuration
```python
# Temporary modification (runtime only)
ANALYSE_CONFIG['HISTORY_PERIOD'] = '5d'

# Permanent modification (edit config.py)
ANALYSE_CONFIG = {
    'HISTORY_PERIOD': '1mo',  # Changed from '2d'
    'MIN_REQUIRED_DAYS': 5,   # Changed from 2
    # ... other settings
}
```

## Configuration Best Practices

### 1. **Centralization**
- Keep all configuration in one place
- Avoid hardcoded values in business logic
- Import configuration where needed

### 4. **Environment-Specific**
Consider extending to support different environments:
```python
import os

ENV = os.getenv('ENVIRONMENT', 'development')

if ENV == 'production':
    ANALYSE_CONFIG['HISTORY_PERIOD'] = '1d'  # Faster for production
elif ENV == 'development':
    ANALYSE_CONFIG['HISTORY_PERIOD'] = '5d'  # More data for testing
```

## Impact on Components

### Data Manager
- `HISTORY_PERIOD`: Determines API call parameters
- `MIN_REQUIRED_DAYS`: Controls data validation
- `PRICE_DECIMAL_PLACES`: Affects price formatting
- `PERCENTAGE_DECIMAL_PLACES`: Affects percentage formatting

## Common Configuration Scenarios

### High-Frequency Trading
```python
ANALYSE_CONFIG = {
    'HISTORY_PERIOD': '1d',
    'MIN_REQUIRED_DAYS': 1,
    'PRICE_DECIMAL_PLACES': 4,  # Higher precision
    'PERCENTAGE_DECIMAL_PLACES': 3,
}
```

### Long-Term Analysis
```python
ANALYSE_CONFIG = {
    'HISTORY_PERIOD': '1y',
    'MIN_REQUIRED_DAYS': 30,
    'PRICE_DECIMAL_PLACES': 2,
    'PERCENTAGE_DECIMAL_PLACES': 2,
}
```

### Development/Testing
```python
ANALYSE_CONFIG = {
    'HISTORY_PERIOD': '5d',
    'MIN_REQUIRED_DAYS': 2,
    'PRICE_DECIMAL_PLACES': 2,
    'PERCENTAGE_DECIMAL_PLACES': 1,  # Simplified for testing
}
```

## Future Configuration Extensions

The configuration system can be extended to include:

### API Settings
```python
API_CONFIG = {
    'YAHOO_FINANCE_TIMEOUT': 10,
    'MAX_RETRIES': 3,
    'RATE_LIMIT_DELAY': 1,
}
```

### Display Settings
```python
DISPLAY_CONFIG = {
    'CURRENCY_SYMBOL': '$',
    'DATE_FORMAT': '%Y-%m-%d',
    'TIME_FORMAT': '%H:%M:%S',
    'CONSOLE_WIDTH': 80,
}
```

### Portfolio Settings
```python
PORTFOLIO_CONFIG = {
    'DEFAULT_PORTFOLIO': 'DIAMOND',
    'ENABLE_SECTORS': True,
    'ENABLE_WEIGHTS': False,
}
```
