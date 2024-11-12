import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { ArrowUpCircle, ArrowDownCircle, Target, AlertTriangle } from 'lucide-react';
import { FiDollarSign } from 'react-icons/fi';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ReferenceLine, ResponsiveContainer } from 'recharts';

interface PriceData {
  timestamp: string;
  price: number;
  volume: number;
}

interface PriceTarget {
  price: number;
  type: 'support' | 'resistance';
  confidence: number;
}

const samplePriceData: PriceData[] = [
  { timestamp: '2024-01-01', price: 150.00, volume: 1000000 },
  { timestamp: '2024-01-02', price: 152.50, volume: 1200000 },
  { timestamp: '2024-01-03', price: 151.75, volume: 900000 },
  { timestamp: '2024-01-04', price: 153.25, volume: 1100000 },
  { timestamp: '2024-01-05', price: 155.00, volume: 1300000 },
  { timestamp: '2024-01-06', price: 154.50, volume: 950000 },
  { timestamp: '2024-01-07', price: 156.00, volume: 1150000 },
];

const PriceTargetsPanel: React.FC = () => {
  const [priceTargets] = useState<PriceTarget[]>([
    { price: 150.00, type: 'support', confidence: 0.8 },
    { price: 165.00, type: 'resistance', confidence: 0.75 }
  ]);

  return (
    <Card className="w-full max-w-4xl">
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <FiDollarSign className="w-6 h-6" />
          <span>Price Targets Analysis</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Chart */}
          <div className="w-full h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={samplePriceData}
                margin={{
                  top: 5, right: 30, left: 20, bottom: 5,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="timestamp"
                  tickFormatter={(value) => new Date(value).toLocaleDateString()}
                />
                <YAxis />
                <Tooltip
                  labelFormatter={(value) => new Date(value).toLocaleDateString()}
                  formatter={(value: number) => [`$${value.toFixed(2)}`, 'Price']}
                />
                <ReferenceLine y={0} stroke="#000" />
                <Line 
                  type="monotone" 
                  dataKey="price" 
                  stroke="#8884d8" 
                  name="Price"
                  dot={false}
                />
                <Line 
                  type="monotone" 
                  dataKey="volume" 
                  stroke="#82ca9d" 
                  name="Volume"
                  dot={false}
                  yAxisId="right"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Price Targets */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {priceTargets.map((target, index) => (
              <div 
                key={index}
                className={`p-4 rounded-lg flex items-center justify-between ${
                  target.type === 'resistance' ? 'bg-red-50' : 'bg-green-50'
                }`}
              >
                <div className="flex items-center space-x-2">
                  {target.type === 'resistance' ? (
                    <ArrowUpCircle className="w-5 h-5 text-red-500" />
                  ) : (
                    <ArrowDownCircle className="w-5 h-5 text-green-500" />
                  )}
                  <div>
                    <div className="font-medium">{target.type === 'resistance' ? 'Resistance' : 'Support'}</div>
                    <div className="text-sm text-gray-500">Confidence: {(target.confidence * 100).toFixed(0)}%</div>
                  </div>
                </div>
                <div className="text-xl font-bold">
                  ${target.price.toFixed(2)}
                </div>
              </div>
            ))}
          </div>

          {/* Risk Indicators */}
          <div className="flex items-center justify-around p-4 bg-slate-50 rounded-lg">
            <div className="flex items-center space-x-2">
              <Target className="w-5 h-5 text-blue-500" />
              <span>Target Zone</span>
            </div>
            <div className="flex items-center space-x-2">
              <AlertTriangle className="w-5 h-5 text-yellow-500" />
              <span>Risk Level: Moderate</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default PriceTargetsPanel;


