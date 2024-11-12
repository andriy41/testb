from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Optional
from datetime import datetime
import logging
from pathlib import Path
import yaml

from ..data.data_manager import DataManager
from ..analysis.market_analyzer import MarketAnalyzer
from ..analysis.technical_analyzer import TechnicalAnalyzer
from ..analysis.manipulation_detector import ManipulationDetector
from ..analysis.fakeout_detector import FakeoutDetector

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
config_path = Path(__file__).parent.parent.parent / "config" / "development.yml"
try:
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
except Exception as e:
    logger.error(f"Error loading configuration: {str(e)}")
    raise

# Initialize components
data_manager = DataManager(config['market_data'])
market_analyzer = MarketAnalyzer()
technical_analyzer = TechnicalAnalyzer()
manipulation_detector = ManipulationDetector()
fakeout_detector = FakeoutDetector()

# Create FastAPI app
app = FastAPI(
    title="Trading System API",
    description="API for market analysis and trading system",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config['api']['cors_origins'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Trading System API"}

@app.get("/api/v1/market-data/{symbol}")
async def get_market_data(
    symbol: str,
    interval: str = "1m",
    start: Optional[datetime] = None,
    end: Optional[datetime] = None
):
    """Get market data for a symbol"""
    try:
        market_data = await data_manager.get_market_data(
            symbol,
            interval,
            start,
            end
        )
        return {
            "symbol": symbol,
            "interval": interval,
            "data": market_data.to_dataframe().to_dict(orient="records")
        }
    except Exception as e:
        logger.error(f"Error getting market data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/analysis/{symbol}")
async def get_market_analysis(
    symbol: str,
    interval: str = "1m"
):
    """Get comprehensive market analysis for a symbol"""
    try:
        # Get market data
        market_data = await data_manager.get_market_data(symbol, interval)
        
        # Perform analysis
        market_analysis = await market_analyzer.analyze(market_data)
        technical_analysis = await technical_analyzer.analyze(market_data)
        manipulation_analysis = await manipulation_detector.detect(market_data)
        fakeout_analysis = await fakeout_detector.detect(market_data)
        
        return {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "market_analysis": market_analysis,
            "technical_analysis": technical_analysis,
            "manipulation_analysis": manipulation_analysis,
            "fakeout_analysis": fakeout_analysis
        }
    except Exception as e:
        logger.error(f"Error performing analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/technical/{symbol}")
async def get_technical_analysis(
    symbol: str,
    interval: str = "1m"
):
    """Get technical analysis for a symbol"""
    try:
        market_data = await data_manager.get_market_data(symbol, interval)
        analysis = await technical_analyzer.analyze(market_data)
        return {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis
        }
    except Exception as e:
        logger.error(f"Error performing technical analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/manipulation/{symbol}")
async def get_manipulation_analysis(
    symbol: str,
    interval: str = "1m"
):
    """Get manipulation analysis for a symbol"""
    try:
        market_data = await data_manager.get_market_data(symbol, interval)
        analysis = await manipulation_detector.detect(market_data)
        return {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis
        }
    except Exception as e:
        logger.error(f"Error performing manipulation analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/fakeout/{symbol}")
async def get_fakeout_analysis(
    symbol: str,
    interval: str = "1m"
):
    """Get fakeout analysis for a symbol"""
    try:
        market_data = await data_manager.get_market_data(symbol, interval)
        analysis = await fakeout_detector.detect(market_data)
        return {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis
        }
    except Exception as e:
        logger.error(f"Error performing fakeout analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
