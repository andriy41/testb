import React from 'react';
import { PerformanceMetrics } from '../types/market';

interface RiskAdjustedReturnsPanelProps {
  riskAdjustedReturns: PerformanceMetrics['riskAdjustedReturns'];
}

const RiskAdjustedReturnsPanel: React.FC<RiskAdjustedReturnsPanelProps> = ({ riskAdjustedReturns }) => {
  return (
    <div className="p-4">
      <h3 className="text-lg font-bold mb-4">Risk Adjusted Returns</h3>
      <div className="grid gap-4">
        <div>
          <p className="text-gray-600">Sharpe Ratio</p>
          <span className="text-xl font-bold">
            {riskAdjustedReturns.sharpeRatio.toFixed(2)}
          </span>
        </div>
        <div>
          <p className="text-gray-600">Sortino Ratio</p>
          <span className="text-xl font-bold">
            {riskAdjustedReturns.sortinoRatio.toFixed(2)}
          </span>
        </div>
        <div>
          <p className="text-gray-600">Calmar Ratio</p>
          <span className="text-xl font-bold">
            {riskAdjustedReturns.calmarRatio.toFixed(2)}
          </span>
        </div>
        <div>
          <p className="text-gray-600">Information Ratio</p>
          <span className="text-xl font-bold">
            {riskAdjustedReturns.informationRatio.toFixed(2)}
          </span>
        </div>
      </div>
    </div>
  );
};

export default RiskAdjustedReturnsPanel;


