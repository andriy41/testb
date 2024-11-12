# Create types directory if it doesn't exist
New-Item -ItemType Directory -Force -Path ".\src\types"

# Create market.ts with type definitions
@"
export type TimeframeType = '5m' | '15m' | '30m' | '1h' | '3h' | 'Daily';

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
"@ | Out-File -FilePath ".\src\types\market.ts" -Encoding UTF8

# Create ui/card components directory
New-Item -ItemType Directory -Force -Path ".\src\components\ui"

# Create card.tsx component
@"
import * as React from 'react'

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}

export function Card({ className, ...props }: CardProps) {
  return (
    <div
      className={`rounded-lg border bg-card text-card-foreground shadow-sm \${className}`}
      {...props}
    />
  )
}

export interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {}

export function CardHeader({ className, ...props }: CardHeaderProps) {
  return <div className={`flex flex-col space-y-1.5 p-6 \${className}`} {...props} />
}

export interface CardTitleProps extends React.HTMLAttributes<HTMLHeadingElement> {}

export function CardTitle({ className, ...props }: CardTitleProps) {
  return (
    <h3
      className={`text-2xl font-semibold leading-none tracking-tight \${className}`}
      {...props}
    />
  )
}

export interface CardContentProps extends React.HTMLAttributes<HTMLDivElement> {}

export function CardContent({ className, ...props }: CardContentProps) {
  return <div className={`p-6 pt-0 \${className}`} {...props} />
}
"@ | Out-File -FilePath ".\src\components\ui\card.tsx" -Encoding UTF8

# Create trading.d.ts type definitions
@"
export interface MarketConditions {
  trend: string;
  volatility: number;
  volume: number;
}

export interface MarketScan {
  sectorBreakdown: Array<{
    sectorName: string;
    percentage: number;
  }>;
}
"@ | Out-File -FilePath ".\src\types\trading.d.ts" -Encoding UTF8

Write-Host "TypeScript type definitions and components have been created successfully."
