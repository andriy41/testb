import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
from ..data.market_data import MarketData
from .technical_analyzer import TechnicalAnalyzer
from .manipulation_detector import ManipulationDetector
from .fakeout_detector import FakeoutDetector

class MarketAnalyzer:
    """
    Analyzes market data to identify trading opportunities and potential risks.
    Combines technical analysis, manipulation detection, and fakeout detection.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.technical_analyzer = TechnicalAnalyzer()
        self.manipulation_detector = ManipulationDetector()
        self.fakeout_detector = FakeoutDetector()
        
    async def analyze(self, market_data: MarketData) -> Dict:
        """
        Perform comprehensive market analysis.
        
        Args:
            market_data: MarketData object containing OHLCV and other market data
            
        Returns:
            Dict containing analysis results including:
            - Technical indicators
            - Market conditions
            - Risk factors
            - Trading opportunities
            - Manipulation indicators
            - Fakeout probabilities
        """
        try:
            # Get technical analysis
            technical_analysis = await self.technical_analyzer.analyze(market_data)
            
            # Detect potential manipulation
            manipulation_indicators = await self.manipulation_detector.detect(market_data)
            
            # Detect potential fakeouts
            fakeout_probabilities = await self.fakeout_detector.detect(market_data)
            
            # Analyze market conditions
            market_conditions = self._analyze_market_conditions(market_data)
            
            # Identify trading opportunities
            opportunities = self._identify_opportunities(
                technical_analysis,
                manipulation_indicators,
                fakeout_probabilities,
                market_conditions
            )
            
            # Calculate risk factors
            risk_factors = self._calculate_risk_factors(
                market_data,
                technical_analysis,
                manipulation_indicators,
                fakeout_probabilities
            )
            
            return {
                'timestamp': datetime.now().isoformat(),
                'symbol': market_data.symbol,
                'interval': market_data.interval,
                'technical_analysis': technical_analysis,
                'market_conditions': market_conditions,
                'manipulation_indicators': manipulation_indicators,
                'fakeout_probabilities': fakeout_probabilities,
                'opportunities': opportunities,
                'risk_factors': risk_factors
            }
            
        except Exception as e:
            self.logger.error(f"Market analysis error: {str(e)}")
            raise
            
    def _analyze_market_conditions(self, market_data: MarketData) -> Dict:
        """Analyze current market conditions"""
        try:
            df = market_data.to_dataframe()
            
            # Calculate volatility
            returns = df['close'].pct_change()
            volatility = returns.std() * np.sqrt(252)  # Annualized volatility
            
            # Calculate volume profile
            volume_sma = df['volume'].rolling(window=20).mean()
            relative_volume = df['volume'].iloc[-1] / volume_sma.iloc[-1]
            
            # Determine trend strength
            price_sma = df['close'].rolling(window=50).mean()
            trend_strength = (df['close'].iloc[-1] - price_sma.iloc[-1]) / price_sma.iloc[-1]
            
            # Market regime classification
            regime = self._classify_market_regime(df)
            
            return {
                'volatility': float(volatility),
                'relative_volume': float(relative_volume),
                'trend_strength': float(trend_strength),
                'market_regime': regime,
                'liquidity_score': self._calculate_liquidity_score(df)
            }
            
        except Exception as e:
            self.logger.error(f"Market conditions analysis error: {str(e)}")
            raise
            
    def _identify_opportunities(
        self,
        technical_analysis: Dict,
        manipulation_indicators: Dict,
        fakeout_probabilities: Dict,
        market_conditions: Dict
    ) -> List[Dict]:
        """Identify potential trading opportunities"""
        opportunities = []
        
        # Check for strong technical setups
        if self._is_valid_technical_setup(technical_analysis):
            # Verify no manipulation
            if not manipulation_indicators['manipulation_detected']:
                # Check fakeout probability
                if fakeout_probabilities['fakeout_probability'] < 0.3:
                    # Ensure favorable market conditions
                    if self._are_conditions_favorable(market_conditions):
                        opportunity = {
                            'type': self._determine_opportunity_type(technical_analysis),
                            'strength': self._calculate_opportunity_strength(
                                technical_analysis,
                                market_conditions
                            ),
                            'entry_zone': self._calculate_entry_zone(technical_analysis),
                            'targets': self._calculate_targets(technical_analysis),
                            'stop_loss': self._calculate_stop_loss(technical_analysis),
                            'confidence': self._calculate_confidence_score(
                                technical_analysis,
                                manipulation_indicators,
                                fakeout_probabilities,
                                market_conditions
                            )
                        }
                        opportunities.append(opportunity)
        
        return opportunities
        
    def _calculate_risk_factors(
        self,
        market_data: MarketData,
        technical_analysis: Dict,
        manipulation_indicators: Dict,
        fakeout_probabilities: Dict
    ) -> Dict:
        """Calculate various risk factors"""
        return {
            'volatility_risk': self._calculate_volatility_risk(market_data),
            'technical_risk': self._calculate_technical_risk(technical_analysis),
            'manipulation_risk': manipulation_indicators['risk_score'],
            'fakeout_risk': fakeout_probabilities['fakeout_probability'],
            'liquidity_risk': self._calculate_liquidity_risk(market_data),
            'correlation_risk': self._calculate_correlation_risk(market_data),
            'overall_risk_score': self._calculate_overall_risk_score(
                market_data,
                technical_analysis,
                manipulation_indicators,
                fakeout_probabilities
            )
        }
        
    def _classify_market_regime(self, df: pd.DataFrame) -> str:
        """Classify the current market regime"""
        # Calculate necessary metrics
        volatility = df['close'].pct_change().std()
        trend = self._calculate_trend_strength(df)
        volume_profile = self._analyze_volume_profile(df)
        
        # Classify regime based on metrics
        if volatility > 0.02:  # High volatility threshold
            if trend > 0.5:
                return 'TRENDING_VOLATILE'
            else:
                return 'CHOPPY_VOLATILE'
        else:
            if trend > 0.5:
                return 'TRENDING_STABLE'
            else:
                return 'RANGING_STABLE'
                
    def _calculate_liquidity_score(self, df: pd.DataFrame) -> float:
        """Calculate market liquidity score"""
        try:
            # Calculate spread and depth metrics
            typical_spread = (df['high'] - df['low']).mean()
            volume_depth = df['volume'].rolling(window=20).mean()
            
            # Calculate turnover ratio
            turnover = (df['volume'] * df['close']).rolling(window=20).mean()
            
            # Combine metrics into liquidity score
            liquidity_score = (
                (1 / typical_spread) *  # Lower spread = higher liquidity
                np.log1p(volume_depth) *  # Higher depth = higher liquidity
                np.log1p(turnover)  # Higher turnover = higher liquidity
            ).mean()
            
            return float(liquidity_score)
            
        except Exception as e:
            self.logger.error(f"Liquidity score calculation error: {str(e)}")
            return 0.0
            
    def _calculate_trend_strength(self, df: pd.DataFrame) -> float:
        """Calculate the strength of the current trend"""
        try:
            # Calculate directional movement
            plus_dm = df['high'].diff()
            minus_dm = df['low'].diff()
            
            # Calculate true range
            tr = pd.DataFrame({
                'h-l': df['high'] - df['low'],
                'h-pc': abs(df['high'] - df['close'].shift(1)),
                'l-pc': abs(df['low'] - df['close'].shift(1))
            }).max(axis=1)
            
            # Calculate ADX
            smoothing_period = 14
            tr_smoothed = tr.rolling(window=smoothing_period).mean()
            plus_di = (plus_dm.rolling(window=smoothing_period).mean() / tr_smoothed) * 100
            minus_di = (minus_dm.rolling(window=smoothing_period).mean() / tr_smoothed) * 100
            dx = abs(plus_di - minus_di) / (plus_di + minus_di) * 100
            adx = dx.rolling(window=smoothing_period).mean()
            
            return float(adx.iloc[-1]) / 100.0  # Normalize to 0-1 range
            
        except Exception as e:
            self.logger.error(f"Trend strength calculation error: {str(e)}")
            return 0.0
