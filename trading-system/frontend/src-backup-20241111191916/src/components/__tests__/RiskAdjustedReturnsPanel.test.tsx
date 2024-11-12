import React from 'react';
import { render, screen } from '@testing-library/react';
import RiskAdjustedReturnsPanel from '../RiskAdjustedReturnsPanel';
import { PerformanceMetrics } from '../types/trading';

describe('RiskAdjustedReturnsPanel', () => {
  const mockRiskAdjustedReturns: PerformanceMetrics['riskAdjustedReturns'] = {
    sharpeRatio: 1.5,
    sortinoRatio: 2.1
  };

  it('renders risk metrics correctly', () => {
    render(<RiskAdjustedReturnsPanel riskAdjustedReturns={mockRiskAdjustedReturns} />);
    
    expect(screen.getByText('Sharpe Ratio')).toBeInTheDocument();
    expect(screen.getByText('1.50')).toBeInTheDocument();
    expect(screen.getByText('Sortino Ratio')).toBeInTheDocument();
    expect(screen.getByText('2.10')).toBeInTheDocument();
  });

  it('handles null/undefined props', () => {
    const { container } = render(<RiskAdjustedReturnsPanel riskAdjustedReturns={undefined} />);
    expect(container.firstChild).toBeNull();
  });
});

