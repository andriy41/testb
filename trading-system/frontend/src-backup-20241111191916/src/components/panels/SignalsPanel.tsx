import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { ArrowUpCircle, ArrowDownCircle, Activity } from 'lucide-react';

const SignalPanel = () => {
  const signals = {
    current: 'BULLISH',
    strength: 7,
    stopLoss: 98.50,
    takeProfit: 107.00,
    signals: [
      { type: 'buy', message: 'RSI oversold bounce', time: '10:15' },
      { type: 'sell', message: 'MACD bearish cross', time: '11:30' }
    ]
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Trading Signals</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="font-medium">Current Signal:</span>
            <span className="text-green-500 flex items-center">
              {signals.current}
              <ArrowUpCircle className="w-4 h-4 ml-1" />
            </span>
          </div>
          
          <div className="flex items-center justify-between">
            <span className="font-medium">Signal Strength:</span>
            <div className="flex items-center">
              <Activity className="w-4 h-4 mr-2" />
              <span>{signals.strength}/10</span>
            </div>
          </div>

          <div className="space-y-2 mt-4">
            <div className="text-sm font-medium">Recent Signals:</div>
            {signals.signals.map((signal, index) => (
              <div key={index} className="flex items-center justify-between text-sm">
                <div className="flex items-center">
                  {signal.type === 'buy' ? (
                    <ArrowUpCircle className="w-4 h-4 text-green-500 mr-2" />
                  ) : (
                    <ArrowDownCircle className="w-4 h-4 text-red-500 mr-2" />
                  )}
                  {signal.message}
                </div>
                <span className="text-gray-500">{signal.time}</span>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default SignalPanel;

