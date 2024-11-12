// src/components/panels/IndicatorsPanel.tsx
import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

const IndicatorsPanel = () => {
  const indicators = {
    rsi: { value: 65, status: 'NEUTRAL' },
    macd: { value: 0.35, status: 'BULLISH' },
    volume: { value: '1.5M', status: 'ABOVE_AVG' },
    trend: { value: 'UPTREND', strength: 'STRONG' }
  };

  const getStatusColor = (status: string): string => {
    switch (status) {
      case 'BULLISH':
        return 'text-green-500';
      case 'BEARISH':
        return 'text-red-500';
      case 'ABOVE_AVG':
        return 'text-blue-500';
      case 'STRONG':
        return 'text-purple-500';
      default:
        return 'text-yellow-500';
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Technical Indicators</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="font-medium">RSI (14):</span>
            <div>
              <span className="mr-2">{indicators.rsi.value}</span>
              <span className={getStatusColor(indicators.rsi.status)}>
                {indicators.rsi.status}
              </span>
            </div>
          </div>

          <div className="flex items-center justify-between">
            <span className="font-medium">MACD:</span>
            <div>
              <span className="mr-2">{indicators.macd.value}</span>
              <span className={getStatusColor(indicators.macd.status)}>
                {indicators.macd.status}
              </span>
            </div>
          </div>

          <div className="flex items-center justify-between">
            <span className="font-medium">Volume:</span>
            <div>
              <span className="mr-2">{indicators.volume.value}</span>
              <span className={getStatusColor(indicators.volume.status)}>
                {indicators.volume.status}
              </span>
            </div>
          </div>

          <div className="flex items-center justify-between">
            <span className="font-medium">Trend:</span>
            <div>
              <span className="mr-2">{indicators.trend.value}</span>
              <span className={getStatusColor(indicators.trend.strength)}>
                {indicators.trend.strength}
              </span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default IndicatorsPanel;


