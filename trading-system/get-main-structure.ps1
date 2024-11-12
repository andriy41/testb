$mainStructure = @"
frontend/
├── src/
│   ├── components/
│   │   ├── dashboard/
│   │   │   ├── MainDashboard.tsx
│   │   │   ├── TradingDashboard.tsx
│   │   │   ├── MLTradingMonitor.tsx
│   │   │   └── AdvancedAnalysisDashboard.tsx
│   │   ├── charts/
│   │   │   ├── CandlestickChart.tsx
│   │   │   ├── InteractivePriceChart.tsx
│   │   │   ├── TechnicalChart.tsx
│   │   │   └── VolumeChart.tsx
│   │   ├── panels/
│   │   │   ├── SignalsPanel.tsx
│   │   │   ├── IndicatorsPanel.tsx
│   │   │   ├── AdvancedIndicatorsPanel.tsx
│   │   │   ├── RiskManagementPanel.tsx
│   │   │   └── PriceTargetsPanel.tsx
│   │   └── ui/
│   │       └── card.tsx
│   └── App.tsx
├── public/
└── package.json

backend/
├── src/
│   ├── data/
│   │   ├── market_data.py
│   │   ├── data_manager.py
│   │   └── yfinance_fetcher.py
│   ├── models/
│   │   ├── ml_models.py
│   │   └── signal_generator.py
│   ├── risk/
│   │   ├── risk_manager.py
│   │   └── position_sizer.py
│   ├── execution/
│   │   ├── execution_engine.py
│   │   └── order_manager.py
│   ├── monitoring/
│   │   ├── system_monitor.py
│   │   └── market_monitor.py
│   └── analysis/
│       ├── technical_analyzer.py
│       ├── market_analyzer.py
│       ├── fakeout_detector.py
│       ├── manipulation_detector.py
│       └── ml_analyzer.py
└── config/
    └── production.yml

docker/
├── Dockerfile.backend
├── Dockerfile.frontend
└── docker-compose.yml
"@

Write-Output $mainStructure