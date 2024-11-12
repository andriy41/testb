import pandas as pd
import numpy as np
import yfinance as yf
from typing import Dict, List, Union, Tuple
from sklearn.preprocessing import StandardScaler
import talib
from datetime import datetime, timedelta
import logging
import warnings
from dataclasses import dataclass
warnings.filterwarnings('ignore')

@dataclass
class MarketRegime:
    trend: str
    volatility: str
    strength: float
    confidence: float

class DataManager:
    def __init__(self, symbols: List[str], timeframes: List[str]):
        self.symbols = symbols
        self.timeframes = timeframes
        self.data_cache = {}
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            filename='data_manager.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def fetch_data(self, symbol: str, timeframe: str, period: str = 'max') -> pd.DataFrame:
        """Fetch market data with error handling and validation"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=timeframe)
            
            if data.empty:
                raise ValueError(f"No data returned for {symbol} on {timeframe} timeframe")
            
            # Data validation
            self._validate_data(data)
            
            # Cache the data
            self.data_cache[f"{symbol}_{timeframe}"] = {
                'data': data,
                'last_update': datetime.now()
            }
            
            return data
            
        except Exception as e:
            logging.error(f"Error fetching data for {symbol}: {str(e)}")
            raise
    
    def _validate_data(self, data: pd.DataFrame):
        """Validate data quality"""
        # Check for missing values
        if data.isnull().sum().sum() > 0:
            logging.warning("Missing values detected in data")
            data.fillna(method='ffill', inplace=True)
        
        # Check for outliers
        for column in ['Open', 'High', 'Low', 'Close']:
            zscore = np.abs(stats.zscore(data[column]))
            outliers = np.where(zscore > 3)[0]
            if len(outliers) > 0:
                logging.warning(f"Outliers detected in {column}")

class FeatureEngine:
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_list = []
        
    def calculate_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate all technical features"""
        df = data.copy()
        
        # Price action features
        self._add_price_features(df)
        
        # Volume features
        self._add_volume_features(df)
        
        # Volatility features
        self._add_volatility_features(df)
        
        # Momentum features
        self._add_momentum_features(df)
        
        # Market regime features
        self._add_regime_features(df)
        
        return df
    
    def _add_price_features(self, df: pd.DataFrame):
        """Add price-based features"""
        # Moving averages
        for period in [5, 10, 20, 50, 200]:
            df[f'ma_{period}'] = df['Close'].rolling(window=period).mean()
            df[f'ma_{period}_slope'] = df[f'ma_{period}'].pct_change(5)
        
        # Price channels
        df['upper_channel'] = df['High'].rolling(20).max()
        df['lower_channel'] = df['Low'].rolling(20).min()
        df['channel_position'] = (df['Close'] - df['lower_channel']) / (df['upper_channel'] - df['lower_channel'])
        
        # Fibonacci levels
        high = df['High'].rolling(20).max()
        low = df['Low'].rolling(20).min()
        diff = high - low
        df['fib_382'] = high - 0.382 * diff
        df['fib_618'] = high - 0.618 * diff
        
        self.feature_list.extend(['channel_position', 'fib_382', 'fib_618'])
    
    def _add_volume_features(self, df: pd.DataFrame):
        """Add volume-based features"""
        # Basic volume features
        df['volume_ma'] = df['Volume'].rolling(20).mean()
        df['volume_ratio'] = df['Volume'] / df['volume_ma']
        
        # Money flow features
        df['money_flow'] = df['Close'] * df['Volume']
        df['money_flow_ma'] = df['money_flow'].rolling(20).mean()
        
        # Volume momentum
        df['volume_momentum'] = df['Volume'].pct_change(5)
        
        # On-balance volume
        df['obv'] = talib.OBV(df['Close'].values, df['Volume'].values)
        
        self.feature_list.extend(['volume_ratio', 'volume_momentum'])
    
    def _add_volatility_features(self, df: pd.DataFrame):
        """Add volatility-based features"""
        # ATR and derivatives
        df['atr'] = talib.ATR(df['High'].values, df['Low'].values, df['Close'].values)
        df['atr_ratio'] = df['atr'] / df['Close']
        
        # Bollinger Bands
        df['bb_upper'], df['bb_middle'], df['bb_lower'] = talib.BBANDS(df['Close'].values)
        df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / df['bb_middle']
        
        # Historical volatility
        df['returns'] = df['Close'].pct_change()
        df['volatility'] = df['returns'].rolling(20).std() * np.sqrt(252)
        
        self.feature_list.extend(['atr_ratio', 'bb_width', 'volatility'])
    
    def _add_momentum_features(self, df: pd.DataFrame):
        """Add momentum-based features"""
        # RSI and derivatives
        df['rsi'] = talib.RSI(df['Close'].values)
        df['rsi_ma'] = df['rsi'].rolling(10).mean()
        
        # MACD
        df['macd'], df['macd_signal'], df['macd_hist'] = talib.MACD(df['Close'].values)
        
        # Rate of change
        df['roc'] = talib.ROC(df['Close'].values)
        
        # ADX
        df['adx'] = talib.ADX(df['High'].values, df['Low'].values, df['Close'].values)
        
        self.feature_list.extend(['rsi', 'macd_hist', 'roc', 'adx'])
    
    def _add_regime_features(self, df: pd.DataFrame):
        """Add market regime features"""
        # Trend strength
        df['trend_strength'] = abs(df['ma_50_slope'])
        
        # Volatility regime
        df['volatility_regime'] = df['volatility'].rolling(100).mean()
        
        # Momentum regime
        df['momentum_regime'] = df['rsi'].rolling(10).mean()
        
        self.feature_list.extend(['trend_strength', 'volatility_regime', 'momentum_regime'])

class MarketRegimeAnalyzer:
    def __init__(self):
        self.lookback_periods = {
            'short': 10,
            'medium': 50,
            'long': 200
        }
    
    def identify_regime(self, data: pd.DataFrame) -> MarketRegime:
        """Identify current market regime"""
        # Trend analysis
        trend = self._analyze_trend(data)
        
        # Volatility analysis
        volatility = self._analyze_volatility(data)
        
        # Calculate regime strength and confidence
        strength = self._calculate_regime_strength(data)
        confidence = self._calculate_regime_confidence(data)
        
        return MarketRegime(
            trend=trend,
            volatility=volatility,
            strength=strength,
            confidence=confidence
        )
    
    def _analyze_trend(self, data: pd.DataFrame) -> str:
        """Analyze market trend"""
        ma_short = data['Close'].rolling(self.lookback_periods['short']).mean()
        ma_medium = data['Close'].rolling(self.lookback_periods['medium']).mean()
        ma_long = data['Close'].rolling(self.lookback_periods['long']).mean()
        
        if ma_short.iloc[-1] > ma_medium.iloc[-1] > ma_long.iloc[-1]:
            return 'BULLISH'
        elif ma_short.iloc[-1] < ma_medium.iloc[-1] < ma_long.iloc[-1]:
            return 'BEARISH'
        else:
            return 'NEUTRAL'
    
    def _analyze_volatility(self, data: pd.DataFrame) -> str:
        """Analyze market volatility"""
        current_vol = data['returns'].rolling(20).std() * np.sqrt(252)
        historical_vol = current_vol.rolling(100).mean()
        
        if current_vol.iloc[-1] > historical_vol.iloc[-1] * 1.5:
            return 'HIGH'
        elif current_vol.iloc[-1] < historical_vol.iloc[-1] * 0.5:
            return 'LOW'
        else:
            return 'NORMAL'