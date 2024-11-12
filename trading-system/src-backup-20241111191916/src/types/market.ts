// src/types/market.ts
export type SignalType = 'BUY' | 'SELL' | 'HOLD';
export type TrendType = 'BULLISH' | 'BEARISH' | 'NEUTRAL';
export type VolatilityLevel = 'LOW' | 'MEDIUM' | 'HIGH';
export type MarketSentimentType = 'POSITIVE' | 'NEGATIVE' | 'NEUTRAL';
export type TimeframeType = '1m' | '5m' | '15m' | '30m' | '1h' | '3h' | '4h' | '1d';

export interface MarketSignal {
    type: SignalType;
    strength: number;
    timestamp: number;
}

export interface MarketConditions {
    trend: TrendType;
    volatility: VolatilityLevel;
    sentiment: MarketSentimentType;
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
