import React from 'react';
import { Card } from '../components/ui/card';
import { MLAnalysis, TrendType, PatternRecognition } from '../types/market';
import { FiAlertTriangle, FiArrowUp, FiArrowDown, FiInfo } from 'react-icons/fi';

interface MLAnalysisPanelProps {
  mlAnalysis: MLAnalysis;
}

export const MLAnalysisPanel: React.FC<MLAnalysisPanelProps> = ({ mlAnalysis }) => {
  const getPredictionColor = (prediction: TrendType): string => {
    switch (prediction) {
      case 'BULLISH':
        return 'text-green-600';
      case 'BEARISH':
        return 'text-red-600';
      default:
        return 'text-yellow-600';
    }
  };

  const getConfidenceColor = (confidence: number): string => {
    if (confidence >= 0.75) return 'text-green-600';
    if (confidence >= 0.5) return 'text-yellow-600';
    return 'text-red-600';
  };

  const PredictionIcon: React.FC<{ prediction: TrendType }> = ({ prediction }) => {
    switch (prediction) {
      case 'BULLISH':
        return <FiArrowUp className="w-6 h-6 text-green-600" />;
      case 'BEARISH':
        return <FiArrowDown className="w-6 h-6 text-red-600" />;
      default:
        return <FiAlertTriangle className="w-6 h-6 text-yellow-600" />;
    }
  };

  return (
    <Card className="p-6">
      {/* Header */}
      <div className="flex items-center gap-2 mb-6">
        <FiInfo className="w-5 h-5" />
        <h3 className="text-lg font-bold">ML Analysis</h3>
      </div>

      <div className="grid grid-cols-2 gap-6">
        {/* Market Prediction */}
        <div className="col-span-2 bg-slate-50 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Market Prediction</p>
              <span
                className={`text-xl font-bold ${getPredictionColor(mlAnalysis.prediction)}`}
              >
                {mlAnalysis.prediction}
              </span>
            </div>
            <PredictionIcon prediction={mlAnalysis.prediction} />
          </div>
        </div>

        {/* Confidence Score */}
        <div className="bg-slate-50 rounded-lg p-4">
          <p className="text-sm text-gray-600 mb-1">Confidence Score</p>
          <span
            className={`text-xl font-bold ${getConfidenceColor(mlAnalysis.confidenceScore)}`}
          >
            {(mlAnalysis.confidenceScore * 100).toFixed(1)}%
          </span>
        </div>

        {/* Detected Patterns */}
        <div className="col-span-2">
          <p className="text-sm text-gray-600 mb-2">Detected Patterns</p>
          <div className="space-y-2">
            {mlAnalysis.patternRecognition.map(
              (pattern: PatternRecognition, index: number) => (
                <div
                  key={index}
                  className="flex justify-between items-center bg-slate-50 p-3 rounded-lg"
                >
                  <span className="font-medium">{pattern.pattern}</span>
                  <span
                    className={`font-bold ${getConfidenceColor(pattern.probability)}`}
                  >
                    {(pattern.probability * 100).toFixed(1)}%
                  </span>
                </div>
              )
            )}
          </div>
        </div>

        {/* Support & Resistance Levels */}
        <div className="col-span-2 grid grid-cols-2 gap-4">
          {/* Support Levels */}
          <div>
            <p className="text-sm text-gray-600 mb-2">Support Levels</p>
            {mlAnalysis.supportLevels.map((level: number, index: number) => (
              <div key={index} className="bg-green-50 p-2 rounded mb-1">
                ${level.toFixed(2)}
              </div>
            ))}
          </div>

          {/* Resistance Levels */}
          <div>
            <p className="text-sm text-gray-600 mb-2">Resistance Levels</p>
            {mlAnalysis.resistanceLevels.map((level: number, index: number) => (
              <div key={index} className="bg-red-50 p-2 rounded mb-1">
                ${level.toFixed(2)}
              </div>
            ))}
          </div>
        </div>
      </div>
    </Card>
  );
};

export default MLAnalysisPanel;


