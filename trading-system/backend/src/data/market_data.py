import pandas as pd
import numpy as np
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import logging

class MarketData:
    """
    Represents market data including OHLCV (Open, High, Low, Close, Volume) data
    and additional market metrics. Provides methods to manipulate and analyze the data.
    """
    
    def __init__(
        self,
        symbol: str,
        interval: str,
        data: Optional[pd.DataFrame] = None
    ):
        """
        Initialize MarketData instance.
        
        Args:
            symbol: Trading symbol/ticker
            interval: Time interval of the data (e.g., '1m', '5m', '1h', '1d')
            data: Optional DataFrame containing market data
        """
        self.logger = logging.getLogger(__name__)
        self.symbol = symbol
        self.interval = interval
        self._data = data if data is not None else pd.DataFrame()
        self._validate_data()
        
    def _validate_data(self):
        """Validate the data structure and content"""
        if not self._data.empty:
            required_columns = ['open', 'high', 'low', 'close', 'volume']
            
            # Convert column names to lowercase
            self._data.columns = self._data.columns.str.lower()
            
            # Check for required columns
            missing_columns = [col for col in required_columns if col not in self._data.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Ensure datetime index
            if not isinstance(self._data.index, pd.DatetimeIndex):
                try:
                    self._data.index = pd.to_datetime(self._data.index)
                except Exception as e:
                    raise ValueError(f"Could not convert index to datetime: {str(e)}")
            
            # Sort by timestamp
            self._data.sort_index(inplace=True)
            
            # Remove duplicates
            self._data = self._data[~self._data.index.duplicated(keep='first')]
            
    def update(self, new_data: pd.DataFrame):
        """
        Update the market data with new data.
        
        Args:
            new_data: DataFrame containing new market data
        """
        try:
            # Convert column names to lowercase
            new_data.columns = new_data.columns.str.lower()
            
            # Merge with existing data
            if self._data.empty:
                self._data = new_data
            else:
                self._data = pd.concat([self._data, new_data])
                self._data = self._data[~self._data.index.duplicated(keep='last')]
                self._data.sort_index(inplace=True)
            
            self._validate_data()
            
        except Exception as e:
            self.logger.error(f"Data update error: {str(e)}")
            raise
            
    def to_dataframe(self) -> pd.DataFrame:
        """
        Get the market data as a pandas DataFrame.
        
        Returns:
            DataFrame containing the market data
        """
        return self._data.copy()
        
    def get_latest_price(self) -> float:
        """
        Get the latest closing price.
        
        Returns:
            Latest closing price
        """
        if self._data.empty:
            raise ValueError("No data available")
        return float(self._data['close'].iloc[-1])
        
    def get_price_range(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Get price data for a specific date range.
        
        Args:
            start: Start datetime
            end: End datetime
            
        Returns:
            DataFrame containing price data for the specified range
        """
        if self._data.empty:
            raise ValueError("No data available")
            
        data = self._data
        
        if start:
            data = data[data.index >= start]
        if end:
            data = data[data.index <= end]
            
        return data
        
    def calculate_returns(self, periods: int = 1) -> pd.Series:
        """
        Calculate price returns over specified periods.
        
        Args:
            periods: Number of periods to calculate returns over
            
        Returns:
            Series containing calculated returns
        """
        if self._data.empty:
            raise ValueError("No data available")
            
        return self._data['close'].pct_change(periods)
        
    def calculate_volatility(self, window: int = 20) -> float:
        """
        Calculate price volatility over specified window.
        
        Args:
            window: Number of periods to calculate volatility over
            
        Returns:
            Calculated volatility
        """
        if self._data.empty:
            raise ValueError("No data available")
            
        returns = self.calculate_returns()
        volatility = returns.rolling(window=window).std()
        return float(volatility.iloc[-1])
        
    def get_volume_profile(self, bins: int = 10) -> Dict[str, List[float]]:
        """
        Calculate volume profile.
        
        Args:
            bins: Number of price bins for volume profile
            
        Returns:
            Dictionary containing price levels and corresponding volumes
        """
        if self._data.empty:
            raise ValueError("No data available")
            
        price_bins = pd.cut(self._data['close'], bins=bins)
        volume_profile = self._data.groupby(price_bins)['volume'].sum()
        
        return {
            'price_levels': [float(x.mid) for x in volume_profile.index],
            'volumes': [float(x) for x in volume_profile.values]
        }
        
    def get_vwap(self) -> pd.Series:
        """
        Calculate Volume Weighted Average Price (VWAP).
        
        Returns:
            Series containing VWAP values
        """
        if self._data.empty:
            raise ValueError("No data available")
            
        typical_price = (self._data['high'] + self._data['low'] + self._data['close']) / 3
        return (typical_price * self._data['volume']).cumsum() / self._data['volume'].cumsum()
        
    def get_market_depth(self, levels: int = 5) -> Dict[str, Dict[float, float]]:
        """
        Get market depth data if available.
        
        Args:
            levels: Number of price levels to include
            
        Returns:
            Dictionary containing bid and ask levels with volumes
        """
        if 'bid_price' not in self._data.columns or 'ask_price' not in self._data.columns:
            raise ValueError("Market depth data not available")
            
        latest = self._data.iloc[-1]
        
        bids = {
            float(latest[f'bid_price_{i}']): float(latest[f'bid_volume_{i}'])
            for i in range(levels)
            if f'bid_price_{i}' in latest.index and f'bid_volume_{i}' in latest.index
        }
        
        asks = {
            float(latest[f'ask_price_{i}']): float(latest[f'ask_volume_{i}'])
            for i in range(levels)
            if f'ask_price_{i}' in latest.index and f'ask_volume_{i}' in latest.index
        }
        
        return {'bids': bids, 'asks': asks}
        
    def is_valid(self) -> bool:
        """
        Check if the market data is valid.
        
        Returns:
            True if data is valid, False otherwise
        """
        if self._data.empty:
            return False
            
        # Check for required columns
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in self._data.columns for col in required_columns):
            return False
            
        # Check for missing values
        if self._data[required_columns].isnull().any().any():
            return False
            
        # Check for negative prices or volumes
        if (self._data[required_columns] < 0).any().any():
            return False
            
        # Check for high/low consistency
        if (self._data['high'] < self._data['low']).any():
            return False
            
        return True
        
    def __len__(self) -> int:
        """Get the number of data points"""
        return len(self._data)
        
    def __str__(self) -> str:
        """Get string representation"""
        return (
            f"MarketData(symbol={self.symbol}, interval={self.interval}, "
            f"points={len(self)}, start={self._data.index[0]}, end={self._data.index[-1]})"
        )
