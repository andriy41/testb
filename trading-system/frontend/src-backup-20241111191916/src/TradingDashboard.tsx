import React, { 
  useMemo, 
  memo, 
  lazy, 
  Suspense,
  useCallback
} from 'react';
import { 
  MarketData, 
  TimeframeType,
  MarketSignal 
} from './types/market';
import AdvancedChart from './components/AdvancedChart';
import { analyzeMarketData } from './components/analysis/MarketAnalysis';
import { useMarketData } from './types/useMarketData';

// Constants
const TRADING_CONSTANTS = {
  DEFAULT_SYMBOL: 'AAPL',
  AVAILABLE_SYMBOLS: ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META'],
  TIMEFRAMES: ['1m', '5m', '15m', '30m', '1h', '3h', '4h', '1d'] as TimeframeType[]
};

// Types
interface MarketHeaderProps {
  symbol: string;
  timeframe: TimeframeType;
  onSymbolChange: (symbol: string) => void;
  onTimeframeChange: (timeframe: TimeframeType) => void;
}

interface TradingDashboardProps {
  initialSymbol?: string;
}

// Memoized Header Component
const MarketHeader = memo(({ 
  symbol, 
  timeframe, 
  onSymbolChange, 
  onTimeframeChange 
}: MarketHeaderProps) => {
  return (
    <div className="flex justify-between items-center p-4 bg-white shadow-sm">
      <h1 className="text-2xl font-bold">Trading Dashboard</h1>
      <div className="flex space-x-4">
        <select
          value={symbol}
          onChange={(e) => onSymbolChange(e.target.value)}
          className="form-select"
        >
          {TRADING_CONSTANTS.AVAILABLE_SYMBOLS.map(sym => (
            <option key={sym} value={sym}>{sym}</option>
          ))}
        </select>
        <select
          value={timeframe}
          onChange={(e) => onTimeframeChange(e.target.value as TimeframeType)}
          className="form-select"
        >
          {TRADING_CONSTANTS.TIMEFRAMES.map(tf => (
            <option key={tf} value={tf}>{tf}</option>
          ))}
        </select>
      </div>
    </div>
  );
});

// Lazy loaded components
const LazyChart = lazy(() => import('./components/AdvancedChart'));

// Main Component
export const TradingDashboard: React.FC<TradingDashboardProps> = ({ 
  initialSymbol = TRADING_CONSTANTS.DEFAULT_SYMBOL 
}) => {
  // Use custom hook for data fetching and state management
  const {
    marketData,
    symbol,
    timeframe,
    loading,
    error,
    setSymbol,
    setTimeframe
  } = useMarketData(initialSymbol);

  // Memoize market analysis
  const marketAnalysis = useMemo(() => {
    if (!marketData) return null;
    return analyzeMarketData(marketData);
  }, [marketData]);

  // Callbacks for event handlers
  const handleSymbolChange = useCallback((newSymbol: string) => {
    setSymbol(newSymbol);
  }, [setSymbol]);

  const handleTimeframeChange = useCallback((newTimeframe: TimeframeType) => {
    setTimeframe(newTimeframe);
  }, [setTimeframe]);

  // Loading state
  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500" />
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-red-500">Error: {error}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <MarketHeader
        symbol={symbol}
        timeframe={timeframe}
        onSymbolChange={handleSymbolChange}
        onTimeframeChange={handleTimeframeChange}
      />

      <main className="max-w-7xl mx-auto py-6 space-y-6">
        {marketData && (
          <>
            <Suspense fallback={<div>Loading chart...</div>}>
              <LazyChart
                data={marketData.timeframeData[timeframe]}
                timeframe={timeframe}
              />
            </Suspense>

            {marketAnalysis && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Add your analysis components here */}
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
};

export default TradingDashboard;

