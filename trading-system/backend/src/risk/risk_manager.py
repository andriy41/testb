from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from scipy import stats
import risk_metrics as rm
from datetime import datetime, timedelta

@dataclass
class PositionSize:
    units: float
    value: float
    risk_amount: float
    risk_percent: float
    position_type: str  # 'full', 'scaled', 'reduced'

@dataclass
class StopLevels:
    initial_stop: float
    trailing_stop: float
    breakeven_stop: float
    time_stop: datetime
    profit_stops: List[float]

@dataclass
class RiskMetrics:
    var_95: float
    cvar_95: float
    sharpe_ratio: float
    sortino_ratio: float
    max_drawdown: float
    beta: float
    correlation: float
    volatility: float

class RiskManager:
    def __init__(self, capital: float, risk_params: Dict[str, float]):
        self.capital = capital
        self.risk_params = {
            'max_position_size': 0.02,  # 2% max per trade
            'max_portfolio_risk': 0.05,  # 5% max portfolio risk
            'max_correlation_risk': 0.3,  # 30% max correlation
            'max_sector_exposure': 0.2,  # 20% max sector exposure
            'max_daily_drawdown': 0.03,  # 3% max daily drawdown
            'position_scaling_factor': 0.5,  # Scale position by 50% in high risk
            'stop_loss_atr_factor': 2.0,  # ATR multiplier for stops
            **risk_params
        }
        self.current_positions = {}
        self.portfolio_risk = PortfolioRisk()
        self.risk_monitor = RiskMonitor()
        
    def calculate_position_size(self, 
                              symbol: str,
                              entry_price: float,
                              stop_loss: float,
                              signal_strength: float,
                              market_regime: MarketRegime) -> PositionSize:
        """Calculate optimal position size based on multiple factors"""
        
        # Base position size calculation
        risk_amount = self.capital * self.risk_params['max_position_size']
        risk_per_share = abs(entry_price - stop_loss)
        base_units = risk_amount / risk_per_share
        
        # Adjust for market regime
        regime_factor = self._get_regime_adjustment(market_regime)
        
        # Adjust for signal strength
        signal_factor = self._get_signal_adjustment(signal_strength)
        
        # Adjust for current portfolio exposure
        portfolio_factor = self._get_portfolio_adjustment()
        
        # Calculate final position size
        adjusted_units = base_units * regime_factor * signal_factor * portfolio_factor
        position_value = adjusted_units * entry_price
        
        # Verify against risk limits
        final_units = self._verify_risk_limits(adjusted_units, entry_price, symbol)
        
        return PositionSize(
            units=final_units,
            value=final_units * entry_price,
            risk_amount=risk_amount,
            risk_percent=risk_amount / self.capital,
            position_type=self._get_position_type(regime_factor)
        )
    
    def calculate_stop_levels(self,
                            entry_price: float,
                            atr: float,
                            signal_strength: float,
                            market_regime: MarketRegime) -> StopLevels:
        """Calculate multiple stop loss levels"""
        
        # Initial stop loss
        initial_stop = entry_price - (atr * self.risk_params['stop_loss_atr_factor'])
        if market_regime.volatility == 'HIGH':
            initial_stop = entry_price - (atr * self.risk_params['stop_loss_atr_factor'] * 1.5)
        
        # Trailing stop
        trailing_stop = entry_price - (atr * 3)
        
        # Breakeven stop
        breakeven_stop = entry_price + (entry_price - initial_stop) * 0.3
        
        # Time-based stop
        time_stop = datetime.now() + timedelta(days=5)
        
        # Profit stops
        profit_stops = [
            entry_price + (entry_price - initial_stop) * multiplier
            for multiplier in [1.5, 2.0, 3.0]
        ]
        
        return StopLevels(
            initial_stop=initial_stop,
            trailing_stop=trailing_stop,
            breakeven_stop=breakeven_stop,
            time_stop=time_stop,
            profit_stops=profit_stops
        )
    
    def _get_regime_adjustment(self, regime: MarketRegime) -> float:
        """Adjust position size based on market regime"""
        if regime.volatility == 'HIGH':
            return self.risk_params['position_scaling_factor']
        elif regime.volatility == 'LOW' and regime.trend == 'STRONG':
            return 1.2
        return 1.0
    
    def _get_signal_adjustment(self, signal_strength: float) -> float:
        """Adjust position size based on signal strength"""
        if signal_strength > 0.8:
            return 1.2
        elif signal_strength < 0.4:
            return 0.8
        return 1.0
    
    def _get_portfolio_adjustment(self) -> float:
        """Adjust position size based on current portfolio exposure"""
        current_exposure = sum(pos.value for pos in self.current_positions.values())
        exposure_ratio = current_exposure / self.capital
        
        if exposure_ratio > self.risk_params['max_portfolio_risk']:
            return 0.5
        elif exposure_ratio < self.risk_params['max_portfolio_risk'] * 0.5:
            return 1.2
        return 1.0

