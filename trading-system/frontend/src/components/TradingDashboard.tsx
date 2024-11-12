// src/components/TradingDashboard.tsx
import React, { useState, useEffect } from 'react';
import { tradingService } from '../services/TradingAnalysisService';
import { 
  MarketSignal,
  MarketConditions,
  TimeframeData,
  RiskMetrics,
  PerformanceMetrics,
  MarketScan,
  StockCandidate
} from '../types';
import AdvancedChart from './AdvancedChart';
import TechnicalIndicatorsPanel from './TechnicalIndicatorsPanel';
import MLAnalysisPanel from './MLAnalysisPanel';
import RiskManagementPanel from './RiskManagementPanel';
import MarketMonitoringPanel from './MarketMonitoringPanel';
import PerformanceTrackingPanel from './PerformanceTrackingPanel';
import CustomizationPanel from './CustomizationPanel';

const TIMEFRAMES = ['5m', '15m', '30m', '1h', '3h', 'Daily'];

interface MarketData {
  marketSignal: MarketSignal;
  marketConditions: MarketConditions;
  timeframeData: Record<string, TimeframeData>;
  riskMetrics: RiskMetrics;
  performanceMetrics: PerformanceMetrics;
  marketScan: MarketScan;
}

const TradingDashboard: React.FC = () => {
  const [selectedSymbol, setSelectedSymbol] = useState('AAPL');
  const [selectedTimeframe, setSelectedTimeframe] = useState('1h');
  const [marketData, setMarketData] = useState<MarketData | null>(null);
  const [topStocks, setTopStocks] = useState<StockCandidate[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        const [
          marketSignal,
          marketConditions,
          timeframeData,
          riskMetrics,
          performanceMetrics,
          marketScan
        ] = await Promise.all([
          tradingService.getMarketSignal(selectedSymbol, selectedTimeframe),
          tradingService.getMarketConditions(),
          tradingService.getTimeframeData(selectedSymbol, TIMEFRAMES),
          tradingService.getRiskMetrics(selectedSymbol),
          tradingService.getPerformanceMetrics(),
          tradingService.performMarketScan()
        ]);

        setMarketData({
          marketSignal,
          marketConditions,
          timeframeData,
          riskMetrics,
          performanceMetrics,
          marketScan
        });
        setTopStocks(marketScan.topStocks);
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred';
        console.error('Error fetching data:', errorMessage);
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    const intervalId = setInterval(fetchData, 300000); // Every 5 minutes

    return () => clearInterval(intervalId);
  }, [selectedSymbol, selectedTimeframe]);

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner" />
        <p>Loading market data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <p className="error-message">{error}</p>
        <button onClick={() => window.location.reload()} className="retry-button">
          Retry
        </button>
      </div>
    );
  }

  if (!marketData) {
    return <div>No data available</div>;
  }

  return (
    <div className="trading-dashboard">
      <header className="dashboard-header">
        <h1>Advanced Trading Dashboard</h1>
        <div className="controls">
          <select 
            value={selectedSymbol} 
            onChange={(e) => setSelectedSymbol(e.target.value)}
            className="symbol-select"
          >
            {topStocks.map((stock) => (
              <option key={stock.symbol} value={stock.symbol}>
                {stock.symbol}
              </option>
            ))}
          </select>
          <select 
            value={selectedTimeframe} 
            onChange={(e) => setSelectedTimeframe(e.target.value)}
            className="timeframe-select"
          >
            {TIMEFRAMES.map((tf) => (
              <option key={tf} value={tf}>{tf}</option>
            ))}
          </select>
        </div>
      </header>

      <main className="dashboard-grid">
        <AdvancedChart 
          data={marketData.timeframeData[selectedTimeframe]} 
          timeframe={selectedTimeframe}
        />
        
        <TechnicalIndicatorsPanel 
          technicalIndicators={marketData.marketSignal.technicalIndicators}
        />
        
        <MLAnalysisPanel 
          mlAnalysis={marketData.marketSignal.mlAnalysis}
        />
        
        <RiskManagementPanel 
          riskMetrics={marketData.riskMetrics}
          marketConditions={marketData.marketConditions}
        />
        
        <MarketMonitoringPanel 
          marketConditions={marketData.marketConditions}
          marketScan={marketData.marketScan}
        />
        
        <PerformanceTrackingPanel 
          performanceMetrics={marketData.performanceMetrics}
        />
        
        <CustomizationPanel 
          selectedSymbol={selectedSymbol}
          selectedTimeframe={selectedTimeframe}
        />
      </main>
    </div>
  );
};


export default React, { useState, useEffect } from 'react';
import { tradingService } from '../services/TradingAnalysisService';
import {
  MarketSignal,
  MarketConditions,
  TimeframeData,
  RiskMetrics,
  PerformanceMetrics,
  MarketScan,
  StockCandidate
} from '../types/market';
import AdvancedChart from './AdvancedChart';
import TechnicalIndicatorsPanel from './TechnicalIndicatorsPanel';
import MLAnalysisPanel from './MLAnalysisPanel';
import RiskManagementPanel from './RiskManagementPanel';
import MarketMonitoringPanel from './MarketMonitoringPanel';
import PerformanceTrackingPanel from './PerformanceTrackingPanel';
import CustomizationPanel from './CustomizationPanel';

const TIMEFRAMES: TimeframeType[] = ['5m', '15m', '30m', '1h', '3h', 'Daily'];

const TradingDashboard: React.FC = () => {
  const [marketData, setMarketData] = useState<MarketData | null>(null);
  const [selectedTimeframe, setSelectedTimeframe] = useState<TimeframeType>('Daily');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await tradingService.getMarketData();
        setMarketData(data);
      } catch (error) {
        console.error('Error fetching market data:', error);
      }
    };

    fetchData();
  }, [selectedTimeframe]);

  return (
    <div>
      <header>
        {/* Header content */}
      </header>

      <main className="max-w-7xl mx-auto py-6">
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

export default TradingDashboard;


