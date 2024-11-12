import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
from ..data.market_data import MarketData

class FakeoutDetector:
    """
    Detects potential fakeout patterns in market data by analyzing price action,
    volume confirmation, and historical patterns.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.min_confidence = 0.8
        self.lookback_periods = 20
        self.thresholds = {
            'price_reversal': 0.5,      # % price reversal required
            'volume_surge': 2.0,        # Volume surge multiplier
            'time_window': 5,           # Periods to confirm fakeout
            'support_resistance_zone': 0.1  # % zone around levels
        }
        
    async def detect(self, market_data: MarketData) -> Dict:
        """
        Detect potential fakeout patterns in market data.
        
        Args:
            market_data: MarketData object containing market data
            
        Returns:
            Dict containing fakeout detection results
        """
        try:
            df = market_data.to_dataframe()
            
            # Analyze different types of fakeouts
            breakout_fakeouts = self._detect_breakout_fakeouts(df)
            support_resistance_fakeouts = self._detect_support_resistance_fakeouts(df)
            trend_fakeouts = self._detect_trend_fakeouts(df)
            
            # Combine and analyze all fakeout signals
            fakeout_probability = self._calculate_fakeout_probability(
                breakout_fakeouts,
                support_resistance_fakeouts,
                trend_fakeouts
            )
            
            return {
                'timestamp': datetime.now().isoformat(),
                'fakeout_detected': fakeout_probability > self.min_confidence,
                'fakeout_probability': float(fakeout_probability),
                'details': {
                    'breakout_fakeouts': breakout_fakeouts,
                    'support_resistance_fakeouts': support_resistance_fakeouts,
                    'trend_fakeouts': trend_fakeouts
                }
            }
            
        except Exception as e:
            self.logger.error(f"Fakeout detection error: {str(e)}")
            raise
            
    def _detect_breakout_fakeouts(self, df: pd.DataFrame) -> Dict:
        """Detect breakout fakeout patterns"""
        try:
            close = df['close'].values
            high = df['high'].values
            low = df['low'].values
            volume = df['volume'].values
            
            # Calculate key levels
            upper_level = pd.Series(high).rolling(window=20).max()
            lower_level = pd.Series(low).rolling(window=20).min()
            
            # Detect breakouts and reversals
            breakouts_up = close > upper_level
            breakouts_down = close < lower_level
            
            # Check for failed breakouts
            failed_breakouts = []
            
            for i in range(len(close)-self.thresholds['time_window'], len(close)):
                if i > 0:
                    # Check upward breakout failure
                    if breakouts_up[i-1] and close[i] < close[i-1]:
                        failed_breakouts.append({
                            'type': 'upward_failure',
                            'index': i,
                            'confidence': self._calculate_breakout_confidence(
                                close[i-1:i+1],
                                volume[i-1:i+1],
                                'up'
                            )
                        })
                    
                    # Check downward breakout failure
                    if breakouts_down[i-1] and close[i] > close[i-1]:
                        failed_breakouts.append({
                            'type': 'downward_failure',
                            'index': i,
                            'confidence': self._calculate_breakout_confidence(
                                close[i-1:i+1],
                                volume[i-1:i+1],
                                'down'
                            )
                        })
            
            return {
                'failed_breakouts': failed_breakouts,
                'breakout_zones': self._identify_breakout_zones(df),
                'volume_confirmation': self._check_volume_confirmation(df)
            }
            
        except Exception as e:
            self.logger.error(f"Breakout fakeout detection error: {str(e)}")
            return {}
            
    def _detect_support_resistance_fakeouts(self, df: pd.DataFrame) -> Dict:
        """Detect support/resistance fakeout patterns"""
        try:
            close = df['close'].values
            
            # Identify support and resistance levels
            levels = self._identify_support_resistance_levels(df)
            
            # Check for failed tests of levels
            failed_tests = []
            
            for level in levels:
                # Check for price approaching level
                approaches = np.abs(close - level) < (level * self.thresholds['support_resistance_zone'])
                
                for i in range(len(close)-self.thresholds['time_window'], len(close)):
                    if approaches[i]:
                        # Check for failed test
                        if self._is_failed_level_test(close[i-5:i+1], level):
                            failed_tests.append({
                                'level': float(level),
                                'index': i,
                                'confidence': self._calculate_level_test_confidence(
                                    close[i-5:i+1],
                                    level
                                )
                            })
            
            return {
                'failed_level_tests': failed_tests,
                'key_levels': [float(level) for level in levels],
                'level_strength': self._calculate_level_strength(df, levels)
            }
            
        except Exception as e:
            self.logger.error(f"Support/Resistance fakeout detection error: {str(e)}")
            return {}
            
    def _detect_trend_fakeouts(self, df: pd.DataFrame) -> Dict:
        """Detect trend fakeout patterns"""
        try:
            close = df['close'].values
            
            # Calculate trend metrics
            sma_20 = pd.Series(close).rolling(window=20).mean()
            sma_50 = pd.Series(close).rolling(window=50).mean()
            
            # Detect trend changes
            trend_changes = []
            
            for i in range(len(close)-self.thresholds['time_window'], len(close)):
                if i > 50:  # Ensure we have enough data
                    # Check for failed trend change
                    if self._is_failed_trend_change(
                        close[i-10:i+1],
                        sma_20[i-10:i+1],
                        sma_50[i-10:i+1]
                    ):
                        trend_changes.append({
                            'index': i,
                            'confidence': self._calculate_trend_change_confidence(
                                close[i-10:i+1],
                                sma_20[i-10:i+1],
                                sma_50[i-10:i+1]
                            )
                        })
            
            return {
                'failed_trend_changes': trend_changes,
                'trend_strength': self._calculate_trend_strength(df),
                'trend_consistency': self._calculate_trend_consistency(df)
            }
            
        except Exception as e:
            self.logger.error(f"Trend fakeout detection error: {str(e)}")
            return {}
            
    def _calculate_fakeout_probability(
        self,
        breakout_fakeouts: Dict,
        support_resistance_fakeouts: Dict,
        trend_fakeouts: Dict
    ) -> float:
        """Calculate overall fakeout probability"""
        try:
            # Weight different factors
            weights = {
                'breakout': 0.4,
                'support_resistance': 0.4,
                'trend': 0.2
            }
            
            # Calculate component probabilities
            breakout_prob = self._calculate_breakout_fakeout_probability(breakout_fakeouts)
            sr_prob = self._calculate_sr_fakeout_probability(support_resistance_fakeouts)
            trend_prob = self._calculate_trend_fakeout_probability(trend_fakeouts)
            
            # Calculate weighted probability
            probability = (
                breakout_prob * weights['breakout'] +
                sr_prob * weights['support_resistance'] +
                trend_prob * weights['trend']
            )
            
            return min(max(probability, 0), 1)  # Ensure result is between 0 and 1
            
        except Exception as e:
            self.logger.error(f"Fakeout probability calculation error: {str(e)}")
            return 0.0
            
    def _identify_support_resistance_levels(self, df: pd.DataFrame) -> np.ndarray:
        """Identify support and resistance levels"""
        try:
            high = df['high'].values
            low = df['low'].values
            
            # Find local maxima and minima
            window = 20
            high_series = pd.Series(high)
            low_series = pd.Series(low)
            
            resistance_levels = high_series[
                (high_series.shift(window) < high_series) &
                (high_series.shift(-window) < high_series)
            ]
            
            support_levels = low_series[
                (low_series.shift(window) > low_series) &
                (low_series.shift(-window) > low_series)
            ]
            
            # Combine and cluster levels
            all_levels = np.concatenate([resistance_levels, support_levels])
            return self._cluster_price_levels(all_levels)
            
        except Exception as e:
            self.logger.error(f"Support/Resistance level identification error: {str(e)}")
            return np.array([])
            
    def _cluster_price_levels(self, levels: np.ndarray) -> np.ndarray:
        """Cluster nearby price levels"""
        if len(levels) == 0:
            return np.array([])
            
        # Sort levels
        sorted_levels = np.sort(levels)
        
        # Initialize clusters
        clusters = []
        current_cluster = [sorted_levels[0]]
        
        # Cluster nearby levels
        for level in sorted_levels[1:]:
            if level - current_cluster[-1] < (current_cluster[-1] * 0.01):  # 1% threshold
                current_cluster.append(level)
            else:
                clusters.append(np.mean(current_cluster))
                current_cluster = [level]
                
        # Add last cluster
        if current_cluster:
            clusters.append(np.mean(current_cluster))
            
        return np.array(clusters)
