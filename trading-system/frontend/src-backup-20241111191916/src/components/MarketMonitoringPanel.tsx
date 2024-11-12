import React from 'react';
import { MarketConditions, MarketScan } from '../types/trading';

interface MarketMonitoringPanelProps {
  marketConditions: MarketConditions;
  marketScan: MarketScan;
}

const MarketMonitoringPanel: React.FC<MarketMonitoringPanelProps> = ({ marketConditions, marketScan }) => {
  return (
    <div className="dashboard-panel">
      <h2>Market Monitoring</h2>
      <div>
        <h3>Market Sentiment</h3>
        <p>{marketConditions.marketSentiment}</p>
      </div>
      <div>
        <h3>Major Trend</h3>
        <p>{marketConditions.majorTrend}</p>
      </div>
      <div>
        <h3>Sector Breakdown</h3>
        {marketScan.sectorBreakdown.map((sector, index) => (
          <div key={index}>
            <span>{sector.sectorName}: </span>
            <span>{sector.percentage.toFixed(2)}%</span>
          </div>
        ))}
      </div>
      <div>
        <h3>Total Market Cap</h3>
        <p>${marketScan.totalMarketCap.toLocaleString()}</p>
      </div>
    </div>
  );
};

export default MarketMonitoringPanel;

