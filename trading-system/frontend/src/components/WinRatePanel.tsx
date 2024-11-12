import React from 'react';
import { PerformanceMetrics } from '../types/trading';

interface Props {
    performanceMetrics: PerformanceMetrics;
}

const WinRatePanel: React.FC<Props> = ({ performanceMetrics }) => {
    return (
        <div className="p-4">
            <h3 className="text-lg font-bold mb-4">Win Rate Analysis</h3>
            <div className="grid gap-4">
                <div>
                    <p className="text-gray-600">Overall Win Rate</p>
                    <span className="text-xl font-bold">
                        {(performanceMetrics.winRate.overall * 100).toFixed(2)}%
                    </span>
                </div>
                {Object.entries(performanceMetrics.winRate.byTimeframe).map(([timeframe, rate]) => (
                    <div key={timeframe}>
                        <p className="text-gray-600">{timeframe}</p>
                        <span className="text-xl font-bold">
                            {(rate * 100).toFixed(2)}%
                        </span>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default WinRatePanel;


