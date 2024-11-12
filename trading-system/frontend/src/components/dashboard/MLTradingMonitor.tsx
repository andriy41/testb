import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ComposedChart, Bar } from 'recharts';
import { AlertTriangle, TrendingUp, Activity, BarChart2 } from 'lucide-react';

const MLTradingMonitor = () => {
  const [signals] = useState({
    timeframes: {
      '5m': { signal: 1, confidence: 0.85, agreement: 0.8 },
      '15m': { signal: 1, confidence: 0.82, agreement: 0.75 },
      '30m': { signal: 1, confidence: 0.78, agreement: 0.7 },
      '1h': { signal: 0, confidence: 0.65, agreement: 0.6 },
      '3h': { signal: 1, confidence: 0.72, agreement: 0.65 },
      '1d': { signal: 1, confidence: 0.88, agreement: 0.85 }
    },
    overall: {
      signal: 1,
      confidence: 0.82,
      strength: 0.75,
      riskLevel: 'MEDIUM'
    },
    modelPerformance: {
      rf: { accuracy: 0.85, precision: 0.83, recall: 0.82 },
      xgb: { accuracy: 0.87, precision: 0.85, recall: 0.84 },
      gb: { accuracy: 0.84, precision: 0.82, recall: 0.83 },
      svm: { accuracy: 0.82, precision: 0.81, recall: 0.80 },
      nn: { accuracy: 0.83, precision: 0.82, recall: 0.81 }
    }
  });

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {/* Overall Signal Card */}
      <Card className="col-span-full">
        <CardHeader>
          <CardTitle className="flex justify-between items-center">
            Overall Trading Signal
            <span className={`px-3 py-1 rounded-full ${
              signals.overall.signal === 1 ? 'bg-green-100 text-green-800' :
              signals.overall.signal === -1 ? 'bg-red-100 text-red-800' :
              'bg-yellow-100 text-yellow-800'
            }`}>
              {signals.overall.signal === 1 ? 'BUY' : 
               signals.overall.signal === -1 ? 'SELL' : 'NEUTRAL'}
            </span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-3 gap-4">
            <div className="p-4 bg-blue-50 rounded-lg">
              <div className="text-sm text-gray-600">Confidence</div>
              <div className="text-2xl font-bold text-blue-600">
                {(signals.overall.confidence * 100).toFixed(1)}%
              </div>
            </div>
            <div className="p-4 bg-purple-50 rounded-lg">
              <div className="text-sm text-gray-600">Signal Strength</div>
              <div className="text-2xl font-bold text-purple-600">
                {(signals.overall.strength * 100).toFixed(1)}%
              </div>
            </div>
            <div className="p-4 bg-orange-50 rounded-lg">
              <div className="text-sm text-gray-600">Risk Level</div>
              <div className="text-2xl font-bold text-orange-600">
                {signals.overall.riskLevel}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Timeframe Signals */}
      <Card className="col-span-2">
        <CardHeader>
          <CardTitle>Timeframe Analysis</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {Object.entries(signals.timeframes).map(([timeframe, data]) => (
              <div key={timeframe} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                <div className="font-medium">{timeframe}</div>
                <div className="flex items-center space-x-4">
                  <span className={`px-2 py-1 rounded ${
                    data.signal === 1 ? 'bg-green-100 text-green-800' :
                    data.signal === -1 ? 'bg-red-100 text-red-800' :
                    'bg-yellow-100 text-yellow-800'
                  }`}>
                    {data.signal === 1 ? 'BUY' : 
                     data.signal === -1 ? 'SELL' : 'NEUTRAL'}
                  </span>
                  <span className="text-blue-600">{(data.confidence * 100).toFixed(1)}%</span>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Model Performance */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <BarChart2 className="w-5 h-5 mr-2" />
            Model Performance
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {Object.entries(signals.modelPerformance).map(([model, metrics]) => (
              <div key={model} className="p-3 bg-slate-50 rounded-lg">
                <div className="flex justify-between items-center mb-2">
                  <span className="font-medium uppercase">{model}</span>
                  <span className="text-blue-600">{(metrics.accuracy * 100).toFixed(1)}%</span>
                </div>
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div>
                    <span className="text-gray-600">Precision: </span>
                    <span>{(metrics.precision * 100).toFixed(1)}%</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Recall: </span>
                    <span>{(metrics.recall * 100).toFixed(1)}%</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default MLTradingMonitor;


