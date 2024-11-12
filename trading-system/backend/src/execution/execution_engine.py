from dataclasses import dataclass
from typing import Dict, List, Optional, Union, Tuple
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import logging
from abc import ABC, abstractmethod

class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"
    TRAILING_STOP = "TRAILING_STOP"

class OrderStatus(Enum):
    PENDING = "PENDING"
    SUBMITTED = "SUBMITTED"
    PARTIAL = "PARTIAL"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"

@dataclass
class Order:
    symbol: str
    order_type: OrderType
    side: str
    quantity: float
    price: Optional[float]
    stop_price: Optional[float]
    time_in_force: str
    order_id: str
    status: OrderStatus
    filled_quantity: float = 0
    average_fill_price: float = 0
    commission: float = 0
    notes: str = ""

@dataclass
class ExecutionMetrics:
    slippage: float
    market_impact: float
    timing_cost: float
    total_cost: float
    execution_time: float
    success_rate: float

class ExecutionEngine:
    def __init__(self, broker_connection, risk_manager):
        self.broker = broker_connection
        self.risk_manager = risk_manager
        self.order_manager = OrderManager()
        self.execution_optimizer = ExecutionOptimizer()
        self.performance_tracker = PerformanceTracker()
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        logger = logging.getLogger('ExecutionEngine')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('execution.log')
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(handler)
        return logger

    async def execute_signal(self, signal: Dict, position_size: float) -> Optional[Order]:
        """Execute trading signal with smart order routing"""
        try:
            # Validate signal and check risk limits
            if not self._validate_signal(signal):
                return None

            # Get market data for execution
            market_data = await self.broker.get_market_data(signal['symbol'])
            
            # Determine optimal execution strategy
            execution_strategy = self.execution_optimizer.get_optimal_strategy(
                signal, market_data, position_size
            )
            
            # Create and submit order
            order = await self._create_and_submit_order(signal, execution_strategy)
            
            # Monitor order execution
            final_order = await self._monitor_execution(order)
            
            # Track execution performance
            self.performance_tracker.track_execution(order, market_data)
            
            return final_order

        except Exception as e:
            self.logger.error(f"Execution error: {str(e)}")
            raise

    async def _create_and_submit_order(self, signal: Dict, strategy: Dict) -> Order:
        """Create and submit order based on execution strategy"""
        order = Order(
            symbol=signal['symbol'],
            order_type=strategy['order_type'],
            side=signal['side'],
            quantity=strategy['quantity'],
            price=strategy.get('price'),
            stop_price=strategy.get('stop_price'),
            time_in_force=strategy['time_in_force'],
            order_id=self._generate_order_id(),
            status=OrderStatus.PENDING
        )
        
        return await self.order_manager.submit_order(order)

    async def _monitor_execution(self, order: Order) -> Order:
        """Monitor order execution and handle exceptions"""
        try:
            while order.status not in [OrderStatus.FILLED, OrderStatus.CANCELLED, OrderStatus.REJECTED]:
                order = await self.order_manager.get_order_status(order.order_id)
                
                if order.status == OrderStatus.PARTIAL:
                    self._handle_partial_fill(order)
                
                await asyncio.sleep(0.1)
            
            return order
            
        except Exception as e:
            self.logger.error(f"Order monitoring error: {str(e)}")
            await self.order_manager.cancel_order(order.order_id)
            raise

class OrderManager:
    def __init__(self):
        self.orders = {}
        self.filled_orders = {}
        self.active_orders = {}
        self.execution_analytics = ExecutionAnalytics()
        
    async def submit_order(self, order: Order) -> Order:
        """Submit order to broker and track it"""
        try:
            # Pre-submission validation
            self._validate_order(order)
            
            # Submit to broker
            submitted_order = await self.broker.submit_order(order)
            
            # Track order
            self.orders[submitted_order.order_id] = submitted_order
            self.active_orders[submitted_order.order_id] = submitted_order
            
            return submitted_order
            
        except Exception as e:
            self.logger.error(f"Order submission error: {str(e)}")
            raise

    async def cancel_order(self, order_id: str) -> bool:
        """Cancel an active order"""
        try:
            if order_id in self.active_orders:
                await self.broker.cancel_order(order_id)
                del self.active_orders[order_id]
                self.orders[order_id].status = OrderStatus.CANCELLED
                return True
            return False
        except Exception as e:
            self.logger.error(f"Order cancellation error: {str(e)}")
            raise

    def _validate_order(self, order: Order):
        """Validate order parameters"""
        if not order.symbol or not order.quantity:
            raise ValueError("Invalid order parameters")
        if order.order_type not in OrderType:
            raise ValueError("Invalid order type")

