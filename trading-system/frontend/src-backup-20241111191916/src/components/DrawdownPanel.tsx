// frontend/src/components/DrawdownPanel.tsx
import React from 'react';
import { PerformanceMetrics } from '../types/market';

interface Props {
  performanceMetrics: PerformanceMetrics;
}

const DrawdownPanel: React.FC<Props> = ({ performanceMetrics }) => {
  return (
    <div className="p-4">
      <h3 className="text-lg font-bold mb-4">Drawdown Analysis</h3>
      <div className="grid gap-4">
        <div>
          <p className="text-gray-600">Current Drawdown</p>
          <span className="text-xl font-bold text-red-500">
            {(performanceMetrics.drawdown.current * 100).toFixed(2)}%
          </span>
        </div>
        <div>
          <p className="text-gray-600">Maximum Drawdown</p>
          <span className="text-xl font-bold text-red-500">
            {(performanceMetrics.drawdown.maximum * 100).toFixed(2)}%
          </span>
        </div>
        <div>
          <p className="text-gray-600">Average Drawdown</p>
          <span className="text-xl font-bold text-red-500">
            {(performanceMetrics.drawdown.average * 100).toFixed(2)}%
          </span>
        </div>
      </div>
    </div>
  );
};

export default DrawdownPanel;

