# Technical Indicators Documentation

This document provides detailed explanations of all technical indicators implemented in the StockAnalyser project.

## Table of Contents
1. [RSI (Relative Strength Index)](#rsi-relative-strength-index)
2. [MACD (Moving Average Convergence Divergence)](#macd-moving-average-convergence-divergence)
3. [Bollinger Bands](#bollinger-bands)
4. [Stochastic Oscillator](#stochastic-oscillator)
5. [EMA (Exponential Moving Average)](#ema-exponential-moving-average)
6. [SMA (Simple Moving Average)](#sma-simple-moving-average)

---

## RSI (Relative Strength Index)

### What is RSI?
The Relative Strength Index (RSI) is a momentum oscillator that measures the speed and change of price movements. It oscillates between 0 and 100 and is primarily used to identify overbought and oversold conditions in a trading instrument.

### How is RSI used?
- **Values above 70**: Generally considered overbought (potential sell signal)
- **Values below 30**: Generally considered oversold (potential buy signal)
- **Values around 50**: Neutral momentum
- **Divergences**: When price moves in opposite direction to RSI, it can signal potential reversals
- **Center line (50)**: Acts as support/resistance for trend confirmation

### How the calculation works:
1. Calculate price changes between consecutive periods
2. Separate gains (positive changes) and losses (negative changes)
3. Calculate average gains and losses over the specified period using Wilder's smoothing
4. Calculate Relative Strength (RS) = Average Gain / Average Loss
5. Calculate RSI = 100 - (100 / (1 + RS))

### Parameters:
- `symbol`: Stock symbol (e.g., 'AAPL')
- `period`: Number of periods for calculation (default: 14)
- `timeframe`: Time interval ('1d', '1h', etc.)

### Returns:
- `pandas.Series`: RSI values between 0 and 100

---

## MACD (Moving Average Convergence Divergence)

### What is MACD?
MACD is a trend-following momentum indicator that shows the relationship between two moving averages of a security's price. It consists of three components:
1. **MACD Line**: Fast EMA - Slow EMA (typically 12-period EMA minus 26-period EMA)
2. **Signal Line**: EMA of the MACD line (typically 9-period EMA)
3. **Histogram**: MACD Line - Signal Line

### How is MACD used?
- **Signal Line Crossovers**: When MACD crosses above signal line = bullish signal, below = bearish signal
- **Zero Line Crossovers**: MACD above zero = upward momentum, below zero = downward momentum
- **Divergences**: When price and MACD move in opposite directions, indicating potential reversal
- **Histogram**: Shows the distance between MACD and signal line - helps identify momentum changes

### How the calculation works:
1. Calculate fast EMA (typically 12 periods)
2. Calculate slow EMA (typically 26 periods)
3. MACD line = Fast EMA - Slow EMA
4. Signal line = EMA of MACD line (typically 9 periods)
5. Histogram = MACD line - Signal line

### Parameters:
- `symbol`: Stock symbol (e.g., 'AAPL')
- `fast`: Fast EMA period (default: 12)
- `slow`: Slow EMA period (default: 26)
- `signal`: Signal line EMA period (default: 9)
- `timeframe`: Time interval ('1d', '1h', etc.)

### Returns:
- `dict`: {'macd': MACD line, 'signal': Signal line, 'histogram': Histogram}

---

## Bollinger Bands

### What are Bollinger Bands?
Bollinger Bands are a volatility indicator consisting of three lines:
1. **Middle Band**: Simple Moving Average (typically 20 periods)
2. **Upper Band**: Middle Band + (Standard Deviation × multiplier, typically 2)
3. **Lower Band**: Middle Band - (Standard Deviation × multiplier, typically 2)

### How are Bollinger Bands used?
- **Squeeze**: When bands contract, it indicates low volatility and potential breakout
- **Expansion**: When bands widen, it indicates high volatility
- **Price touching bands**: Upper band can act as resistance, lower band as support
- **Bollinger Band Walk**: Price consistently touching one band indicates strong trend
- **Mean Reversion**: Prices tend to return to the middle band (moving average)
- **%B Indicator**: Shows where price is relative to the bands (0 = lower band, 1 = upper band)

### How the calculation works:
1. Calculate the Simple Moving Average (SMA) for the specified period
2. Calculate the standard deviation of prices over the same period
3. Upper Band = SMA + (Standard Deviation × multiplier)
4. Lower Band = SMA - (Standard Deviation × multiplier)
5. Bandwidth = (Upper Band - Lower Band) / Middle Band × 100
6. %B = (Price - Lower Band) / (Upper Band - Lower Band)

### Parameters:
- `symbol`: Stock symbol (e.g., 'AAPL')
- `period`: Period for moving average and standard deviation (default: 20)
- `std_dev`: Number of standard deviations for bands (default: 2)
- `timeframe`: Time interval ('1d', '1h', etc.)

### Returns:
- `dict`: {'upper': Upper band, 'middle': Middle band (SMA), 'lower': Lower band, 'bandwidth': Band width, 'percent_b': %B indicator}

---

## Stochastic Oscillator

### What is the Stochastic Oscillator?
The Stochastic Oscillator is a momentum indicator that compares a security's closing price to its price range over a given time period. It consists of two lines:
1. **%K Line**: The main stochastic line (fast stochastic)
2. **%D Line**: A moving average of %K (slow stochastic, signal line)

### How is the Stochastic Oscillator used?
- **Overbought/Oversold**: Values above 80 indicate overbought conditions, below 20 indicate oversold
- **Signal Line Crossovers**: %K crossing above %D = bullish signal, below = bearish signal
- **Divergences**: When price and stochastic move in opposite directions
- **Range**: Oscillates between 0 and 100, making it easy to identify extreme levels

### How the calculation works:
1. **%K Calculation**: %K = ((Current Close - Lowest Low) / (Highest High - Lowest Low)) × 100
2. **%D Calculation**: %D = Moving average of %K over D periods
3. The "Lowest Low" and "Highest High" are calculated over the K period
4. Results in values between 0-100 showing where current price sits in recent range

### Parameters:
- `symbol`: Stock symbol (e.g., 'AAPL')
- `k_period`: Period for %K calculation (default: 14)
- `d_period`: Period for %D smoothing (default: 3)
- `timeframe`: Time interval ('1d', '1h', etc.)

### Returns:
- `dict`: {'%K': Fast stochastic line, '%D': Slow stochastic line (signal)}

---

## EMA (Exponential Moving Average)

### What is EMA?
The Exponential Moving Average is a type of moving average that gives more weight to recent prices, making it more responsive to new information compared to a Simple Moving Average (SMA). It reacts more quickly to recent price changes.

### How is EMA used?
- **Trend Direction**: Price above EMA = uptrend, below EMA = downtrend
- **Support/Resistance**: EMA can act as dynamic support in uptrends, resistance in downtrends
- **Crossover Signals**: Price crossing above/below EMA generates buy/sell signals
- **Multiple EMA Strategy**: Using multiple EMAs (e.g., 12, 26, 50) for trend confirmation
- **Entry/Exit Points**: Traders use EMA bounces or breaks for timing trades

### How the calculation works:
1. **Smoothing Factor**: α = 2 / (period + 1)
2. **Initial EMA**: Usually starts with SMA for the first period
3. **Subsequent EMAs**: EMA(today) = (Price(today) × α) + (EMA(yesterday) × (1 - α))
4. **Weight Distribution**: Recent prices have exponentially decreasing weights
5. **Responsiveness**: Shorter periods = more responsive, longer periods = smoother

### Parameters:
- `symbol`: Stock symbol (e.g., 'AAPL')
- `period`: Number of periods for EMA calculation
- `timeframe`: Time interval ('1d', '1h', etc.)

### Returns:
- `pandas.Series`: EMA values

---

## SMA (Simple Moving Average)

### What is SMA?
The Simple Moving Average calculates the average price over a specified number of periods, giving equal weight to all prices in the calculation period. It's smoother than EMA but less responsive to recent changes.

### How is SMA used?
- **Trend Direction**: Price above SMA = bullish trend, below SMA = bearish trend
- **Support/Resistance**: SMA can act as dynamic support/resistance levels
- **Crossover Strategies**: Multiple SMA crossovers for trend confirmation
- **Trend Strength**: Slope and direction of SMA indicates trend strength
- **Baseline**: Often used as a baseline for other indicators

### How the calculation works:
1. Sum all closing prices over the specified period
2. Divide by the number of periods
3. As new prices come in, drop the oldest price and add the newest
4. Recalculate the average

### Parameters:
- `symbol`: Stock symbol (e.g., 'AAPL')
- `period`: Number of periods for SMA calculation
- `timeframe`: Time interval ('1d', '1h', etc.)

### Returns:
- `pandas.Series`: SMA values

---

## Notes for Developers

- All functions include robust error handling
- Functions work with different data formats (Close/close columns)
- Parameters use industry-standard defaults
- Returns are pandas Series or dictionaries for easy manipulation
- All calculations follow standard financial formulas