class ExecutionOptimizer:
    def __init__(self):
        self.market_impact_model = MarketImpactModel()
        self.timing_optimizer = TimingOptimizer()
        
    def get_optimal_strategy(self, signal: Dict, market_data: Dict, size: float) -> Dict:
        """Determine optimal execution strategy"""
        # Analyze market conditions
        market_conditions = self._analyze_market_conditions(market_data)
        
        # Estimate market impact
        impact = self.market_impact_model.estimate_impact(size, market_data)
        
        # Determine optimal timing
        timing = self.timing_optimizer.get_optimal_timing(market_conditions)
        
        # Build execution strategy
        return self._build_execution_strategy(signal, impact, timing)
    
    def _analyze_market_conditions(self, market_data: Dict) -> Dict:
        """Analyze current market conditions"""
        return {
            'liquidity': self._calculate_liquidity(market_data),
            'volatility': self._calculate_volatility(market_data),
            'spread': self._calculate_spread(market_data)
        }
    
    def _build_execution_strategy(self, signal: Dict, impact: float, timing: Dict) -> Dict:
        """Build execution strategy based on analysis"""
        if impact > 0.01:  # High market impact
            return self._build_algorithmic_strategy(signal, impact)
        return self._build_direct_strategy(signal)

class PerformanceTracker:
    def __init__(self):
        self.executions = {}
        self.metrics = {}
        
    def track_execution(self, order: Order, market_data: Dict):
        """Track execution performance"""
        metrics = self._calculate_execution_metrics(order, market_data)
        self.executions[order.order_id] = metrics
        self._update_aggregate_metrics(metrics)
    
    def _calculate_execution_metrics(self, order: Order, market_data: Dict) -> ExecutionMetrics:
        """Calculate execution performance metrics"""
        return ExecutionMetrics(
            slippage=self._calculate_slippage(order, market_data),
            market_impact=self._calculate_market_impact(order, market_data),
            timing_cost=self._calculate_timing_cost(order, market_data),
            total_cost=0.0,  # Will be calculated
            execution_time=0.0,  # Will be calculated
            success_rate=1.0 if order.status == OrderStatus.FILLED else 0.0
        )
    
    def generate_performance_report(self) -> Dict:
        """Generate execution performance report"""
        return {
            'overall_metrics': self.metrics,
            'recent_executions': self._get_recent_executions(),
            'cost_analysis': self._analyze_costs(),
            'recommendations': self._generate_recommendations()
        }

class BrokerConnection(ABC):
    @abstractmethod
    async def submit_order(self, order: Order) -> Order:
        pass
    
    @abstractmethod
    async def cancel_order(self, order_id: str) -> bool:
        pass
    
    @abstractmethod
    async def get_market_data(self, symbol: str) -> Dict:
        pass

class MarketImpactModel:
    def estimate_impact(self, size: float, market_data: Dict) -> float:
        """Estimate market impact of trade"""
        avg_volume = market_data['average_volume']
        volatility = market_data['volatility']
        spread = market_data['spread']
        
        # Simple market impact model
        volume_ratio = size / avg_volume
        impact = volume_ratio * volatility * spread
        
        return impact

class TimingOptimizer:
    def get_optimal_timing(self, market_conditions: Dict) -> Dict:
        """Determine optimal trade timing"""
        if market_conditions['volatility'] > 0.02:
            return self._get_high_volatility_timing()
        return self._get_normal_timing()
    
    def _get_high_volatility_timing(self) -> Dict:
        return {
            'type': 'TWAP',
            'duration': timedelta(minutes=30),
            'intervals': 6
        }
    
    def _get_normal_timing(self) -> Dict:
        return {
            'type': 'IMMEDIATE',
            'duration': timedelta(minutes=5),
            'intervals': 1
        }

class ExecutionAnalytics:
    def __init__(self):
        self.analytics_data = pd.DataFrame()
        
    def add_execution_data(self, order: Order, market_data: Dict):
        """Add execution data for analysis"""
        execution_data = {
            'timestamp': datetime.now(),
            'symbol': order.symbol,
            'order_type': order.order_type,
            'quantity': order.quantity,
            'fill_price': order.average_fill_price,
            'market_price': market_data['price'],
            'spread': market_data['spread'],
            'volume': market_data['volume']
        }
        
        self.analytics_data = self.analytics_data.append(
            execution_data, ignore_index=True
        )
    
    def analyze_executions(self) -> Dict:
        """Analyze execution performance"""
        return {
            'slippage_analysis': self._analyze_slippage(),
            'timing_analysis': self._analyze_timing(),
            'cost_analysis': self._analyze_costs(),
            'recommendations': self._generate_recommendations()
        }
