from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import precision_score, recall_score, f1_score
import optuna
import joblib
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import numpy as np
import pandas as pd

@dataclass
class ModelPrediction:
    signal: int  # 1: Buy, 0: Hold, -1: Sell
    confidence: float
    probability: Dict[str, float]
    supporting_factors: List[str]
    timeframe: str

@dataclass
class EnsemblePrediction:
    final_signal: int
    confidence: float
    model_predictions: Dict[str, ModelPrediction]
    regime_alignment: float
    risk_score: float

class ModelManager:
    def __init__(self, timeframes: List[str]):
        self.timeframes = timeframes
        self.models = {}
        self.feature_importance = {}
        self.performance_metrics = {}
        self.setup_models()
        
    def setup_models(self):
        """Initialize models for each timeframe"""
        for timeframe in self.timeframes:
            self.models[timeframe] = {
                'rf': RandomForestClassifier(n_estimators=100, random_state=42),
                'xgb': XGBClassifier(n_estimators=100, random_state=42),
                'gb': GradientBoostingClassifier(n_estimators=100, random_state=42),
                'nn': MLPClassifier(hidden_layer_sizes=(100, 50), random_state=42)
            }
    
    def optimize_hyperparameters(self, X: pd.DataFrame, y: pd.Series, timeframe: str):
        """Optimize model hyperparameters using Optuna"""
        for model_name in self.models[timeframe]:
            optimization = ModelOptimizer(model_name)
            best_params = optimization.optimize(X, y)
            self.models[timeframe][model_name] = self._create_model(model_name, best_params)
    
    def train_models(self, X: pd.DataFrame, y: pd.Series, timeframe: str):
        """Train all models for a specific timeframe"""
        # Prepare cross-validation
        tscv = TimeSeriesSplit(n_splits=5)
        
        for model_name, model in self.models[timeframe].items():
            try:
                # Train model with cross-validation
                cv_scores = []
                for train_idx, val_idx in tscv.split(X):
                    X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
                    y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
                    
                    # Train model
                    model.fit(X_train, y_train)
                    
                    # Validate
                    score = self._evaluate_model(model, X_val, y_val)
                    cv_scores.append(score)
                
                # Store performance metrics
                self.performance_metrics[f"{timeframe}_{model_name}"] = {
                    'mean_cv_score': np.mean(cv_scores),
                    'std_cv_score': np.std(cv_scores)
                }
                
                # Store feature importance if available
                if hasattr(model, 'feature_importances_'):
                    self.feature_importance[f"{timeframe}_{model_name}"] = {
                        'importance': model.feature_importances_,
                        'features': X.columns
                    }
                
            except Exception as e:
                logging.error(f"Error training {model_name} for {timeframe}: {str(e)}")
                raise
    
    def predict(self, X: pd.DataFrame, timeframe: str) -> Dict[str, ModelPrediction]:
        """Generate predictions from all models"""
        predictions = {}
        
        for model_name, model in self.models[timeframe].items():
            try:
                # Get raw prediction and probability
                pred = model.predict(X)
                prob = model.predict_proba(X)
                
                # Create prediction object
                predictions[model_name] = ModelPrediction(
                    signal=pred[-1],
                    confidence=np.max(prob[-1]),
                    probability={'buy': prob[-1][1], 'sell': prob[-1][0]},
                    supporting_factors=self._get_supporting_factors(X, model_name),
                    timeframe=timeframe
                )
                
            except Exception as e:
                logging.error(f"Prediction error for {model_name}: {str(e)}")
                continue
        
        return predictions

