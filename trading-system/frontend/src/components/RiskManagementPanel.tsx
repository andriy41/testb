import React from 'react';
import { RiskMetrics, MarketConditions } from '../types/market';
import { Card } from './ui/card';
import { 
  FiAlertTriangle,
  FiTrendingUp,
  FiActivity,
  FiDollarSign,
  FiBarChart2,
  FiShield
} from 'react-icons/fi';

interface RiskManagementPanelProps {
  riskMetrics: RiskMetrics;
  marketConditions: MarketConditions;
}

const formatPercentage = (value: number) => `${(value * 100).toFixed(2)}%`;
const formatCurrency = (value: number) => `$${value.toFixed(2)}`;
const formatRatio = (value: number) => value.toFixed(2);

const RiskManagementPanel: React.FC<RiskManagementPanelProps> = ({
  riskMetrics,
  marketConditions
}) => {
  const getRiskLevel = (value: number, thresholds: [number, number]) => {
    const [warning, danger] = thresholds;
    if (value >= danger) return 'text-red-600';
    if (value >= warning) return 'text-yellow-600';
    return 'text-green-600';
  };

  const getVolatilityColor = (level: string) => {
    switch (level.toUpperCase()) {
      case 'HIGH': return 'text-red-600';
      case 'MEDIUM': return 'text-yellow-600';
      case 'LOW': return 'text-green-600';
      default: return 'text-gray-600';
    }
  };

  return (
    <Card className="p-6">
      {/* Header */}
      <div className="flex items-center gap-2 mb-6">
        <FiShield className="w-5 h-5" />
        <h2 className="text-xl font-bold">Risk Management</h2>
      </div>

      <div className="grid gap-6">
        {/* Position Sizing Section */}
        <section>
          <div className="flex items-center gap-2 mb-3">
            <FiDollarSign className="w-4 h-4" />
            <h3 className="text-lg font-semibold">Position Sizing</h3>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-slate-50 p-3 rounded-lg">
              <p className="text-sm text-gray-600">Position Size</p>
              <p className={`text-lg font-medium ${
                getRiskLevel(riskMetrics.currentRisk.positionSize, [0.05, 0.1])
              }`}>
                {formatPercentage(riskMetrics.currentRisk.positionSize)}
              </p>
            </div>
            <div className="bg-slate-50 p-3 rounded-lg">
              <p className="text-sm text-gray-600">Risk per Trade</p>
              <p className={`text-lg font-medium ${
                getRiskLevel(riskMetrics.currentRisk.riskPerTrade / 10000, [0.02, 0.05])
              }`}>
                {formatCurrency(riskMetrics.currentRisk.riskPerTrade)}
              </p>
            </div>
          </div>
        </section>

        {/* Entry/Exit Levels */}
        <section>
          <div className="flex items-center gap-2 mb-3">
            <FiActivity className="w-4 h-4" />
            <h3 className="text-lg font-semibold">Entry/Exit Levels</h3>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-red-50 p-3 rounded-lg">
              <p className="text-sm text-gray-600">Stop Loss</p>
              <p className="text-lg font-medium text-red-600">
                {formatCurrency(riskMetrics.stopLoss)}
              </p>
            </div>
            <div className="bg-green-50 p-3 rounded-lg">
              <p className="text-sm text-gray-600">Take Profit</p>
              <p className="text-lg font-medium text-green-600">
                {formatCurrency(riskMetrics.takeProfit)}
              </p>
            </div>
            <div className="col-span-2 bg-blue-50 p-3 rounded-lg">
              <div className="flex justify-between items-center">
                <p className="text-sm text-gray-600">Risk/Reward Ratio</p>
                <p className={`text-lg font-medium ${
                  getRiskLevel(1/riskMetrics.riskRewardRatio, [0.5, 1])
                }`}>
                  1:{formatRatio(riskMetrics.riskRewardRatio)}
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Risk Metrics */}
        <section>
          <div className="flex items-center gap-2 mb-3">
            <FiBarChart2 className="w-4 h-4" />
            <h3 className="text-lg font-semibold">Risk Metrics</h3>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-slate-50 p-3 rounded-lg">
              <p className="text-sm text-gray-600">Sharpe Ratio</p>
              <p className={`text-lg font-medium ${
                getRiskLevel(2 - riskMetrics.sharpeRatio, [1, 1.5])
              }`}>
                {formatRatio(riskMetrics.sharpeRatio)}
              </p>
            </div>
            <div className="bg-slate-50 p-3 rounded-lg">
              <p className="text-sm text-gray-600">Sortino Ratio</p>
              <p className={`text-lg font-medium ${
                getRiskLevel(2 - riskMetrics.sortinoRatio, [1, 1.5])
              }`}>
                {formatRatio(riskMetrics.sortinoRatio)}
              </p>
            </div>
            <div className="bg-slate-50 p-3 rounded-lg">
              <p className="text-sm text-gray-600">Volatility</p>
              <p className={`text-lg font-medium ${
                getVolatilityColor(marketConditions.volatility)
              }`}>
                {marketConditions.volatility}
              </p>
            </div>
            <div className="bg-slate-50 p-3 rounded-lg">
              <p className="text-sm text-gray-600">Max Drawdown</p>
              <p className={`text-lg font-medium ${
                getRiskLevel(riskMetrics.maxDrawdown, [0.1, 0.2])
              }`}>
                {formatPercentage(riskMetrics.maxDrawdown)}
              </p>
            </div>
          </div>
        </section>

        {/* Market Warnings */}
        {(marketConditions.manipulationIndicators.unusualVolume || 
          marketConditions.manipulationIndicators.priceManipulation) && (
          <section className="bg-yellow-50 p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-3">
              <FiAlertTriangle className="w-4 h-4 text-yellow-600" />
              <h3 className="text-lg font-semibold text-yellow-800">Market Warnings</h3>
            </div>
            <div className="space-y-2">
              {marketConditions.manipulationIndicators.unusualVolume && (
                <div className="flex items-center gap-2 text-yellow-700">
                  <span>⚠️</span>
                  <p>Unusual volume detected - exercise caution</p>
                </div>
              )}
              {marketConditions.manipulationIndicators.priceManipulation && (
                <div className="flex items-center gap-2 text-red-700">
                  <span>⚠️</span>
                  <p>Potential price manipulation detected</p>
                </div>
              )}
            </div>
          </section>
        )}
      </div>
    </Card>
  );
};

export default RiskManagementPanel;


