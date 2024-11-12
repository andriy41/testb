import { useState, useEffect } from 'react';
import { MarketData, TimeframeType } from './market';
import { tradingService } from '../services/TradingAnalysisService';

export const useMarketData = (initialSymbol: string) => {
  const [marketData, setMarketData] = useState<MarketData | null>(null);
  const [symbol, setSymbol] = useState(initialSymbol);
  const [timeframe, setTimeframe] = useState<TimeframeType>('1h');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const data = await tradingService.getMarketData();
        setMarketData(data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [symbol, timeframe]);

  return {
    marketData,
    symbol,
    timeframe,
    loading,
    error,
    setSymbol,
    setTimeframe
  };
};
