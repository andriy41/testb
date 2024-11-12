import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta
import logging
import asyncio
from .market_data import MarketData
from .yfinance_fetcher import YFinanceFetcher

class DataManager:
    """
    Manages market data fetching, caching, and processing.
    Coordinates between different data sources and ensures data consistency.
    """
    
    def __init__(self, config: Dict):
        """
        Initialize DataManager with configuration.
        
        Args:
            config: Configuration dictionary containing data settings
        """
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.cache = {}  # symbol -> MarketData mapping
        self.data_fetcher = YFinanceFetcher()
        self.update_interval = timedelta(minutes=1)
        self.last_update = {}  # symbol -> last update time mapping
        
    async def get_market_data(
        self,
        symbol: str,
        interval: str = '1m',
        start: Optional[datetime] = None,
        end: Optional[datetime] = None
    ) -> MarketData:
        """
        Get market data for a symbol. Fetches from cache if available and recent,
        otherwise fetches from data source.
        
        Args:
            symbol: Trading symbol
            interval: Time interval for the data
            start: Start datetime for historical data
            end: End datetime for historical data
            
        Returns:
            MarketData object containing the requested data
        """
        try:
            cache_key = f"{symbol}_{interval}"
            
            # Check if we need to update cached data
            if self._should_update_data(cache_key):
                await self._update_market_data(symbol, interval, start, end)
            
            # Return cached data
            if cache_key in self.cache:
                return self.cache[cache_key]
            
            # If not in cache, fetch new data
            market_data = await self._fetch_market_data(symbol, interval, start, end)
            self.cache[cache_key] = market_data
            self.last_update[cache_key] = datetime.now()
            
            return market_data
            
        except Exception as e:
            self.logger.error(f"Error getting market data for {symbol}: {str(e)}")
            raise
            
    async def get_multiple_symbols(
        self,
        symbols: List[str],
        interval: str = '1m'
    ) -> Dict[str, MarketData]:
        """
        Get market data for multiple symbols concurrently.
        
        Args:
            symbols: List of trading symbols
            interval: Time interval for the data
            
        Returns:
            Dictionary mapping symbols to their MarketData objects
        """
        try:
            tasks = [
                self.get_market_data(symbol, interval)
                for symbol in symbols
            ]
            
            results = await asyncio.gather(*tasks)
            return dict(zip(symbols, results))
            
        except Exception as e:
            self.logger.error(f"Error getting multiple symbols: {str(e)}")
            raise
            
    async def update_market_data(
        self,
        symbol: str,
        new_data: Union[pd.DataFrame, MarketData]
    ):
        """
        Update market data for a symbol.
        
        Args:
            symbol: Trading symbol
            new_data: New market data to update with
        """
        try:
            if isinstance(new_data, pd.DataFrame):
                market_data = MarketData(symbol, interval='1m', data=new_data)
            else:
                market_data = new_data
                
            cache_key = f"{symbol}_{market_data.interval}"
            
            if cache_key in self.cache:
                self.cache[cache_key].update(market_data.to_dataframe())
            else:
                self.cache[cache_key] = market_data
                
            self.last_update[cache_key] = datetime.now()
            
        except Exception as e:
            self.logger.error(f"Error updating market data for {symbol}: {str(e)}")
            raise
            
    def clear_cache(self, symbol: Optional[str] = None):
        """
        Clear cached market data.
        
        Args:
            symbol: Optional symbol to clear specific cache entry
        """
        try:
            if symbol:
                # Clear specific symbol
                keys_to_clear = [k for k in self.cache.keys() if k.startswith(f"{symbol}_")]
                for key in keys_to_clear:
                    del self.cache[key]
                    if key in self.last_update:
                        del self.last_update[key]
            else:
                # Clear all cache
                self.cache.clear()
                self.last_update.clear()
                
        except Exception as e:
            self.logger.error(f"Error clearing cache: {str(e)}")
            raise
            
    def get_cached_symbols(self) -> List[str]:
        """
        Get list of symbols currently in cache.
        
        Returns:
            List of cached symbols
        """
        return list(set(k.split('_')[0] for k in self.cache.keys()))
        
    async def _update_market_data(
        self,
        symbol: str,
        interval: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None
    ):
        """Update market data for a symbol"""
        try:
            market_data = await self._fetch_market_data(symbol, interval, start, end)
            cache_key = f"{symbol}_{interval}"
            
            if cache_key in self.cache:
                self.cache[cache_key].update(market_data.to_dataframe())
            else:
                self.cache[cache_key] = market_data
                
            self.last_update[cache_key] = datetime.now()
            
        except Exception as e:
            self.logger.error(f"Error updating market data for {symbol}: {str(e)}")
            raise
            
    async def _fetch_market_data(
        self,
        symbol: str,
        interval: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None
    ) -> MarketData:
        """Fetch market data from data source"""
        try:
            df = await self.data_fetcher.fetch_data(symbol, interval, start, end)
            return MarketData(symbol, interval, df)
            
        except Exception as e:
            self.logger.error(f"Error fetching market data for {symbol}: {str(e)}")
            raise
            
    def _should_update_data(self, cache_key: str) -> bool:
        """Check if cached data should be updated"""
        if cache_key not in self.last_update:
            return True
            
        time_since_update = datetime.now() - self.last_update[cache_key]
        return time_since_update >= self.update_interval
        
    def validate_data(self, market_data: MarketData) -> bool:
        """
        Validate market data quality and consistency.
        
        Args:
            market_data: MarketData object to validate
            
        Returns:
            True if data is valid, False otherwise
        """
        try:
            if not market_data.is_valid():
                return False
                
            df = market_data.to_dataframe()
            
            # Check for gaps in timestamps
            timestamps = df.index
            expected_diff = pd.Timedelta(market_data.interval)
            actual_diffs = timestamps[1:] - timestamps[:-1]
            if (actual_diffs > expected_diff * 1.5).any():
                return False
                
            # Check for price continuity
            price_jumps = abs(df['close'].pct_change())
            if (price_jumps > self.config.get('max_price_jump', 0.1)).any():
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating market data: {str(e)}")
            return False
