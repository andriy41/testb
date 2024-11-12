import { MarketData, TrendType } from '../../types/market';

export const analyzeMarketData = (data: MarketData) => {
  const { marketSignal, marketConditions, timeframeData } = data;

  // Initialize variables
  let trend: TrendType = 'NEUTRAL';
  const signals: string[] = [];
  let confidence = marketSignal.mlAnalysis.confidenceScore;

  // Analyze Machine Learning prediction
  trend = marketSignal.mlAnalysis.prediction;

  // Technical indicators analysis
  const { technicalIndicators } = marketSignal;

  // RSI analysis
  const rsi = technicalIndicators.rsi;
  if (rsi < 30) {
    signals.push('RSI indicates oversold conditions');
  } else if (rsi > 70) {
    signals.push('RSI indicates overbought conditions');
  }

  // MACD analysis
  const macd = technicalIndicators.macd;
  if (macd.macd > macd.signal && macd.histogram > 0) {
    signals.push('MACD bullish crossover detected');
  } else if (macd.macd < macd.signal && macd.histogram < 0) {
    signals.push('MACD bearish crossover detected');
  }

  // Bollinger Bands analysis
  if (technicalIndicators.bollingerBands) {
    const { upperBand, lowerBand } = technicalIndicators.bollingerBands;
    const currentPrice = marketSignal.currentPrice;
    if (currentPrice > upperBand) {
      signals.push('Price is above the upper Bollinger Band (potential overbought)');
    } else if (currentPrice < lowerBand) {
      signals.push('Price is below the lower Bollinger Band (potential oversold)');
    }
  }

  // Stochastic Oscillator analysis
  if (technicalIndicators.stochastic) {
    const { k, d } = technicalIndicators.stochastic;
    if (k < 20 && d < 20) {
      signals.push('Stochastic Oscillator indicates oversold conditions');
    } else if (k > 80 && d > 80) {
      signals.push('Stochastic Oscillator indicates overbought conditions');
    }
  }

  // Fibonacci Retracement analysis
  if (technicalIndicators.fibonacciRetracement) {
    const { currentLevel } = technicalIndicators.fibonacciRetracement;
    signals.push(`Price is at Fibonacci retracement level ${currentLevel}`);
  }

  // Moving Averages analysis
  const { movingAverages } = technicalIndicators;
  if (movingAverages.ma20 && movingAverages.ma50 && movingAverages.ma200) {
    const { ma20, ma50, ma200 } = movingAverages;
    if (ma20 > ma50 && ma50 > ma200) {
      signals.push('Strong uptrend indicated by moving averages alignment');
    } else if (ma20 < ma50 && ma50 < ma200) {
      signals.push('Strong downtrend indicated by moving averages alignment');
    }
  }

  // Ichimoku Cloud analysis
  if (technicalIndicators.ichimokuCloud) {
    const { conversionLine, baseLine, leadingSpanA, leadingSpanB } = technicalIndicators.ichimokuCloud;
    const currentPrice = marketSignal.currentPrice;
    if (currentPrice > leadingSpanA && currentPrice > leadingSpanB) {
      signals.push('Price is above Ichimoku Cloud (bullish signal)');
    } else if (currentPrice < leadingSpanA && currentPrice < leadingSpanB) {
      signals.push('Price is below Ichimoku Cloud (bearish signal)');
    }
  }

  // Average Directional Index (ADX) analysis
  if (technicalIndicators.adx !== undefined) {
    if (technicalIndicators.adx > 25) {
      signals.push('Strong trend indicated by ADX');
    } else {
      signals.push('Weak trend indicated by ADX');
    }
  }

  // Standard Deviation analysis
  if (technicalIndicators.standardDeviation !== undefined) {
    if (technicalIndicators.standardDeviation > 2) {
      signals.push('High market volatility detected');
    } else {
      signals.push('Low market volatility detected');
    }
  }

  // VIDYA (Variable Index Dynamic Average) analysis
  if (technicalIndicators.vidya) {
    const { trendLine, deltaVolume } = technicalIndicators.vidya;
    if (deltaVolume > 30) {
      signals.push('Strong trend indicated by VIDYA with high delta volume');
    } else if (deltaVolume < -30) {
      signals.push('Strong downtrend indicated by VIDYA with high delta volume');
    } else {
      signals.push('Potential ranging market detected by VIDYA');
    }
  }

  // Adjust confidence based on the number of confirming signals
  confidence += signals.length * 0.02; // Increase confidence by 2% per signal

  // Ensure confidence is between 0 and 1
  confidence = Math.min(Math.max(confidence, 0), 1);

  // Return analysis results
  return {
    trend,
    signals,
    confidence,
  };
};
