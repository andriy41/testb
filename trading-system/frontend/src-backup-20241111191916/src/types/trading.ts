export type TimeframeType = '1m' | '5m' | '15m' | '30m' | '1h' | '3h' | '4h' | '1d';
export type TimeframeType = '1m' | '5m' | '15m' | '30m' | '1h' | '3h' | '4h' | '1d';
export type TimeframeType = '1m' | '5m' | '15m' | '30m' | '1h' | '3h' | '4h' | '1d';
import { TimeframeType } from './market';

export interface SectorBreakdown {
  sectorName: string;
  percentage: number;
  momentum?: number;
}

export const TRADING_CONSTANTS = {
  DEFAULT_SYMBOL: 'BTC/USD',
  AVAILABLE_SYMBOLS: ['BTC/USD', 'ETH/USD', 'SOL/USD'],
  TIMEFRAMES: ['1m', '5m', '15m', '1h', '4h', '1d'] as TimeframeType[],
};
  | '3h'
  | '4h'
  | '1d';

// Technical Analysis Types
export interface MovingAverages {
  ma20: number;
  ma50: number;
  ma200: number;
}

export interface MACD {
  macd: number;
  signal: number;
  histogram: number;
}

export interface TechnicalIndicators {
  rsi: number;
  adx: number;
  macd: MACD;
  movingAverages: MovingAverages;
}

// Machine Learning Types
export interface PatternRecognition {
  pattern: string;
  probability: number;
}

export interface MLAnalysis {
  prediction: TrendType;
  confidenceScore: number;
  patternRecognition: PatternRecognition[];
}

// Market Analysis Types
export interface MarketSignal {
  symbol: string;
  timeframe: TimeframeType;
  signalType: SignalType;
  timestamp: number;
  currentPrice: number;
  technicalIndicators: TechnicalIndicators;
  mlAnalysis: MLAnalysis;
}

export interface SectorPerformance {
  sectorName: string;
  performance: number;
}

export interface EconomicIndicators {
  gdpGrowth: number;
  inflation: number;
  unemployment: number;
}

export interface MarketConditions {
  marketSentiment: SentimentType;
  majorTrend: TrendType;
  sectorPerformance: SectorPerformance[];
  economicIndicators: EconomicIndicators;
}

// Price Data Types
export interface TimeframeData {
  timestamp: number;
  timeframe: TimeframeType;
  open: number[];
  high: number[];
  low: number[];
  close: number[];
  volume: number[];
}

// Risk Management Types
export interface RiskMetrics {
  // Risk Ratios
  volatility: number;
  sharpeRatio: number;
  sortinoRatio: number;
  maxDrawdown: number;

  // Position Management
  positionSize: number;
  riskPerTrade: number;
  stopLoss: number;
  takeProfit: number;
  potentialReward: number;
}

// Performance Analysis Types
export interface RiskAdjustedReturns {
  sharpeRatio: number;
  sortinoRatio: number;
}

export interface Drawdown {
  maxDrawdown: number;
  currentDrawdown: number;
  drawdownDuration: number;
}

export interface WinRate {
  overall: number;
  byTimeframe: Record<TimeframeType, number>;
}

export interface PerformanceMetrics {
  winRate: WinRate;
  averageWin: number;
  averageLoss: number;
  profitFactor: number;
  riskAdjustedReturns: RiskAdjustedReturns;
  drawdown: Drawdown;
}

// Market Scanning Types
export interface StockCandidate {
  symbol: string;
  score: number;
  fundamentals?: {
    marketCap: number;
    peRatio: number;
    volume: number;
  };
  technicals?: {
    trend: TrendType;
    momentum: number;
    volatility: number;
  };
}

export interface SectorRotation {
  from: string;
  to: string;
  strength?: number;
}

export interface SectorBreakdown {
  sectorName: string;
  percentage: number;
  momentum?: number;
}

export interface MarketScan {
  topStocks: StockCandidate[];
  sectorRotation: SectorRotation[];
  sectorBreakdown: SectorBreakdown[];
  totalMarketCap: number;
}

// Aggregate Market Data Type
export interface MarketData {
  marketSignal: MarketSignal;
  marketConditions: MarketConditions;
  timeframeData: Record<TimeframeType, TimeframeData>;
  riskMetrics: RiskMetrics;
  performanceMetrics: PerformanceMetrics;
  marketScan: MarketScan;
}

import { TimeframeType } from '../types/market';

export const TRADING_CONSTANTS = {
  DEFAULT_SYMBOL: 'BTC/USD',
  AVAILABLE_SYMBOLS: ['BTC/USD', 'ETH/USD', 'SOL/USD'],
  TIMEFRAMES: ['1m', '5m', '15m', '1h', '4h', '1d'] as TimeframeType[],
};
```
