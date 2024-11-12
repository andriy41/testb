// src/types/market.ts

export type TimeframeType = '1m' | '5m' | '15m' | '30m' | '1h' | '3h' | '4h' | '1d';
export type SignalType = 'BUY' | 'SELL' | 'HOLD';
export type TrendType = 'BULLISH' | 'BEARISH' | 'NEUTRAL' | 'Uptrend' | 'Downtrend' | 'Sideways';
export type SentimentType = 'POSITIVE' | 'NEGATIVE' | 'NEUTRAL' | 'Bullish' | 'Bearish';
export type VolatilityLevel = 'LOW' | 'MEDIUM' | 'HIGH';

export interface MarketSignal {
    type: SignalType;
    strength: number;
    timestamp: number;
}

export interface MarketConditions {
    trend: TrendType;
    volatility: VolatilityLevel;
    sentiment: SentimentType;
    majorTrend: TrendType;
    marketSentiment: SentimentType;
}

export interface TimeframeData {
    timeframe: TimeframeType;
    data: {
        price: number;
        volume: number;
        timestamp: number;
    }[];
}

export interface RiskMetrics {
    volatility: number;
    drawdown: number;
    sharpeRatio: number;
}

export interface PerformanceMetrics {
    returns: number;
    winRate: number;
    profitFactor: number;
}

export interface MarketScan {
    opportunities: Array<{
        symbol: string;
        signal: SignalType;
        confidence: number;
    }>;
}

export interface StockCandidate {
    symbol: string;
    score: number;
    signals: MarketSignal[];
}

export const TRADING_CONSTANTS = {
    DEFAULT_SYMBOL: 'BTC/USD',
    AVAILABLE_SYMBOLS: ['BTC/USD', 'ETH/USD', 'SOL/USD'],
    TIMEFRAMES: ['1m', '5m', '15m', '1h', '4h', '1d'] as TimeframeType[]
};
