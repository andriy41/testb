import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, Optional
from datetime import datetime, timedelta
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor

class YFinanceFetcher:
    """
    Fetches market data from Yahoo Finance using the yfinance library.
    Handles rate limiting, error handling, and data validation.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.rate_limit = 2000  # requests per hour
        self.request_count = 0
        self.last_reset = datetime.now()
        self.executor = ThreadPoolExecutor(max_workers=5)
        
    async def fetch_data(
        self,
        symbol: str,
        interval: str = '1m',
        start: Optional[datetime] = None,
        end: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Fetch market data for a symbol.
        
        Args:
            symbol: Trading symbol
            interval: Time interval for the data
            start: Start datetime for historical data
            end: End datetime for historical data
            
        Returns:
            DataFrame containing the fetched market data
        """
        try:
            # Check rate limit
            await self._check_rate_limit()
            
            # Determine period based on interval if start/end not provided
            if not start and not end:
                period = self._get_default_period(interval)
            else:
                period = None
                
            # Fetch data using ThreadPoolExecutor since yfinance is synchronous
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(
                self.executor,
                self._fetch_yfinance_data,
                symbol,
                interval,
                period,
                start,
                end
            )
            
            # Validate and clean data
            df = self._validate_and_clean_data(df)
            
            self.request_count += 1
            return df
            
        except Exception as e:
            self.logger.error(f"Error fetching data for {symbol}: {str(e)}")
            raise
            
    async def fetch_multiple(
        self,
        symbols: list,
        interval: str = '1m',
        start: Optional[datetime] = None,
        end: Optional[datetime] = None
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch market data for multiple symbols concurrently.
        
        Args:
            symbols: List of trading symbols
            interval: Time interval for the data
            start: Start datetime for historical data
            end: End datetime for historical data
            
        Returns:
            Dictionary mapping symbols to their respective DataFrames
        """
        try:
            tasks = [
                self.fetch_data(symbol, interval, start, end)
                for symbol in symbols
            ]
            
            results = await asyncio.gather(*tasks)
            return dict(zip(symbols, results))
            
        except Exception as e:
            self.logger.error(f"Error fetching multiple symbols: {str(e)}")
            raise
            
    def _fetch_yfinance_data(
        self,
        symbol: str,
        interval: str,
        period: Optional[str],
        start: Optional[datetime],
        end: Optional[datetime]
    ) -> pd.DataFrame:
        """Fetch data from yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            
            if period:
                df = ticker.history(period=period, interval=interval)
            else:
                df = ticker.history(
                    interval=interval,
                    start=start,
                    end=end or datetime.now()
                )
                
            return df
            
        except Exception as e:
            self.logger.error(f"YFinance fetch error for {symbol}: {str(e)}")
            raise
            
    def _validate_and_clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate and clean the fetched data"""
        try:
            if df.empty:
                raise ValueError("Empty dataset received")
                
            # Convert column names to lowercase
            df.columns = df.columns.str.lower()
            
            # Check for required columns
            required_columns = ['open', 'high', 'low', 'close', 'volume']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
                
            # Remove rows with missing values
            df = df.dropna(subset=required_columns)
            
            # Ensure datetime index
            if not isinstance(df.index, pd.DatetimeIndex):
                df.index = pd.to_datetime(df.index)
                
            # Sort by timestamp
            df = df.sort_index()
            
            # Remove duplicates
            df = df[~df.index.duplicated(keep='first')]
            
            # Validate price and volume data
            if (df[['open', 'high', 'low', 'close']] <= 0).any().any():
                raise ValueError("Invalid price data (negative or zero prices)")
                
            if (df['volume'] < 0).any():
                raise ValueError("Invalid volume data (negative volumes)")
                
            if (df['high'] < df['low']).any():
                raise ValueError("Invalid price data (high < low)")
                
            return df
            
        except Exception as e:
            self.logger.error(f"Data validation error: {str(e)}")
            raise
            
    async def _check_rate_limit(self):
        """Check and handle rate limiting"""
        try:
            current_time = datetime.now()
            
            # Reset counter if an hour has passed
            if current_time - self.last_reset > timedelta(hours=1):
                self.request_count = 0
                self.last_reset = current_time
                
            # Check if we've hit the rate limit
            if self.request_count >= self.rate_limit:
                wait_time = timedelta(hours=1) - (current_time - self.last_reset)
                self.logger.warning(f"Rate limit reached. Waiting {wait_time.seconds} seconds")
                await asyncio.sleep(wait_time.seconds)
                self.request_count = 0
                self.last_reset = datetime.now()
                
        except Exception as e:
            self.logger.error(f"Rate limit check error: {str(e)}")
            raise
            
    def _get_default_period(self, interval: str) -> str:
        """Get default period based on interval"""
        interval_periods = {
            '1m': '7d',
            '2m': '7d',
            '5m': '7d',
            '15m': '7d',
            '30m': '7d',
            '60m': '30d',
            '90m': '30d',
            '1h': '30d',
            '1d': '1y',
            '5d': '2y',
            '1wk': '5y',
            '1mo': 'max',
            '3mo': 'max'
        }
        
        return interval_periods.get(interval, '7d')
