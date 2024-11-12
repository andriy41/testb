import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { ArrowUpCircle, ArrowDownCircle, Target, AlertTriangle } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ReferenceLine } from 'recharts';

const PriceTargets = () => {
  const [priceData] = useState({
    currentPrice: 155.75,
    targets: {
      entry: {
        primary: 153.25,
        secondary: 151.80,
        confidence: 85.5,
        timeframe: "Next 2-3 hours",
        indicators: ["RSI oversold", "MACD convergence", "Support level"]
      },
      exit: {
        primary: 159.50,
        secondary: 162.75,
        confidence: 78.2,
        timeframe: "1-2 days",
        indicators: ["Bollinger upper band", "Resistance level", "RSI overbought"]
      },
      stopLoss: {
        primary: 151.25,
        aggressive: 152.00,
        conservative: 150.50,
        indicators: ["Recent swing low", "Support breakdown", "Volatility range"]
      },
      riskReward: {
        ratio: "1:2.5",
        potential_gain: 3.75,
        potential_loss: 1.50,
        win_rate: 75.8
      }
    },
    priceHistory: [
      { time: '09:30', price: 154.50, target: 155.75 },
      { time: '10:00', price: 155.25, target: 155.75 },
      { time: '10:30', price: 155.75, target: 155.75 },
      { time: '11:00', price: 156.00, target: 155.75 },
      { time: '11:30', price: 155.75, target: 155.75 }
    ],
    indicatorConfidence: {
      technicalAlignment: 85,
      volumeConfirmation: 78,
      trendStrength: 82,
      overallConfidence: 82
    }
  });

  const getConfidenceColor = (confidence: number): string => {
    if (confidence >= 80) return 'text-green-500';
    if (confidence >= 70) return 'text-yellow-500';
    return 'text-red-500';
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {/* Price Chart with Targets */}
      <Card className="col-span-full">
        <CardHeader>
          <CardTitle>Price Targets Visualization</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-64">
            <LineChart data={priceData.priceHistory} className="w-full">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis domain={['auto', 'auto']} />
              <Tooltip />
              <Line type="monotone" dataKey="price" stroke="#2563eb" />
              <ReferenceLine y={priceData.targets.entry.primary} stroke="green" strokeDasharray="3 3" label="Entry" />
              <ReferenceLine y={priceData.targets.exit.primary} stroke="blue" strokeDasharray="3 3" label="Target" />
              <ReferenceLine y={priceData.targets.stopLoss.primary} stroke="red" strokeDasharray="3 3" label="Stop Loss" />
            </LineChart>
          </div>
        </CardContent>
      </Card>

      {/* Entry Points */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Target className="w-5 h-5 mr-2" />
            Entry Points
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="p-4 bg-green-50 rounded-lg">
              <div className="flex justify-between items-center mb-2">
                <span className="font-medium">Primary Entry:</span>
                <span className="text-green-600 font-bold">${priceData.targets.entry.primary}</span>
              </div>
              <div className="flex justify-between items-center mb-2">
                <span className="font-medium">Secondary Entry:</span>
                <span className="text-green-600">${priceData.targets.entry.secondary}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="font-medium">Confidence:</span>
                <span className={getConfidenceColor(priceData.targets.entry.confidence)}>
                  {priceData.targets.entry.confidence}%
                </span>
              </div>
              <div className="mt-2 text-sm text-gray-600">
                Based on: {priceData.targets.entry.indicators.join(", ")}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Exit Points */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <ArrowUpCircle className="w-5 h-5 mr-2" />
            Profit Targets
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="p-4 bg-blue-50 rounded-lg">
              <div className="flex justify-between items-center mb-2">
                <span className="font-medium">Primary Target:</span>
                <span className="text-blue-600 font-bold">${priceData.targets.exit.primary}</span>
              </div>
              <div className="flex justify-between items-center mb-2">
                <span className="font-medium">Extended Target:</span>
                <span className="text-blue-600">${priceData.targets.exit.secondary}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="font-medium">Confidence:</span>
                <span className={getConfidenceColor(priceData.targets.exit.confidence)}>
                  {priceData.targets.exit.confidence}%
                </span>
              </div>
              <div className="mt-2 text-sm text-gray-600">
                Based on: {priceData.targets.exit.indicators.join(", ")}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Stop Loss Levels */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <AlertTriangle className="w-5 h-5 mr-2" />
            Stop Loss Levels
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="p-4 bg-red-50 rounded-lg">
              <div className="flex justify-between items-center mb-2">
                <span className="font-medium">Primary Stop:</span>
                <span className="text-red-600 font-bold">${priceData.targets.stopLoss.primary}</span>
              </div>
              <div className="flex justify-between items-center mb-2">
                <span className="font-medium">Conservative:</span>
                <span className="text-red-600">${priceData.targets.stopLoss.conservative}</span>
              </div>
              <div className="flex justify-between items-center mb-2">
                <span className="font-medium">Aggressive:</span>
                <span className="text-red-600">${priceData.targets.stopLoss.aggressive}</span>
              </div>
              <div className="mt-2 text-sm text-gray-600">
                Based on: {priceData.targets.stopLoss.indicators.join(", ")}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Risk/Reward Analysis */}
      <Card>
        <CardHeader>
          <CardTitle>Risk/Reward Analysis</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 bg-slate-50 rounded-lg">
                <div className="text-sm text-gray-600">Risk/Reward Ratio</div>
                <div className="text-xl font-bold">{priceData.targets.riskReward.ratio}</div>
              </div>
              <div className="p-4 bg-slate-50 rounded-lg">
                <div className="text-sm text-gray-600">Win Rate</div>
                <div className="text-xl font-bold">{priceData.targets.riskReward.win_rate}%</div>
              </div>
              <div className="p-4 bg-slate-50 rounded-lg">
                <div className="text-sm text-gray-600">Potential Gain</div>
                <div className="text-xl font-bold text-green-600">
                  ${priceData.targets.riskReward.potential_gain}
                </div>
              </div>
              <div className="p-4 bg-slate-50 rounded-lg">
                <div className="text-sm text-gray-600">Potential Loss</div>
                <div className="text-xl font-bold text-red-600">
                  ${priceData.targets.riskReward.potential_loss}
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default PriceTargets;


