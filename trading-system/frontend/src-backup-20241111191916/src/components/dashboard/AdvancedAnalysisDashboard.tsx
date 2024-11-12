import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { ComposedChart, LineChart, Line, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ReferenceLine, Area } from 'recharts';
import { ArrowUpCircle, ArrowDownCircle, Target, AlertTriangle, TrendingUp, BarChart2, Activity } from 'lucide-react';

const AdvancedAnalysisDashboard = () => {
  const [marketData] = useState({
    currentPrice: 155.75,
    priceAction: {
      support: [151.20, 149.80, 148.50],
      resistance: [158.30, 160.50, 162.75],
      pivotPoints: {
        r3: 165.20,
        r2: 162.75,
        r1: 160.50,
        pivot: 157.80,
        s1: 155.50,
        s2: 153.20,
        s3: 151.80
      }
    },
    volumeProfile: {
      valueAreas: [
        { price: 155.50, volume: 2500000, type: 'high' },
        { price: 153.20, volume: 1800000, type: 'low' },
      ],
      keyLevels: [
        { price: 154.25, description: 'VWAP' },
        { price: 153.80, description: 'POC' }
      ]
    },
    orderFlow: {
      buyPressure: 65,
      sellPressure: 35,
      largeOrders: [
        { price: 155.20, volume: 50000, type: 'buy' },
        { price: 153.80, volume: 35000, type: 'sell' }
      ]
    },
    marketSentiment: {
      overall: 'BULLISH',
      indicators: {
        technical: 75,
        fundamental: 68,
        social: 82,
        news: 71
      },
      events: [
        { time: '10:30', type: 'NEWS', impact: 'HIGH', description: 'Economic Data Release' },
        { time: '14:00', type: 'EARNINGS', impact: 'MEDIUM', description: 'Sector Peer Report' }
      ]
    },
    riskMetrics: {
      volatility: {
        current: 18.5,
        historical: 22.3,
        implied: 20.1
      },
      correlations: {
        spy: 0.85,
        sector: 0.92,
        vix: -0.75
      },
      marketRegime: {
        current: 'RISK-ON',
        trend: 'STRENGTHENING',
        probability: 0.78
      }
    }
  });

  const [timeframeAnalysis] = useState({
    m5: { trend: 'BULLISH', strength: 85 },
    m15: { trend: 'BULLISH', strength: 82 },
    h1: { trend: 'BULLISH', strength: 78 },
    h4: { trend: 'NEUTRAL', strength: 65 },
    d1: { trend: 'BULLISH', strength: 72 }
  });

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {/* Main Chart with Volume Profile */}
      <Card className="col-span-full">
        <CardHeader>
          <CardTitle className="flex justify-between items-center">
            Advanced Price Analysis
            <div className="flex space-x-2">
              {Object.entries(timeframeAnalysis).map(([tf, data]) => (
                <span key={tf} className={`text-sm px-2 py-1 rounded ${
                  data.trend === 'BULLISH' ? 'bg-green-100 text-green-800' :
                  data.trend === 'BEARISH' ? 'bg-red-100 text-red-800' :
                  'bg-yellow-100 text-yellow-800'
                }`}>
                  {tf}: {data.trend}
                </span>
              ))}
            </div>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-96">
            <ComposedChart className="w-full" data={[/* price data */]}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis yAxisId="price" domain={['auto', 'auto']} />
              <YAxis yAxisId="volume" orientation="right" />
              <Tooltip />
              <Legend />
              <Bar dataKey="volume" fill="#8884d8" yAxisId="volume" opacity={0.3} />
              <Line type="monotone" dataKey="price" stroke="#2563eb" yAxisId="price" />
              <Area type="monotone" dataKey="volumeProfile" fill="#82ca9d" stroke="#82ca9d" />
              {marketData.priceAction.support.map((level, i) => (
                <ReferenceLine 
                  key={`support-${i}`} 
                  y={level} 
                  stroke="green" 
                  strokeDasharray="3 3" 
                  label={`Support ${i + 1}`} 
                />
              ))}
              {marketData.priceAction.resistance.map((level, i) => (
                <ReferenceLine 
                  key={`resistance-${i}`} 
                  y={level} 
                  stroke="red" 
                  strokeDasharray="3 3" 
                  label={`Resistance ${i + 1}`} 
                />
              ))}
            </ComposedChart>
          </div>
        </CardContent>
      </Card>

      {/* Order Flow Analysis */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Activity className="w-5 h-5 mr-2" />
            Order Flow Analysis
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="h-4 bg-gray-200 rounded overflow-hidden">
              <div 
                className="h-full bg-green-500" 
                style={{ width: `${marketData.orderFlow.buyPressure}%` }}
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="p-3 bg-green-50 rounded-lg">
                <div className="text-sm text-gray-600">Buy Pressure</div>
                <div className="text-xl font-bold text-green-600">
                  {marketData.orderFlow.buyPressure}%
                </div>
              </div>
              <div className="p-3 bg-red-50 rounded-lg">
                <div className="text-sm text-gray-600">Sell Pressure</div>
                <div className="text-xl font-bold text-red-600">
                  {marketData.orderFlow.sellPressure}%
                </div>
              </div>
            </div>
            <div className="space-y-2">
              {marketData.orderFlow.largeOrders.map((order, i) => (
                <div key={i} className={`p-2 rounded-lg ${
                  order.type === 'buy' ? 'bg-green-50' : 'bg-red-50'
                }`}>
                  <div className="flex justify-between">
                    <span>{order.volume.toLocaleString()} shares</span>
                    <span className={order.type === 'buy' ? 'text-green-600' : 'text-red-600'}>
                      ${order.price}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Market Sentiment */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <TrendingUp className="w-5 h-5 mr-2" />
            Market Sentiment
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="text-center p-3 bg-blue-50 rounded-lg">
              <div className="text-sm text-gray-600">Overall Sentiment</div>
              <div className="text-2xl font-bold text-blue-600">
                {marketData.marketSentiment.overall}
              </div>
            </div>
            <div className="grid grid-cols-2 gap-2">
              {Object.entries(marketData.marketSentiment.indicators).map(([key, value]) => (
                <div key={key} className="p-2 bg-slate-50 rounded-lg">
                  <div className="text-sm text-gray-600 capitalize">{key}</div>
                  <div className="text-lg font-bold">{value}%</div>
                </div>
              ))}
            </div>
            <div className="space-y-2">
              {marketData.marketSentiment.events.map((event, i) => (
                <div key={i} className="p-2 bg-yellow-50 rounded-lg">
                  <div className="flex justify-between text-sm">
                    <span>{event.time}</span>
                    <span className="font-medium">{event.type}</span>
                  </div>
                  <div className="text-sm text-gray-600">{event.description}</div>
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Risk Metrics */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <AlertTriangle className="w-5 h-5 mr-2" />
            Risk Analysis
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-2">
              <div className="p-3 bg-slate-50 rounded-lg">
                <div className="text-sm text-gray-600">Current Vol</div>
                <div className="text-xl font-bold">
                  {marketData.riskMetrics.volatility.current}%
                </div>
              </div>
              <div className="p-3 bg-slate-50 rounded-lg">
                <div className="text-sm text-gray-600">Implied Vol</div>
                <div className="text-xl font-bold">
                  {marketData.riskMetrics.volatility.implied}%
                </div>
              </div>
            </div>
            <div className="p-3 bg-blue-50 rounded-lg">
              <div className="flex justify-between items-center">
                <span className="font-medium">Market Regime</span>
                <span className="text-blue-600">{marketData.riskMetrics.marketRegime.current}</span>
              </div>
              <div className="flex justify-between items-center mt-1">
                <span className="text-sm text-gray-600">Probability</span>
                <span>{(marketData.riskMetrics.marketRegime.probability * 100).toFixed(1)}%</span>
              </div>
            </div>
            <div className="space-y-2">
              {Object.entries(marketData.riskMetrics.correlations).map(([asset, correlation]) => (
                <div key={asset} className="flex justify-between items-center p-2 bg-slate-50 rounded-lg">
                  <span className="uppercase">{asset}</span>
                  <span className={correlation > 0 ? 'text-green-600' : 'text-red-600'}>
                    {correlation.toFixed(2)}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default AdvancedAnalysisDashboard;