class EnsembleManager:
    def __init__(self, voting_weights: Dict[str, float] = None):
        self.voting_weights = voting_weights or {
            'rf': 0.3,
            'xgb': 0.3,
            'gb': 0.2,
            'nn': 0.2
        }
        self.confidence_threshold = 0.6
        
    def generate_ensemble_signal(self, 
                               predictions: Dict[str, ModelPrediction],
                               market_regime: MarketRegime,
                               risk_metrics: Dict[str, float]) -> EnsemblePrediction:
        """Generate final trading signal from ensemble of models"""
        
        # Calculate weighted vote
        weighted_signal = 0
        total_confidence = 0
        
        for model_name, pred in predictions.items():
            weight = self.voting_weights[model_name]
            weighted_signal += pred.signal * weight * pred.confidence
            total_confidence += pred.confidence * weight
        
        # Normalize signal
        final_signal = self._normalize_signal(weighted_signal)
        
        # Calculate regime alignment
        regime_alignment = self._calculate_regime_alignment(final_signal, market_regime)
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(predictions, risk_metrics)
        
        return EnsemblePrediction(
            final_signal=final_signal,
            confidence=total_confidence,
            model_predictions=predictions,
            regime_alignment=regime_alignment,
            risk_score=risk_score
        )
    
    def _normalize_signal(self, weighted_signal: float) -> int:
        """Convert weighted signal to discrete signal"""
        if weighted_signal > self.confidence_threshold:
            return 1
        elif weighted_signal < -self.confidence_threshold:
            return -1
        return 0
    
    def _calculate_regime_alignment(self, signal: int, regime: MarketRegime) -> float:
        """Calculate how well the signal aligns with the current market regime"""
        if regime.trend == 'BULLISH' and signal == 1:
            return 1.0
        elif regime.trend == 'BEARISH' and signal == -1:
            return 1.0
        elif regime.trend == 'NEUTRAL':
            return 0.5
        return 0.0
    
    def _calculate_risk_score(self, 
                            predictions: Dict[str, ModelPrediction],
                            risk_metrics: Dict[str, float]) -> float:
        """Calculate risk score based on predictions and market conditions"""
        # Model agreement risk
        prediction_values = [p.signal for p in predictions.values()]
        model_agreement = len(set(prediction_values)) == 1
        
        # Confidence risk
        avg_confidence = np.mean([p.confidence for p in predictions.values()])
        
        # Market risk
        market_risk = risk_metrics.get('market_risk', 0.5)
        
        # Combined risk score
        risk_score = (
            (0.4 * (1 if model_agreement else 0)) +
            (0.3 * avg_confidence) +
            (0.3 * (1 - market_risk))
        )
        
        return risk_score

class AdaptiveSignalGenerator:
    def __init__(self, timeframes: List[str]):
        self.timeframes = timeframes
        self.model_manager = ModelManager(timeframes)
        self.ensemble_manager = EnsembleManager()
        self.signal_history = {}
        
    def generate_signals(self, 
                        data: Dict[str, pd.DataFrame],
                        market_regime: MarketRegime,
                        risk_metrics: Dict[str, float]) -> Dict[str, EnsemblePrediction]:
        """Generate trading signals for all timeframes"""
        signals = {}
        
        for timeframe in self.timeframes:
            # Get predictions from all models
            predictions = self.model_manager.predict(data[timeframe], timeframe)
            
            # Generate ensemble signal
            ensemble_prediction = self.ensemble_manager.generate_ensemble_signal(
                predictions, market_regime, risk_metrics
            )
            
            # Store signal
            signals[timeframe] = ensemble_prediction
            self.signal_history[timeframe] = ensemble_prediction
            
        return signals
    
    def analyze_signal_performance(self) -> Dict[str, Any]:
        """Analyze historical signal performance"""
        performance_metrics = {}
        
        for timeframe in self.timeframes:
            if timeframe in self.signal_history:
                performance_metrics[timeframe] = self._calculate_signal_metrics(timeframe)
        
        return performance_metrics
    
    def _calculate_signal_metrics(self, timeframe: str) -> Dict[str, float]:
        """Calculate performance metrics for signals"""
        signals = self.signal_history[timeframe]
        
        return {
            'accuracy': self._calculate_accuracy(signals),
            'profit_factor': self._calculate_profit_factor(signals),
            'win_rate': self._calculate_win_rate(signals)
        }

class ModelOptimizer:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.n_trials = 100
        
    def optimize(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, Any]:
        """Optimize model hyperparameters"""
        study = optuna.create_study(direction='maximize')
        study.optimize(
            lambda trial: self._objective(trial, X, y),
            n_trials=self.n_trials
        )
        
        return study.best_params
    
    def _objective(self, trial: optuna.Trial, X: pd.DataFrame, y: pd.Series) -> float:
        """Objective function for hyperparameter optimization"""
        params = self._get_param_space(trial)
        model = self._create_model(params)
        
        # Time series cross-validation
        tscv = TimeSeriesSplit(n_splits=5)
        scores = []
        
        for train_idx, val_idx in tscv.split(X):
            X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
            y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
            
            model.fit(X_train, y_train)
            pred = model.predict(X_val)
            scores.append(f1_score(y_val, pred))
        
        return np.mean(scores)
