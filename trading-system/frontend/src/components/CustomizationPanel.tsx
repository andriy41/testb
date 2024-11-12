import React, { useState } from 'react';

interface CustomizationPanelProps {
  selectedSymbol: string;
  selectedTimeframe: string;
}

const CustomizationPanel: React.FC<CustomizationPanelProps> = ({ 
  selectedSymbol, 
  selectedTimeframe 
}) => {
  const [layout, setLayout] = useState<string[]>([
    'chart', 
    'technical-indicators', 
    'ml-analysis', 
    'risk-management'
  ]);

  const [colorScheme, setColorScheme] = useState({
    primary: '#2c3e50',
    secondary: '#3498db',
    background: '#ecf0f1'
  });

  const handleLayoutChange = (panel: string) => {
    setLayout(prev => 
      prev.includes(panel) 
        ? prev.filter(p => p !== panel)
        : [...prev, panel]
    );
  };

  return (
    <div className="dashboard-panel">
      <h2>Customization</h2>
      
      <div>
        <h3>Current Selection</h3>
        <p>Symbol: {selectedSymbol}</p>
        <p>Timeframe: {selectedTimeframe}</p>
      </div>

      <div>
        <h3>Layout Configuration</h3>
        {['chart', 'technical-indicators', 'ml-analysis', 'risk-management', 'market-monitoring', 'performance'].map(panel => (
          <label key={panel} className="checkbox-container">
            <input 
              type="checkbox" 
              checked={layout.includes(panel)}
              onChange={() => handleLayoutChange(panel)}
            />
            {panel.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}
          </label>
        ))}
      </div>

      <div>
        <h3>Color Scheme</h3>
        <div>
          <label>
            Primary Color
            <input 
              type="color" 
              value={colorScheme.primary}
              onChange={(e) => setColorScheme(prev => ({...prev, primary: e.target.value}))}
            />
          </label>
          <label>
            Secondary Color
            <input 
              type="color" 
              value={colorScheme.secondary}
              onChange={(e) => setColorScheme(prev => ({...prev, secondary: e.target.value}))}
            />
          </label>
        </div>
      </div>
    </div>
  );
};

export default CustomizationPanel;


