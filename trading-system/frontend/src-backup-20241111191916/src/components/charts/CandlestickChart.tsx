import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { ComposedChart, Line, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const CandlestickAnalysis = () => {
  const data = [
    {
      date: '9:30',
      open: 150,
      high: 160,
      low: 145,
      close: 155,
      volume: 1000,
      ma20: 152,
      ma50: 151
    },
    {
      date: '10:00',
      open: 155,
      high: 165,
      low: 150,
      close: 160,
      volume: 1200,
      ma20: 154,
      ma50: 152
    },
    {
      date: '10:30',
      open: 160,
      high: 170,
      low: 158,
      close: 165,
      volume: 1500,
      ma20: 156,
      ma50: 153
    },
    {
      date: '11:00',
      open: 165,
      high: 168,
      low: 162,
      close: 163,
      volume: 800,
      ma20: 157,
      ma50: 154
    },
    {
      date: '11:30',
      open: 163,
      high: 167,
      low: 160,
      close: 162,
      volume: 900,
      ma20: 158,
      ma50: 155
    }
  ];

  return (
    <Card className="w-full max-w-4xl">
      <CardHeader>
        <CardTitle>Interactive Price Analysis</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-96">
          <ComposedChart data={data} className="w-full">
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis yAxisId="price" domain={['auto', 'auto']} />
            <YAxis yAxisId="volume" orientation="right" />
            <Tooltip />
            <Legend />
            <Bar dataKey="volume" fill="#8884d8" yAxisId="volume" opacity={0.3} />
            <Line type="monotone" dataKey="ma20" stroke="#ff7300" yAxisId="price" />
            <Line type="monotone" dataKey="ma50" stroke="#387908" yAxisId="price" />
            <Line 
              type="monotone" 
              dataKey="high" 
              stroke="#82ca9d" 
              yAxisId="price"
              dot={false}
            />
            <Line 
              type="monotone" 
              dataKey="low" 
              stroke="#8884d8" 
              yAxisId="price"
              dot={false}
            />
          </ComposedChart>
        </div>
      </CardContent>
    </Card>
  );
};

export default CandlestickAnalysis;

