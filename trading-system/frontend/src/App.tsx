import React, { useState, useEffect } from 'react';
import { TimeframeType } from './types/market';

export const TIMEFRAMES: TimeframeType[] = ['5m', '15m', '30m', '1h', '3h', '1d'];
const App: React.FC = () => {
  // State management with proper typing
  const [selectedSymbol, setSelectedSymbol] = useState<string>('AAPL');
  const [selectedTimeframe, setSelectedTimeframe] = useState<TimeframeType>('1h');
  const [marketData, setMarketData] = useState<MarketData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
import { tradingService } from './services/TradingAnalysisService';
import { 
  MarketData, 
  TimeframeType, 
  TimeframeData 
} from './types/market';
import AdvancedChart from './components/AdvancedChart';

// Constants
export const TIMEFRAMES: TimeframeType[] = ['5m', '15m', '30m', '1h', '3h', '1d'];
const DEFAULT_SYMBOL = 'AAPL';

const App: React.FC = () => {
  // State management with proper typing
  const [selectedSymbol, setSelectedSymbol] = useState<string>(DEFAULT_SYMBOL);
  const [selectedTimeframe, setSelectedTimeframe] = useState<TimeframeType>('1h');
  const [marketData, setMarketData] = useState<MarketData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Type guard for TimeframeData
  const isValidTimeframeData = (data: unknown): data is TimeframeData => {
    if (!data || typeof data !== 'object') return false;
    const d = data as TimeframeData;
    return Array.isArray(d.timestamp) && Array.isArray(d.close);
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await tradingService.getMarketData();
        setMarketData(data);
      } catch (error) {
        console.error('Error fetching market data:', error);
        setError('Failed to fetch market data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [selectedSymbol, selectedTimeframe]);

  return (
    <div>
      <header>
        {/* Header content */}
      </header>

      <main className="max-w-7xl mx-auto py-6">
        {loading && <p>Loading...</p>}
        {error && <p>{error}</p>}
        {marketData && (
          <AdvancedChart
            data={marketData.timeframeData[selectedTimeframe]}
            timeframe={selectedTimeframe}
          />
        )}
        {/* Other components */}
      </main>
    </div>
  );
};

export default App;


