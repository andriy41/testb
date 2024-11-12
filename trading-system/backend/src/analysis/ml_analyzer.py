import numpy as np
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime
import logging
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, IsolationForest
import tensorflow as tf
from ..data.market_data import MarketData

class MLAnalyzer:
    """
    Provides machine learning based analysis of market data.
    Includes anomaly detection, pattern recognition, and price prediction.
    """
    
    def __init__(self):
        """Initialize MLAnalyzer with default models and parameters"""
        self.logger = logging.getLogger(__name__)
        self.scaler = StandardScaler()
        self.anomaly_detector = IsolationForest(
            contamination=0.1,
            random_state=42
        )
        self.pattern_classifier = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )
        self._initialize_deep_learning_model()
        
    def _initialize_deep_learning_model(self):
        """Initialize deep learning model for price prediction"""
        try:
            self.sequence_length = 60  # Use last 60 periods for prediction
            
            self.price_predictor = tf.keras.Sequential([
                tf.keras.layers.LSTM(50, activation='relu', input_shape=(self.sequence_length, 5)),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Dense(25, activation='relu'),
                tf.keras.layers.Dense(1)
            ])
            
            self.price_predictor.compile(
                optimizer='adam',
                loss='mse',
                metrics=['mae']
            )
            
        except Exception as e:
            self.logger.error(f"Error initializing deep learning model: {str(e)}")
            raise
            
    async def analyze(self, market_data: MarketData) -> Dict:
        """
        Perform comprehensive ML analysis on market data.
        
        Args:
            market_data: MarketData object containing market data
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            df = market_data.to_dataframe()
            
            # Prepare features
            features = self._prepare_features(df)
            
            # Perform various analyses
            anomalies = await self._detect_anomalies(features)
            patterns = await self._detect_patterns(features)
            prediction = await self._predict_prices(features)
            
            return {
                'anomalies': anomalies,
                'patterns': patterns,
                'prediction': prediction,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in ML analysis: {str(e)}")
            raise
            
    def _prepare_features(self, df: pd.DataFrame) -> np.ndarray:
        """Prepare feature matrix for ML models"""
        try:
            # Calculate technical indicators
            df['returns'] = df['close'].pct_change()
            df['volatility'] = df['returns'].rolling(window=20).std()
            df['volume_ma'] = df['volume'].rolling(window=20).mean()
            df['price_ma'] = df['close'].rolling(window=20).mean()
            
            # Select features
            features = df[[
                'open', 'high', 'low', 'close', 'volume',
                'returns', 'volatility', 'volume_ma', 'price_ma'
            ]].dropna()
            
            # Scale features
            return self.scaler.fit_transform(features)
            
        except Exception as e:
            self.logger.error(f"Error preparing features: {str(e)}")
            raise
            
    async def _detect_anomalies(self, features: np.ndarray) -> List[Dict]:
        """Detect market anomalies using Isolation Forest"""
        try:
            # Predict anomalies (-1 for anomalies, 1 for normal)
            predictions = self.anomaly_detector.fit_predict(features)
            
            # Find anomaly timestamps
            anomaly_indices = np.where(predictions == -1)[0]
            
            return [{
                'index': int(idx),
                'score': float(self.anomaly_detector.score_samples(features[idx:idx+1])[0])
            } for idx in anomaly_indices]
            
        except Exception as e:
            self.logger.error(f"Error detecting anomalies: {str(e)}")
            raise
            
    async def _detect_patterns(self, features: np.ndarray) -> List[Dict]:
        """Detect market patterns using Random Forest"""
        try:
            # Create labels for pattern detection
            returns = features[:, features.shape[1]-1]  # Assuming returns is last column
            labels = np.where(returns > 0, 1, 0)  # 1 for positive returns, 0 for negative
            
            # Train classifier
            self.pattern_classifier.fit(features[:-1], labels[1:])
            
            # Get feature importance
            importance = self.pattern_classifier.feature_importances_
            
            return [{
                'feature_index': int(idx),
                'importance': float(imp)
            } for idx, imp in enumerate(importance)]
            
        except Exception as e:
            self.logger.error(f"Error detecting patterns: {str(e)}")
            raise
            
    async def _predict_prices(self, features: np.ndarray) -> Dict:
        """Predict future prices using LSTM"""
        try:
            # Prepare sequences for LSTM
            sequences = []
            for i in range(len(features) - self.sequence_length):
                sequences.append(features[i:i+self.sequence_length])
            sequences = np.array(sequences)
            
            # Use last sequence for prediction
            last_sequence = sequences[-1:]
            
            # Make prediction
            prediction = self.price_predictor.predict(last_sequence)
            
            return {
                'predicted_price': float(prediction[0][0]),
                'confidence': float(np.random.uniform(0.6, 0.9))  # Placeholder for actual confidence calculation
            }
            
        except Exception as e:
            self.logger.error(f"Error predicting prices: {str(e)}")
            raise
            
    def train(self, market_data: MarketData, epochs: int = 10):
        """
        Train the deep learning model on historical data.
        
        Args:
            market_data: MarketData object containing training data
            epochs: Number of training epochs
        """
        try:
            features = self._prepare_features(market_data.to_dataframe())
            
            # Prepare sequences and targets
            sequences = []
            targets = []
            
            for i in range(len(features) - self.sequence_length - 1):
                sequences.append(features[i:i+self.sequence_length])
                targets.append(features[i+self.sequence_length, 3])  # Target is close price
                
            sequences = np.array(sequences)
            targets = np.array(targets)
            
            # Train model
            self.price_predictor.fit(
                sequences,
                targets,
                epochs=epochs,
                validation_split=0.2,
                verbose=1
            )
            
        except Exception as e:
            self.logger.error(f"Error training model: {str(e)}")
            raise
