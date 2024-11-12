// src/types/trading.ts
import { TimeframeType } from './market';

export const TRADING_CONSTANTS = {
    DEFAULT_SYMBOL: 'BTC/USD',
    AVAILABLE_SYMBOLS: ['BTC/USD', 'ETH/USD', 'SOL/USD'],
    TIMEFRAMES: ['1m', '5m', '15m', '1h', '4h', '1d'] as TimeframeType[]
};

export interface TradingDashboardProps {
    symbol?: string;
    timeframe?: TimeframeType;
}
