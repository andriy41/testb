import axios from 'axios';
import { 
  MarketData,
  MarketSignal,
  MarketConditions,
  TimeframeData,
  RiskMetrics,
  PerformanceMetrics,
  MarketScan,
  TimeframeType
} from '../types/market';

export class TradingAnalysisService {
  private baseUrl: string;
  private apiKey: string;

  constructor(
    baseUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
    apiKey = process.env.REACT_APP_API_KEY || ''
  ) {
    this.baseUrl = baseUrl;
    this.apiKey = apiKey;
  }

  async getMarketSignal(symbol: string): Promise<MarketSignal> {
    return this.fetchWithAuth<MarketSignal>('/market-signal', { symbol });
  }

  async getMarketConditions(): Promise<MarketConditions> {
    return this.fetchWithAuth<MarketConditions>('/market-conditions');
  }

  async getTimeframeData(
    symbol: string, 
    timeframes: TimeframeType[]
  ): Promise<Record<TimeframeType, TimeframeData>> {
    return this.fetchWithAuth<Record<TimeframeType, TimeframeData>>('/timeframe-data', {
      symbol,
      timeframes: timeframes.join(',')
    });
  }

  async getRiskMetrics(symbol: string): Promise<RiskMetrics> {
    return this.fetchWithAuth<RiskMetrics>('/risk-metrics', { symbol });
  }

  async getPerformanceMetrics(): Promise<PerformanceMetrics> {
    return this.fetchWithAuth<PerformanceMetrics>('/performance-metrics');
  }

  async performMarketScan(): Promise<MarketScan> {
    return this.fetchWithAuth<MarketScan>('/market-scan');
  }

  async getMarketData(): Promise<MarketData> {
    return {
      marketSignal: await this.getMarketSignal('AAPL'),
      marketConditions: await this.getMarketConditions(),
      timeframeData: await this.getTimeframeData('AAPL', ['5m', '15m', '30m', '1h', '3h', '1d']),
      riskMetrics: await this.getRiskMetrics('AAPL'),
      performanceMetrics: await this.getPerformanceMetrics(),
      marketScan: await this.performMarketScan()
    };
  }

  private async fetchWithAuth<T>(endpoint: string, params: Record<string, any> = {}): Promise<T> {
    try {
      const response = await axios.get(`${this.baseUrl}${endpoint}`, {
        params,
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json'
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error fetching from ${endpoint}:`, error);
      throw error;
    }
  }
}

// Export singleton instance
export const tradingService = new TradingAnalysisService();