class PortfolioRisk:
    def __init__(self):
        self.positions = {}
        self.correlations = pd.DataFrame()
        self.sector_exposure = {}
        
    def calculate_portfolio_metrics(self) -> RiskMetrics:
        """Calculate portfolio risk metrics"""
        portfolio_returns = self._calculate_portfolio_returns()
        
        return RiskMetrics(
            var_95=self._calculate_var(portfolio_returns),
            cvar_95=self._calculate_cvar(portfolio_returns),
            sharpe_ratio=self._calculate_sharpe_ratio(portfolio_returns),
            sortino_ratio=self._calculate_sortino_ratio(portfolio_returns),
            max_drawdown=self._calculate_max_drawdown(portfolio_returns),
            beta=self._calculate_portfolio_beta(),
            correlation=self._calculate_portfolio_correlation(),
            volatility=self._calculate_portfolio_volatility(portfolio_returns)
        )
    
    def update_correlations(self, prices: Dict[str, pd.Series]):
        """Update correlation matrix for portfolio positions"""
        returns = pd.DataFrame({
            symbol: prices[symbol].pct_change()
            for symbol in prices
        })
        self.correlations = returns.corr()
    
    def check_correlation_limits(self, symbol: str) -> bool:
        """Check if adding a position would violate correlation limits"""
        if symbol in self.correlations:
            max_correlation = self.correlations[symbol].abs().max()
            return max_correlation < self.risk_params['max_correlation_risk']
        return True
    
    def update_sector_exposure(self, sector_data: Dict[str, str]):
        """Update sector exposure calculations"""
        self.sector_exposure = {}
        for symbol, sector in sector_data.items():
            if symbol in self.positions:
                if sector not in self.sector_exposure:
                    self.sector_exposure[sector] = 0
                self.sector_exposure[sector] += self.positions[symbol].value
    
    def check_sector_limits(self, symbol: str, sector: str, value: float) -> bool:
        """Check if adding a position would violate sector exposure limits"""
        potential_exposure = self.sector_exposure.get(sector, 0) + value
        return potential_exposure / self.capital <= self.risk_params['max_sector_exposure']

class RiskMonitor:
    def __init__(self):
        self.risk_events = []
        self.alerts = []
        self.daily_stats = {}
        
    def monitor_position_risk(self, position: Dict[str, Any]) -> List[str]:
        """Monitor individual position risk"""
        warnings = []
        
        # Check for large losses
        if position['unrealized_pl'] < -position['risk_amount']:
            warnings.append(f"Position {position['symbol']} exceeds risk limit")
        
        # Check for time decay
        if datetime.now() > position['time_stop']:
            warnings.append(f"Position {position['symbol']} reached time stop")
        
        # Check for adverse movement
        if position['price'] < position['trailing_stop']:
            warnings.append(f"Position {position['symbol']} hit trailing stop")
        
        return warnings
    
    def monitor_portfolio_risk(self, portfolio: Dict[str, Any]) -> List[str]:
        """Monitor overall portfolio risk"""
        warnings = []
        
        # Check portfolio drawdown
        if portfolio['drawdown'] < -self.risk_params['max_daily_drawdown']:
            warnings.append("Portfolio exceeds daily drawdown limit")
        
        # Check portfolio exposure
        if portfolio['exposure'] > self.risk_params['max_portfolio_risk']:
            warnings.append("Portfolio exceeds exposure limit")
        
        # Check correlation risk
        if portfolio['max_correlation'] > self.risk_params['max_correlation_risk']:
            warnings.append("Portfolio exceeds correlation limit")
        
        return warnings
    
    def update_daily_stats(self, stats: Dict[str, float]):
        """Update daily risk statistics"""
        self.daily_stats = {
            'date': datetime.now(),
            'drawdown': stats['drawdown'],
            'exposure': stats['exposure'],
            'volatility': stats['volatility'],
            'var': stats['var_95'],
            'sharpe': stats['sharpe_ratio']
        }
        
    def generate_risk_report(self) -> Dict[str, Any]:
        """Generate comprehensive risk report"""
        return {
            'daily_stats': self.daily_stats,
            'risk_events': self.risk_events,
            'alerts': self.alerts,
            'risk_metrics': self._calculate_risk_metrics(),
            'recommendations': self._generate_risk_recommendations()
        }

class PositionManager:
    def __init__(self, risk_manager: RiskManager):
        self.risk_manager = risk_manager
        self.positions = {}
        self.position_history = []
        
    def open_position(self,
                     symbol: str,
                     signal: Dict[str, Any],
                     market_regime: MarketRegime) -> Dict[str, Any]:
        """Open new position with risk management"""
        
        # Calculate position size
        position_size = self.risk_manager.calculate_position_size(
            symbol=symbol,
            entry_price=signal['price'],
            stop_loss=signal['stop_loss'],
            signal_strength=signal['strength'],
            market_regime=market_regime
        )
        
        # Calculate stop levels
        stop_levels = self.risk_manager.calculate_stop_levels(
            entry_price=signal['price'],
            atr=signal['atr'],
            signal_strength=signal['strength'],
            market_regime=market_regime
        )
        
        # Create position
        position = {
            'symbol': symbol,
            'entry_price': signal['price'],
            'size': position_size,
            'stops': stop_levels,
            'entry_time': datetime.now(),
            'signal': signal,
            'market_regime': market_regime
        }
        
        # Store position
        self.positions[symbol] = position
        self.position_history.append(position)
        
        return position
    
    def update_position(self,
                       symbol: str,
                       current_price: float,
                       current_atr: float) -> Dict[str, Any]:
        """Update position and stops"""
        if symbol not in self.positions:
            return None
            
        position = self.positions[symbol]
        
        # Update stops
        new_trailing_stop = max(
            position['stops'].trailing_stop,
            current_price - (current_atr * self.risk_manager.risk_params['stop_loss_atr_factor'])
        )
        
        position['stops'].trailing_stop = new_trailing_stop
        
        # Update metrics
        position['current_price'] = current_price
        position['unrealized_pl'] = (current_price - position['entry_price']) * position['size'].units
        
        return position
    
    def close_position(self, symbol: str, reason: str) -> Dict[str, Any]:
        """Close position and record results"""
        if symbol not in self.positions:
            return None
            
        position = self.positions.pop(symbol)
        position['exit_time'] = datetime.now()
        position['exit_reason'] = reason
        position['realized_pl'] = (position['current_price'] - position['entry_price']) * position['size'].units
        
        self.position_history.append(position)
        
        return position
