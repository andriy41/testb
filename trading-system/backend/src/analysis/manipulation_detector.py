import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
from ..data.market_data import MarketData

class ManipulationDetector:
    """
    Detects potential market manipulation by analyzing various market metrics
    and patterns that could indicate manipulative behavior.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.detection_thresholds = {
            'volume_spike': 3.0,      # Standard deviations
            'price_movement': 2.5,     # Standard deviations
            'bid_ask_spread': 2.0,     # Standard deviations
            'trade_size': 3.0,         # Standard deviations
            'momentum': 2.5,           # Standard deviations
            'correlation': 0.85        # Correlation coefficient
        }
        
    async def detect(self, market_data: MarketData) -> Dict:
        """
        Detect potential market manipulation patterns.
        
        Args:
            market_data: MarketData object containing market data
            
        Returns:
            Dict containing manipulation detection results
        """
        try:
            df = market_data.to_dataframe()
            
            # Run various manipulation detection algorithms
            volume_manipulation = self._detect_volume_manipulation(df)
            price_manipulation = self._detect_price_manipulation(df)
            momentum_manipulation = self._detect_momentum_manipulation(df)
            pattern_manipulation = self._detect_pattern_manipulation(df)
            
            # Calculate overall manipulation probability
            manipulation_probability = self._calculate_manipulation_probability(
                volume_manipulation,
                price_manipulation,
                momentum_manipulation,
                pattern_manipulation
            )
            
            return {
                'timestamp': datetime.now().isoformat(),
                'manipulation_detected': manipulation_probability > 0.7,
                'manipulation_probability': float(manipulation_probability),
                'risk_score': float(manipulation_probability * 100),
                'details': {
                    'volume_manipulation': volume_manipulation,
                    'price_manipulation': price_manipulation,
                    'momentum_manipulation': momentum_manipulation,
                    'pattern_manipulation': pattern_manipulation
                }
            }
            
        except Exception as e:
            self.logger.error(f"Manipulation detection error: {str(e)}")
            raise
            
    def _detect_volume_manipulation(self, df: pd.DataFrame) -> Dict:
        """Detect volume-based manipulation patterns"""
        try:
            volume = df['volume'].values
            close = df['close'].values
            
            # Calculate volume metrics
            volume_sma = pd.Series(volume).rolling(window=20).mean()
            volume_std = pd.Series(volume).rolling(window=20).std()
            relative_volume = volume / volume_sma
            
            # Detect volume spikes
            volume_spikes = relative_volume > self.detection_thresholds['volume_spike']
            
            # Detect volume/price divergence
            price_returns = pd.Series(close).pct_change()
            volume_returns = pd.Series(volume).pct_change()
            divergence = np.corrcoef(price_returns.fillna(0), volume_returns.fillna(0))[0, 1]
            
            return {
                'volume_spikes_detected': bool(volume_spikes.any()),
                'volume_spike_periods': np.where(volume_spikes)[0].tolist(),
                'max_relative_volume': float(relative_volume.max()),
                'volume_price_divergence': float(divergence),
                'abnormal_volume_score': float(
                    (relative_volume > self.detection_thresholds['volume_spike']).mean()
                )
            }
            
        except Exception as e:
            self.logger.error(f"Volume manipulation detection error: {str(e)}")
            return {}
            
    def _detect_price_manipulation(self, df: pd.DataFrame) -> Dict:
        """Detect price-based manipulation patterns"""
        try:
            close = df['close'].values
            high = df['high'].values
            low = df['low'].values
            
            # Calculate price metrics
            returns = pd.Series(close).pct_change()
            returns_std = returns.rolling(window=20).std()
            
            # Detect abnormal price movements
            abnormal_moves = np.abs(returns) > (returns_std * self.detection_thresholds['price_movement'])
            
            # Calculate price range analysis
            true_range = pd.DataFrame({
                'hl': high - low,
                'hc': np.abs(high - np.roll(close, 1)),
                'lc': np.abs(low - np.roll(close, 1))
            }).max(axis=1)
            
            return {
                'abnormal_moves_detected': bool(abnormal_moves.any()),
                'abnormal_move_periods': np.where(abnormal_moves)[0].tolist(),
                'max_price_deviation': float(np.abs(returns).max()),
                'price_volatility_score': float(returns_std.iloc[-1]),
                'average_true_range': float(true_range.mean())
            }
            
        except Exception as e:
            self.logger.error(f"Price manipulation detection error: {str(e)}")
            return {}
            
    def _detect_momentum_manipulation(self, df: pd.DataFrame) -> Dict:
        """Detect momentum-based manipulation patterns"""
        try:
            close = df['close'].values
            volume = df['volume'].values
            
            # Calculate momentum metrics
            momentum = pd.Series(close).diff(periods=5)
            momentum_std = momentum.rolling(window=20).std()
            
            # Detect momentum anomalies
            abnormal_momentum = np.abs(momentum) > (momentum_std * self.detection_thresholds['momentum'])
            
            # Calculate momentum/volume relationship
            momentum_volume_corr = np.corrcoef(
                momentum.fillna(0),
                pd.Series(volume).pct_change().fillna(0)
            )[0, 1]
            
            return {
                'abnormal_momentum_detected': bool(abnormal_momentum.any()),
                'momentum_anomaly_periods': np.where(abnormal_momentum)[0].tolist(),
                'max_momentum_deviation': float(np.abs(momentum).max()),
                'momentum_volume_correlation': float(momentum_volume_corr),
                'momentum_volatility_score': float(momentum_std.iloc[-1])
            }
            
        except Exception as e:
            self.logger.error(f"Momentum manipulation detection error: {str(e)}")
            return {}
            
    def _detect_pattern_manipulation(self, df: pd.DataFrame) -> Dict:
        """Detect pattern-based manipulation"""
        try:
            close = df['close'].values
            volume = df['volume'].values
            
            # Calculate pattern metrics
            price_patterns = self._identify_price_patterns(close)
            volume_patterns = self._identify_volume_patterns(volume)
            
            # Detect pattern anomalies
            pattern_correlation = np.corrcoef(
                price_patterns.fillna(0),
                volume_patterns.fillna(0)
            )[0, 1]
            
            return {
                'suspicious_patterns_detected': pattern_correlation > self.detection_thresholds['correlation'],
                'pattern_correlation': float(pattern_correlation),
                'price_pattern_score': float(price_patterns.std()),
                'volume_pattern_score': float(volume_patterns.std())
            }
            
        except Exception as e:
            self.logger.error(f"Pattern manipulation detection error: {str(e)}")
            return {}
            
    def _identify_price_patterns(self, prices: np.ndarray) -> pd.Series:
        """Identify price patterns"""
        try:
            price_series = pd.Series(prices)
            
            # Calculate various pattern indicators
            sma = price_series.rolling(window=20).mean()
            upper_band = sma + (price_series.rolling(window=20).std() * 2)
            lower_band = sma - (price_series.rolling(window=20).std() * 2)
            
            # Create pattern score
            pattern_score = (price_series - sma) / (upper_band - lower_band)
            
            return pattern_score
            
        except Exception as e:
            self.logger.error(f"Price pattern identification error: {str(e)}")
            return pd.Series()
            
    def _identify_volume_patterns(self, volume: np.ndarray) -> pd.Series:
        """Identify volume patterns"""
        try:
            volume_series = pd.Series(volume)
            
            # Calculate volume pattern indicators
            sma = volume_series.rolling(window=20).mean()
            std = volume_series.rolling(window=20).std()
            
            # Create pattern score
            pattern_score = (volume_series - sma) / std
            
            return pattern_score
            
        except Exception as e:
            self.logger.error(f"Volume pattern identification error: {str(e)}")
            return pd.Series()
            
    def _calculate_manipulation_probability(
        self,
        volume_manipulation: Dict,
        price_manipulation: Dict,
        momentum_manipulation: Dict,
        pattern_manipulation: Dict
    ) -> float:
        """Calculate overall manipulation probability"""
        try:
            # Weight different factors
            weights = {
                'volume': 0.3,
                'price': 0.3,
                'momentum': 0.2,
                'pattern': 0.2
            }
            
            # Calculate component scores
            volume_score = volume_manipulation.get('abnormal_volume_score', 0)
            price_score = price_manipulation.get('price_volatility_score', 0)
            momentum_score = momentum_manipulation.get('momentum_volatility_score', 0)
            pattern_score = pattern_manipulation.get('pattern_correlation', 0)
            
            # Calculate weighted probability
            probability = (
                volume_score * weights['volume'] +
                price_score * weights['price'] +
                momentum_score * weights['momentum'] +
                pattern_score * weights['pattern']
            )
            
            return min(max(probability, 0), 1)  # Ensure result is between 0 and 1
            
        except Exception as e:
            self.logger.error(f"Manipulation probability calculation error: {str(e)}")
            return 0.0
