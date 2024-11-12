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
