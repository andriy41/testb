import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import talib
import logging
from ..data.market_data import MarketData

class TechnicalAnalyzer:
    """
    Performs technical analysis on market data using various indicators
    and techniques to identify trading opportunities.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    async def analyze(self, market_data: MarketData) -> Dict:
        """
        Perform technical analysis on market data.
        
        Args:
            market_data: MarketData object containing OHLCV data
            
        Returns:
            Dict containing various technical indicators and analysis results
        """
        try:
            df = market_data.to_dataframe()
            
            return {
                'trend_indicators': self._calculate_trend_indicators(df),
                'momentum_indicators': self._calculate_momentum_indicators(df),
                'volatility_indicators': self._calculate_volatility_indicators(df),
                'volume_indicators': self._calculate_volume_indicators(df),
                'support_resistance': self._identify_support_resistance(df),
                'patterns': self._identify_patterns(df),
                'fibonacci_levels': self._calculate_fibonacci_levels(df),
                'pivot_points': self._calculate_pivot_points(df)
            }
            
        except Exception as e:
            self.logger.error(f"Technical analysis error: {str(e)}")
            raise
            
    def _calculate_trend_indicators(self, df: pd.DataFrame) -> Dict:
        """Calculate trend indicators"""
        try:
            close = df['close'].values
            high = df['high'].values
            low = df['low'].values
            
            # Moving averages
            sma_20 = talib.SMA(close, timeperiod=20)
            sma_50 = talib.SMA(close, timeperiod=50)
            sma_200 = talib.SMA(close, timeperiod=200)
            
            # MACD
            macd, macd_signal, macd_hist = talib.MACD(
                close,
                fastperiod=12,
                slowperiod=26,
                signalperiod=9
            )
            
            # ADX
            adx = talib.ADX(high, low, close, timeperiod=14)
            
            # Parabolic SAR
            sar = talib.SAR(high, low, acceleration=0.02, maximum=0.2)
            
            return {
                'sma_20': self._get_latest_value(sma_20),
                'sma_50': self._get_latest_value(sma_50),
                'sma_200': self._get_latest_value(sma_200),
                'macd': {
                    'macd': self._get_latest_value(macd),
                    'signal': self._get_latest_value(macd_signal),
                    'histogram': self._get_latest_value(macd_hist)
                },
                'adx': self._get_latest_value(adx),
                'parabolic_sar': self._get_latest_value(sar)
            }
            
        except Exception as e:
            self.logger.error(f"Trend indicators calculation error: {str(e)}")
            return {}
            
    def _calculate_momentum_indicators(self, df: pd.DataFrame) -> Dict:
        """Calculate momentum indicators"""
        try:
            close = df['close'].values
            high = df['high'].values
            low = df['low'].values
            
            # RSI
            rsi = talib.RSI(close, timeperiod=14)
            
            # Stochastic
            slowk, slowd = talib.STOCH(
                high,
                low,
                close,
                fastk_period=5,
                slowk_period=3,
                slowk_matype=0,
                slowd_period=3,
                slowd_matype=0
            )
            
            # CCI
            cci = talib.CCI(high, low, close, timeperiod=14)
            
            # Williams %R
            willr = talib.WILLR(high, low, close, timeperiod=14)
            
            return {
                'rsi': self._get_latest_value(rsi),
                'stochastic': {
                    'k': self._get_latest_value(slowk),
                    'd': self._get_latest_value(slowd)
                },
                'cci': self._get_latest_value(cci),
                'williams_r': self._get_latest_value(willr)
            }
            
        except Exception as e:
            self.logger.error(f"Momentum indicators calculation error: {str(e)}")
            return {}
            
    def _calculate_volatility_indicators(self, df: pd.DataFrame) -> Dict:
        """Calculate volatility indicators"""
        try:
            close = df['close'].values
            high = df['high'].values
            low = df['low'].values
            
            # Bollinger Bands
            upper, middle, lower = talib.BBANDS(
                close,
                timeperiod=20,
                nbdevup=2,
                nbdevdn=2,
                matype=0
            )
            
            # ATR
            atr = talib.ATR(high, low, close, timeperiod=14)
            
            # Standard Deviation
            stddev = talib.STDDEV(close, timeperiod=20, nbdev=1)
            
            return {
                'bollinger_bands': {
                    'upper': self._get_latest_value(upper),
                    'middle': self._get_latest_value(middle),
                    'lower': self._get_latest_value(lower)
                },
                'atr': self._get_latest_value(atr),
                'stddev': self._get_latest_value(stddev)
            }
            
        except Exception as e:
            self.logger.error(f"Volatility indicators calculation error: {str(e)}")
            return {}
            
    def _calculate_volume_indicators(self, df: pd.DataFrame) -> Dict:
        """Calculate volume indicators"""
        try:
            close = df['close'].values
            volume = df['volume'].values
            
            # On Balance Volume
            obv = talib.OBV(close, volume)
            
            # Money Flow Index
            high = df['high'].values
            low = df['low'].values
            mfi = talib.MFI(high, low, close, volume, timeperiod=14)
            
            # Chaikin A/D Line
            ad = talib.AD(high, low, close, volume)
            
            # Volume SMA
            volume_sma = talib.SMA(volume, timeperiod=20)
            
            return {
                'obv': self._get_latest_value(obv),
                'mfi': self._get_latest_value(mfi),
                'chaikin_ad': self._get_latest_value(ad),
                'volume_sma': self._get_latest_value(volume_sma)
            }
            
        except Exception as e:
            self.logger.error(f"Volume indicators calculation error: {str(e)}")
            return {}
            
    def _identify_patterns(self, df: pd.DataFrame) -> Dict:
        """Identify candlestick patterns"""
        try:
            open = df['open'].values
            high = df['high'].values
            low = df['low'].values
            close = df['close'].values
            
            patterns = {}
            
            # Reversal patterns
            patterns['hammer'] = talib.CDLHAMMER(open, high, low, close)
            patterns['engulfing'] = talib.CDLENGULFING(open, high, low, close)
            patterns['morning_star'] = talib.CDLMORNINGSTAR(open, high, low, close)
            patterns['evening_star'] = talib.CDLEVENINGSTAR(open, high, low, close)
            
            # Continuation patterns
            patterns['doji'] = talib.CDLDOJI(open, high, low, close)
            patterns['three_white_soldiers'] = talib.CDL3WHITESOLDIERS(open, high, low, close)
            patterns['three_black_crows'] = talib.CDL3BLACKCROWS(open, high, low, close)
            
            return {
                name: bool(self._get_latest_value(pattern))
                for name, pattern in patterns.items()
            }
            
        except Exception as e:
            self.logger.error(f"Pattern identification error: {str(e)}")
            return {}
            
    def _identify_support_resistance(self, df: pd.DataFrame) -> Dict:
        """Identify support and resistance levels"""
        try:
            # Use pivot points and recent highs/lows
            highs = df['high'].values
            lows = df['low'].values
            
            # Calculate pivot points
            pivot = (highs[-1] + lows[-1] + df['close'].values[-1]) / 3
            r1 = 2 * pivot - lows[-1]
            s1 = 2 * pivot - highs[-1]
            r2 = pivot + (highs[-1] - lows[-1])
            s2 = pivot - (highs[-1] - lows[-1])
            
            return {
                'resistance_levels': [float(r2), float(r1)],
                'support_levels': [float(s1), float(s2)],
                'pivot': float(pivot)
            }
            
        except Exception as e:
            self.logger.error(f"Support/Resistance identification error: {str(e)}")
            return {}
            
    def _calculate_fibonacci_levels(self, df: pd.DataFrame) -> Dict:
        """Calculate Fibonacci retracement levels"""
        try:
            high = df['high'].max()
            low = df['low'].min()
            diff = high - low
            
            return {
                'level_0': float(high),
                'level_236': float(high - 0.236 * diff),
                'level_382': float(high - 0.382 * diff),
                'level_500': float(high - 0.500 * diff),
                'level_618': float(high - 0.618 * diff),
                'level_100': float(low)
            }
            
        except Exception as e:
            self.logger.error(f"Fibonacci levels calculation error: {str(e)}")
            return {}
            
    def _calculate_pivot_points(self, df: pd.DataFrame) -> Dict:
        """Calculate pivot points"""
        try:
            high = df['high'].values[-1]
            low = df['low'].values[-1]
            close = df['close'].values[-1]
            
            pivot = (high + low + close) / 3
            r1 = 2 * pivot - low
            s1 = 2 * pivot - high
            r2 = pivot + (high - low)
            s2 = pivot - (high - low)
            r3 = high + 2 * (pivot - low)
            s3 = low - 2 * (high - pivot)
            
            return {
                'pivot': float(pivot),
                'r1': float(r1),
                'r2': float(r2),
                'r3': float(r3),
                's1': float(s1),
                's2': float(s2),
                's3': float(s3)
            }
            
        except Exception as e:
            self.logger.error(f"Pivot points calculation error: {str(e)}")
            return {}
            
    def _get_latest_value(self, arr: np.ndarray) -> float:
        """Get the latest non-NaN value from an array"""
        if arr is None or len(arr) == 0:
            return None
        
        # Convert to float to handle np.nan
        val = float(arr[-1])
        return None if np.isnan(val) else val
