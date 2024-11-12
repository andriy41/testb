import React from 'react';
import { Card } from ../../../../common/Card';
import { TechnicalIndicators } from '../types/market';
import { 
  TrendingUp, 
  Activity, 
  BarChart2
} from 'lucide-react';

interface TechnicalIndicatorsPanelProps {
  technicalIndicators: TechnicalIndicators;
}

export const TechnicalIndicatorsPanel: React.FC<TechnicalIndicatorsPanelProps> = ({
  technicalIndicators
}) => {
  // Helper functions for indicator analysis
  const getMaStatus = () => {
    const { sma20, sma50, sma200 } = technicalIndicators.movingAverages;
    if (sma20 > sma50 && sma50 > sma200) return { trend: 'BULLISH', color: 'text-green-600' };
    if (sma20 < sma50 && sma50 < sma200) return { trend: 'BEARISH', color: 'text-red-600' };
    return { trend: 'NEUTRAL', color: 'text-yellow-600' };
  };

  const getRsiStatus = (rsi: number) => {
    if (rsi > 70) return { status: 'OVERBOUGHT', color: 'text-red-600' };
    if (rsi < 30) return { status: 'OVERSOLD', color: 'text-green-600' };
    return { status: 'NEUTRAL', color: 'text-yellow-600' };
  };

  const getMacdStatus = () => {
    const { value, signal, histogram } = technicalIndicators.macd;
    if (value > signal && histogram > 0) return { trend: 'BULLISH', color: 'text-green-600' };
    if (value < signal && histogram < 0) return { trend: 'BEARISH', color: 'text-red-600' };
    return { trend: 'NEUTRAL', color: 'text-yellow-600' };
  };

  const getVolumeStatus = () => {
    const { current, average } = technicalIndicators.volume;
    const ratio = current / average;
    if (ratio > 1.5) return { status: 'HIGH', color: 'text-green-600' };
    if (ratio < 0.5) return { status: 'LOW', color: 'text-red-600' };
    return { status: 'NORMAL', color: 'text-yellow-600' };
  };

  return (
    <div className="grid grid-cols-12 gap-4">
      {/* Moving Averages Card */}
      <Card className="col-span-12 md:col-span-6">
        <div className="p-4">
          <h3 className="flex items-center text-lg font-bold mb-4">
            Moving Averages
          </h3>

          <div className="space-y-3">
            {Object.entries(technicalIndicators.movingAverages).map(([key, value]) => (
              <div key={key} className="flex justify-between items-center bg-slate-50 p-3 rounded-lg">
                <span className="text-gray-600 uppercase">{key}</span>
                <span className="font-medium">{(value as number).toFixed(2)}</span>
              </div>
            ))}
            <div className="flex justify-between items-center bg-slate-50 p-3 rounded-lg">
              <span>Trend</span>
              <span className={`font-medium ${getMaStatus().color}`}>
                {getMaStatus().trend}
              </span>
            </div>
          </div>
        </div>
      </Card>

      {/* Momentum Indicators Card */}
      <Card className="col-span-12 md:col-span-6">
        <div className="p-4">
          <h3 className="flex items-center text-lg font-bold mb-4">
            <Activity className="w-5 h-5 mr-2" />
            Momentum Indicators
          </h3>

          {/* RSI */}
          <div className="mb-4">
            <p className="text-sm text-gray-600 mb-2">Relative Strength Index (RSI)</p>
            <div className="bg-slate-50 p-3 rounded-lg">
              <div className="flex justify-between items-center">
                <span>Value</span>
                <span className={`font-medium ${getRsiStatus(technicalIndicators.relativeStrengthIndex).color}`}>
                  {technicalIndicators.relativeStrengthIndex.toFixed(2)}
                </span>
              </div>
              <div className="flex justify-between items-center mt-2">
                <span>Status</span>
                <span className={`font-medium ${getRsiStatus(technicalIndicators.relativeStrengthIndex).color}`}>
                  {getRsiStatus(technicalIndicators.relativeStrengthIndex).status}
                </span>
              </div>
            </div>
          </div>

          {/* MACD */}
          <div>
            <p className="text-sm text-gray-600 mb-2">MACD</p>
            <div className="bg-slate-50 p-3 rounded-lg space-y-2">
              <div className="flex justify-between items-center">
                <span>MACD Line</span>
                <span className="font-medium">{technicalIndicators.macd.value.toFixed(3)}</span>
              </div>
              <div className="flex justify-between items-center">
                <span>Signal Line</span>
                <span className="font-medium">{technicalIndicators.macd.signal.toFixed(3)}</span>
              </div>
              <div className="flex justify-between items-center">
                <span>Histogram</span>
                <span className={`font-medium ${technicalIndicators.macd.histogram > 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {technicalIndicators.macd.histogram.toFixed(3)}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span>Signal</span>
                <span className={`font-medium ${getMacdStatus().color}`}>
                  {getMacdStatus().trend}
                </span>
              </div>
            </div>
          </div>
        </div>
      </Card>

      {/* Volume Analysis Card */}
      <Card className="col-span-12">
        <div className="p-4">
          <h3 className="flex items-center text-lg font-bold mb-4">
            Volume Analysis
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-slate-50 p-3 rounded-lg">
              <p className="text-sm text-gray-600">Current Volume</p>
              <p className="text-xl font-bold">
                {technicalIndicators.volume.current.toLocaleString()}
              </p>
            </div>

            <div className="bg-slate-50 p-3 rounded-lg">
              <p className="text-sm text-gray-600">Average Volume</p>
              <p className="text-xl font-bold">
                {technicalIndicators.volume.average.toLocaleString()}
              </p>
            </div>

            <div className="bg-slate-50 p-3 rounded-lg">
              <p className="text-sm text-gray-600">Volume Status</p>
              <p className={`text-xl font-bold ${getVolumeStatus().color}`}>
                {getVolumeStatus().status}
              </p>
            </div>
          </div>
        </div>
      </Card>

      {/* ATR Card */}
      <Card className="col-span-12">
        <div className="p-4">
          <h3 className="flex items-center text-lg font-bold mb-4">
            <BarChart2 className="w-5 h-5 mr-2" />
            Volatility (ATR)
          </h3>

          <div className="bg-slate-50 p-4 rounded-lg">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Average True Range</span>
              <span className="text-xl font-bold">
                {technicalIndicators.atr.toFixed(3)}
              </span>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default TechnicalIndicatorsPanel;




