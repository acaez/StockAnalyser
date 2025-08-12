import pandas as pd
import numpy as np

class TechnicalIndicators:
    """
    Advanced technical analysis indicators
    """
    
    def __init__(self, data_handler):
        self.data = data_handler
    
    def rsi(self, symbol: str, period: int = 14, timeframe: str = '1d'):
        """
        Calculate Relative Strength Index (RSI).
        
        Parameters:
        - symbol: Stock symbol (e.g., 'AAPL')
        - period: Number of periods for calculation (default: 14)
        - timeframe: Time interval ('1d', '1h', etc.)
        
        Returns:
        - pandas.Series: RSI values (0-100)
        """
        try:
            prices = self.data.get_price_data(symbol, timeframe)
            
            if 'Close' in prices.columns:
                close_prices = prices['Close']
            elif 'close' in prices.columns:
                close_prices = prices['close']
            else:
                close_prices = prices.iloc[:, 0]
            
            price_changes = close_prices.diff()
            gains = price_changes.where(price_changes > 0, 0)
            losses = -price_changes.where(price_changes < 0, 0)
            
            avg_gain = gains.rolling(window=period).mean()
            avg_loss = losses.rolling(window=period).mean()
            
            for i in range(period, len(gains)):
                avg_gain.iloc[i] = (avg_gain.iloc[i-1] * (period - 1) + gains.iloc[i]) / period
                avg_loss.iloc[i] = (avg_loss.iloc[i-1] * (period - 1) + losses.iloc[i]) / period
            
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            rsi = rsi.fillna(100)
            
            return rsi
            
        except Exception as e:
            print(f"Error calculating RSI for {symbol}: {str(e)}")
            return None
    
    def macd(self, symbol: str, fast: int = 12, slow: int = 26, signal: int = 9, timeframe: str = '1d'):
        """
        Calculate MACD (Moving Average Convergence Divergence).
        
        Parameters:
        - symbol: Stock symbol (e.g., 'AAPL')
        - fast: Fast EMA period (default: 12)
        - slow: Slow EMA period (default: 26)
        - signal: Signal line EMA period (default: 9)
        - timeframe: Time interval ('1d', '1h', etc.)
        
        Returns:
        - dict: {'macd': MACD line, 'signal': Signal line, 'histogram': Histogram}
        """
        try:
            prices = self.data.get_price_data(symbol, timeframe)
            
            if 'Close' in prices.columns:
                close_prices = prices['Close']
            elif 'close' in prices.columns:
                close_prices = prices['close']
            else:
                close_prices = prices.iloc[:, 0]
            
            fast_ema = close_prices.ewm(span=fast).mean()
            slow_ema = close_prices.ewm(span=slow).mean()

            macd_line = fast_ema - slow_ema

            signal_line = macd_line.ewm(span=signal).mean()

            histogram = macd_line - signal_line
            
            return {
                'macd': macd_line,
                'signal': signal_line,
                'histogram': histogram
            }
            
        except Exception as e:
            print(f"Error calculating MACD for {symbol}: {str(e)}")
            return None
    
    def bollinger_bands(self, symbol: str, period: int = 20, std_dev: float = 2, timeframe: str = '1d'):
        """
        Calculate Bollinger Bands.
        
        Parameters:
        - symbol: Stock symbol (e.g., 'AAPL')
        - period: Period for moving average and standard deviation (default: 20)
        - std_dev: Number of standard deviations for bands (default: 2)
        - timeframe: Time interval ('1d', '1h', etc.)
        
        Returns:
        - dict: {'upper': Upper band, 'middle': Middle band, 'lower': Lower band, 
                'bandwidth': Band width, 'percent_b': %B indicator}
        """
        try:
            prices = self.data.get_price_data(symbol, timeframe)
            
            if 'Close' in prices.columns:
                close_prices = prices['Close']
            elif 'close' in prices.columns:
                close_prices = prices['close']
            else:
                close_prices = prices.iloc[:, 0]

            middle_band = close_prices.rolling(window=period).mean()

            rolling_std = close_prices.rolling(window=period).std()

            upper_band = middle_band + (rolling_std * std_dev)
            lower_band = middle_band - (rolling_std * std_dev)

            bandwidth = (upper_band - lower_band) / middle_band * 100

            percent_b = (close_prices - lower_band) / (upper_band - lower_band)
            
            return {
                'upper': upper_band,
                'middle': middle_band,
                'lower': lower_band,
                'bandwidth': bandwidth,
                'percent_b': percent_b
            }
            
        except Exception as e:
            print(f"Error calculating Bollinger Bands for {symbol}: {str(e)}")
            return None
    
    def stochastic_oscillator(self, symbol: str, k_period: int = 14, d_period: int = 3, timeframe: str = '1d'):
        """
        Calculate Stochastic Oscillator.
        
        Parameters:
        - symbol: Stock symbol (e.g., 'AAPL')
        - k_period: Period for %K calculation (default: 14)
        - d_period: Period for %D smoothing (default: 3)
        - timeframe: Time interval ('1d', '1h', etc.)
        
        Returns:
        - dict: {'%K': Fast stochastic line, '%D': Slow stochastic line}
        """
        try:
            prices = self.data.get_price_data(symbol, timeframe)
            
            if 'High' in prices.columns and 'Low' in prices.columns and 'Close' in prices.columns:
                high_prices = prices['High']
                low_prices = prices['Low']
                close_prices = prices['Close']
            elif 'high' in prices.columns and 'low' in prices.columns and 'close' in prices.columns:
                high_prices = prices['high']
                low_prices = prices['low']
                close_prices = prices['close']
            else:
                close_prices = prices.iloc[:, 0]
                high_prices = close_prices
                low_prices = close_prices
            
            lowest_low = low_prices.rolling(window=k_period).min()
            highest_high = high_prices.rolling(window=k_period).max()
            
            k_percent = ((close_prices - lowest_low) / (highest_high - lowest_low)) * 100
            
            d_percent = k_percent.rolling(window=d_period).mean()
            
            k_percent = k_percent.fillna(50)
            d_percent = d_percent.fillna(50)
            
            return {
                '%K': k_percent,
                '%D': d_percent
            }
            
        except Exception as e:
            print(f"Error calculating Stochastic Oscillator for {symbol}: {str(e)}")
            return None
    
    def ema(self, symbol: str, period: int, timeframe: str = '1d'):
        """
        Calculate Exponential Moving Average (EMA).
        
        Parameters:
        - symbol: Stock symbol (e.g., 'AAPL')
        - period: Number of periods for EMA calculation
        - timeframe: Time interval ('1d', '1h', etc.)
        
        Returns:
        - pandas.Series: EMA values
        """
        try:
            prices = self.data.get_price_data(symbol, timeframe)
            
            if 'Close' in prices.columns:
                close_prices = prices['Close']
            elif 'close' in prices.columns:
                close_prices = prices['close']
            else:
                close_prices = prices.iloc[:, 0]

            ema_values = close_prices.ewm(span=period, adjust=False).mean()
            
            return ema_values
            
        except Exception as e:
            print(f"Error calculating EMA for {symbol}: {str(e)}")
            return None
    
    def sma(self, symbol: str, period: int, timeframe: str = '1d'):
        """
        Calculate Simple Moving Average (SMA).
        
        Parameters:
        - symbol: Stock symbol (e.g., 'AAPL')
        - period: Number of periods for SMA calculation
        - timeframe: Time interval ('1d', '1h', etc.)
        
        Returns:
        - pandas.Series: SMA values
        """
        try:
            prices = self.data.get_price_data(symbol, timeframe)
            
            if 'Close' in prices.columns:
                close_prices = prices['Close']
            elif 'close' in prices.columns:
                close_prices = prices['close']
            else:
                close_prices = prices.iloc[:, 0]
            
            sma_values = close_prices.rolling(window=period).mean()
            
            return sma_values
            
        except Exception as e:
            print(f"Error calculating SMA for {symbol}: {str(e)}")
            return None