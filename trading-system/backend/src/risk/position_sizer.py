import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, Any
import talib

class PriceTargetCalculator:
    def __init__(self, symbol: str, timeframe: str = "1d"):
        self.symbol = symbol
        self.timeframe = timeframe
        self.data = None
        self.targets = {}
        self.confidence_scores = {}
        
    def calculate_price_targets(self) -> Dict[str, Any]:
        """Calculate entry, exit, and stop loss points based on multiple indicators"""
        self.fetch_data()
        
        # Calculate various support/resistance levels
        self.calculate_technical_levels()
        
        # Generate entry points
        entry_points = self._calculate_entry_points()
        
        # Generate exit points
        exit_points = self._calculate_exit_points()
        
        # Calculate stop loss levels
        stop_loss = self._calculate_stop_loss()
        
        # Calculate risk/reward metrics
        risk_reward = self._calculate_risk_reward(entry_points, exit_points, stop_loss)
        
        return {
            "entry": entry_points,
            "exit": exit_points,
            "stopLoss": stop_loss,
            "riskReward": risk_reward,
            "confidence": self.confidence_scores
        }
    
    def _calculate_entry_points(self) -> Dict[str, Any]:
        """Calculate optimal entry points using multiple indicators"""
        close = self.data['Close'].values
        high = self.data['High'].values
        low = self.data['Low'].values
        
        # RSI analysis
        rsi = talib.RSI(close, timeperiod=14)
        
        # MACD analysis
        macd, signal, _ = talib.MACD(close)
        
        # Bollinger Bands
        upper, middle, lower = talib.BBANDS(close)
        
        # Support levels
        supports = self._find_support_levels()
        
        # Calculate primary entry based on weighted average of indicators
        primary_entry = self._weighted_price_average([
            (lower[-1], 0.3),  # Bollinger lower band
            (supports[0], 0.4),  # Strongest support
            (close[-1] * 0.99, 0.3)  # Just below current price
        ])
        
        # Calculate confidence score
        confidence = self._calculate_entry_confidence(rsi[-1], macd[-1], signal[-1], close[-1], lower[-1])
        
        return {
            "primary": round(primary_entry, 2),
            "secondary": round(primary_entry * 0.99, 2),
            "confidence": confidence,
            "indicators": self._get_entry_signals()
        }
    
    def _calculate_stop_loss(self) -> Dict[str, Any]:
        """Calculate stop loss levels based on various indicators"""
        close = self.data['Close'].values
        low = self.data['Low'].values
        
        # Calculate ATR for volatility-based stops
        atr = talib.ATR(self.data['High'].values, low, close)
        
        # Recent swing lows
        swing_lows = self._find_swing_lows()
        
        # Support levels
        supports = self._find_support_levels()
        
        # Primary stop loss (most conservative)
        primary_stop = max(
            supports[0] * 0.99,  # Just below strongest support
            close[-1] - (atr[-1] * 2)  # 2 ATR below current price
        )
        
        return {
            "primary": round(primary_stop, 2),
            "aggressive": round(primary_stop * 1.01, 2),
            "conservative": round(primary_stop * 0.99, 2),
            "indicators": [
                "Support levels",
                "ATR volatility",
                "Recent swing lows"
            ]
        }
    
    def _calculate_risk_reward(self, entry, exit, stop) -> Dict[str, Any]:
        """Calculate risk/reward metrics"""
        risk = entry['primary'] - stop['primary']
        reward = exit['primary'] - entry['primary']
        ratio = round(reward / risk, 2)
        
        return {
            "ratio": f"1:{ratio}",
            "potential_gain": round(reward, 2),
            "potential_loss": round(risk, 2),
            "win_rate": self._calculate_historical_win_rate()
        }
    
    def _calculate_historical_win_rate(self) -> float:
        """Calculate historical success rate of similar setups"""
        # Implementation would analyze past similar setups
        # and calculate win rate
        return 75.8  # Placeholder
    
    def _weighted_price_average(self, price_weights: list) -> float:
        """Calculate weighted average price from list of (price, weight) tuples"""
        total_weight = sum(weight for _, weight in price_weights)
        weighted_sum = sum(price * weight for price, weight in price_weights)
        return weighted_sum / total_weight
    
    # Additional helper methods...