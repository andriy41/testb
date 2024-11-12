import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { ComposedChart, Line, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const PriceChart = () => {
  const [data] = useState([
    {
      time: '09:30',
      price: 100,
      volume: 1000,
      ma20: 98,
      ma50: 97,
      signal: 'none'
    },
    {
      time: '10:00',
      price: 102,
      volume: 1500,
      ma20: 99,
      ma50: 98,
      signal: 'buy'
    },
    {
      time: '10:30',
      price: 105,
      volume: 2000,
      ma20: 100,
      ma50: 98,
      signal: 'none'
    },
    {
      time: '11:00',
      price: 103,
      volume: 1800,
      ma20: 101,
      ma50: 99,
      signal: 'sell'
    },
    {
      time: '11:30',
      price: 104,
      volume: 1600,
      ma20: 102,
      ma50: 99,
      signal: 'none'
    }
  ]);

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Price Analysis</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-96">
          <ComposedChart data={data} className="w-full h-full">
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis yAxisId="price" domain={['auto', 'auto']} />
            <YAxis yAxisId="volume" orientation="right" />
            <Tooltip />
            <Legend />
            <Bar dataKey="volume" fill="#8884d8" yAxisId="volume" opacity={0.3} />
            <Line type="monotone" dataKey="price" stroke="#2563eb" yAxisId="price" />
            <Line type="monotone" dataKey="ma20" stroke="#ff7300" yAxisId="price" dot={false} />
            <Line type="monotone" dataKey="ma50" stroke="#387908" yAxisId="price" dot={false} />
          </ComposedChart>
        </div>
      </CardContent>
    </Card>
  );
};

export default PriceChart;


