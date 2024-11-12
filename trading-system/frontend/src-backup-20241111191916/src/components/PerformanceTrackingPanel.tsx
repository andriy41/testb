import React from 'react';
import { PerformanceMetrics } from '../types/market';
import { Card } from './ui/card';
import { 
  FiTrendingUp,
  FiActivity, 
  FiBarChart2, 
  FiAlertTriangle 
} from 'react-icons/fi';

interface PerformanceTrackingPanelProps {
  performanceMetrics: PerformanceMetrics;
}

export const PerformanceTrackingPanel: React.FC<PerformanceTrackingPanelProps> = ({
  performanceMetrics
}) => {
  // Format helpers
  const formatPercent = (value: number) => `${(value * 100).toFixed(2)}%`;
  const formatCurrency = (value: number) => 
    new Intl.NumberFormat('en-US', { 
      style: 'currency', 
      currency: 'USD' 
    }).format(value);

  // Style helpers
  const getValueColor = (value: number) => 
    value >= 0 ? 'text-green-600' : 'text-red-600';

  return (
    <div className="grid grid-cols-12 gap-4">
      {/* Win Rate Section */}
      <Card className="col-span-12 md:col-span-6">
        <div className="p-4">
          <h3 className="flex items-center text-lg font-bold mb-4">
            <FiActivity className="w-5 h-5 mr-2" />
            Win Rate Analysis
          </h3>

          {/* Overall Win Rate */}
          <div className="bg-slate-50 rounded-lg p-4 mb-4">
            <p className="text-sm text-gray-600">Overall Win Rate</p>
            <p className={`text-2xl font-bold ${
              getValueColor(performanceMetrics.winRate.overall)
            }`}>
              {formatPercent(performanceMetrics.winRate.overall)}
            </p>
          </div>

          {/* Win Rate by Timeframe */}
          <div className="space-y-2">
            <p className="text-sm text-gray-600">Win Rate by Timeframe</p>
            {Object.entries(performanceMetrics.winRate.byTimeframe).map(([timeframe, rate]) => (
              <div 
                key={timeframe} 
                className="flex justify-between items-center bg-white p-2 rounded-md"
              >
                <span className="font-medium">{timeframe}</span>
                <span className={getValueColor(rate as number)}>
                  {formatPercent(rate as number)}
                </span>
              </div>
            ))}
          </div>
        </div>
      </Card>

      {/* Profit/Loss Section */}
      <Card className="col-span-12 md:col-span-6">
        <div className="p-4">
          <h3 className="flex items-center text-lg font-bold mb-4">
            <FiBarChart2 className="w-5 h-5 mr-2" />
            Profit/Loss Analysis
          </h3>

          {/* Total P/L */}
          <div className="bg-slate-50 rounded-lg p-4 mb-4">
            <p className="text-sm text-gray-600">Total P/L</p>
            <p className={`text-2xl font-bold ${
              getValueColor(performanceMetrics.profitLoss.total)
            }`}>
              {formatCurrency(performanceMetrics.profitLoss.total)}
            </p>
          </div>

          {/* P/L by Strategy */}
          <div className="space-y-2">
            <p className="text-sm text-gray-600">P/L by Strategy</p>
            {Object.entries(performanceMetrics.profitLoss.byStrategy).map(([strategy, pl]) => (
              <div 
                key={strategy} 
                className="flex justify-between items-center bg-white p-2 rounded-md"
              >
                <span className="font-medium capitalize">
                  {strategy.replace('_', ' ')}
                </span>
                <span className={getValueColor(pl as number)}>
                  {formatCurrency(pl as number)}
                </span>
              </div>
            ))}
          </div>
        </div>
      </Card>

      {/* Risk Adjusted Returns */}
      <Card className="col-span-12">
        <div className="p-4">
          <h3 className="flex items-center text-lg font-bold mb-4">
            <FiTrendingUp className="w-5 h-5 mr-2" />
            Risk-Adjusted Returns
          </h3>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {/* Sharpe Ratio */}
            <div className="bg-slate-50 rounded-lg p-4">
              <p className="text-sm text-gray-600">Sharpe Ratio</p>
              <p className="text-xl font-bold">
                {performanceMetrics.riskAdjustedReturns.sharpeRatio.toFixed(2)}
              </p>
            </div>

            {/* Sortino Ratio */}
            <div className="bg-slate-50 rounded-lg p-4">
              <p className="text-sm text-gray-600">Sortino Ratio</p>
              <p className="text-xl font-bold">
                {performanceMetrics.riskAdjustedReturns.sortinoRatio.toFixed(2)}
              </p>
            </div>

            {/* Calmar Ratio */}
            <div className="bg-slate-50 rounded-lg p-4">
              <p className="text-sm text-gray-600">Calmar Ratio</p>
              <p className="text-xl font-bold">
                {performanceMetrics.riskAdjustedReturns.calmarRatio.toFixed(2)}
              </p>
            </div>

            {/* Information Ratio */}
            <div className="bg-slate-50 rounded-lg p-4">
              <p className="text-sm text-gray-600">Information Ratio</p>
              <p className="text-xl font-bold">
                {performanceMetrics.riskAdjustedReturns.informationRatio.toFixed(2)}
              </p>
            </div>
          </div>
        </div>
      </Card>

      {/* Drawdown Analysis */}
      <Card className="col-span-12">
        <div className="p-4">
          <h3 className="flex items-center text-lg font-bold mb-4">
            <FiAlertTriangle className="w-5 h-5 mr-2" />
            Drawdown Analysis
          </h3>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {/* Current Drawdown */}
            <div className="bg-slate-50 rounded-lg p-4">
              <p className="text-sm text-gray-600">Current Drawdown</p>
              <p className="text-xl font-bold text-red-600">
                {formatPercent(performanceMetrics.drawdown.current)}
              </p>
            </div>

            {/* Maximum Drawdown */}
            <div className="bg-slate-50 rounded-lg p-4">
              <p className="text-sm text-gray-600">Maximum Drawdown</p>
              <p className="text-xl font-bold text-red-600">
                {formatPercent(performanceMetrics.drawdown.maximum)}
              </p>
            </div>

            {/* Average Drawdown */}
            <div className="bg-slate-50 rounded-lg p-4">
              <p className="text-sm text-gray-600">Average Drawdown</p>
              <p className="text-xl font-bold text-red-600">
                {formatPercent(performanceMetrics.drawdown.average)}
              </p>
            </div>

            {/* Drawdown Duration */}
            <div className="bg-slate-50 rounded-lg p-4">
              <p className="text-sm text-gray-600">Duration (Days)</p>
              <p className="text-xl font-bold">
                {performanceMetrics.drawdown.duration}
              </p>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default PerformanceTrackingPanel;

