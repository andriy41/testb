export type TimeframeType = '5m' | '15m' | '30m' | '1h' | '3h' | '1d' | 'Daily';

export type TrendType = 'BULLISH' | 'BEARISH' | 'NEUTRAL';

export interface MLAnalysis {
  prediction: TrendType;
  confidence: number;
  patternRecognition: PatternRecognition[];
  supportLevels: number[];
  resistanceLevels: number[];
}

export interface MarketSignal {
  mlAnalysis: MLAnalysis;
  technicalIndicators: TechnicalIndicators;
  currentPrice: number;
}

export interface TechnicalIndicators {
  rsi: number;
  bollingerBands?: {
    upperBand: number;
    lowerBand: number;
  };
  ichimokuCloud?: {
    conversionLine: number;
    baseLine: number;
    leadingSpanA: number;
    leadingSpanB: number;
  };
}

export interface PatternRecognition {
  pattern: string;
  confidence: number;
}
export interface MarketScan {
  sectorBreakdown: Array<{
    sectorName: string;
    percentage: number;
  }>;
  topStocks: StockCandidate[];
}

export interface MarketData {
  marketSignal: MarketSignal;
  marketConditions: MarketConditions;
  timeframeData: Record<TimeframeType, TimeframeData>;
  riskMetrics: RiskMetrics;
  performanceMetrics: PerformanceMetrics;
  marketScan: MarketScan;
}

export interface TimeframeData {
  timestamp: number[];
  close: number[];
  open: number[];
  high: number[];
  low: number[];
  volume: number[];
}

export interface MarketSignal {
  direction: 'buy' | 'sell' | 'neutral';
  strength: number;
  timestamp: number;
}

export interface MarketConditions {
  trend: TrendType;
  volatility: number;
  volume: number;
  manipulationIndicators: {
    unusualVolume: boolean;
    priceManipulation: boolean;
  };
}

export interface RiskMetrics {
  currentRisk: {
    positionSize: number;
    riskPerTrade: number;
  };
  stopLoss: number;
  takeProfit: number;
  riskRewardRatio: number;
  drawdown: {
    current: number;
    maximum: number;
    average: number;
    duration: number;
  };
  sortinoRatio: number;
}

export interface PerformanceMetrics {
  winRate: {
    overall: number;
    byTimeframe: Record<TimeframeType, number>;
  };
  profitLoss: {
    total: number;
    byStrategy: Record<string, number>;
  };
  riskAdjustedReturns: {
    sharpeRatio: number;
    sortinoRatio: number;
    calmarRatio: number;
    informationRatio: number;
  };
  drawdown: {
    current: number;
    maximum: number;
    average: number;
    duration: number;
  };
}

export interface MarketScan {
  sectorBreakdown: Array<{
    sectorName: string;
    percentage: number;
  }>;
  topStocks: StockCandidate[];
}

export interface StockCandidate {
  symbol: string;
  score: number;
  signals: string[];
}

export interface MLAnalysis {
  prediction: number;
  confidence: number;
  features: string[];
}

export interface PatternRecognition {
  pattern: string;
  probability: number;
  significance: number;
}

export type TrendType = 'bullish' | 'bearish' | 'sideways';
