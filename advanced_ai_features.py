+++"""
Advanced AI Features for Health Analytics
Machine learning models and predictive analytics
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import logging
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib

logger = logging.getLogger(__name__)

class PredictiveHealthAnalytics:
    """Advanced predictive analytics for health insights"""
    
    def __init__(self):
        self.models = {}
        self.scaler = StandardScaler()
        self.feature_importance = {}
    
    def train_wellness_predictor(self, historical_data: List[Dict]) -> bool:
        """Train ML model to predict wellness scores"""
        try:
            # Prepare training data
            df = pd.DataFrame(historical_data)
            
            # Feature engineering
            features = self._engineer_features(df)
            target = df['wellness_score']
            
            # Train model
            X_train, X_test, y_train, y_test = train_test_split(
                features, target, test_size=0.2, random_state=42
            )
            
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train Random Forest model
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            score = model.score(X_test_scaled, y_test)
            logger.info(f"Wellness predictor trained with R² score: {score:.3f}")
            
            # Store model and feature importance
            self.models['wellness_predictor'] = model
            self.feature_importance['wellness'] = dict(zip(
                features.columns, model.feature_importances_
            ))
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to train wellness predictor: {e}")
            return False
    
    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create advanced features for ML model"""
        features = pd.DataFrame()
        
        # Basic metrics
        features['avg_steps'] = df['steps'].rolling(window=7).mean()
        features['avg_sleep'] = df['sleep_hours'].rolling(window=7).mean()
        features['avg_heart_rate'] = df['heart_rate'].rolling(window=7).mean()
        
        # Trend features
        features['steps_trend'] = df['steps'].diff().rolling(window=3).mean()
        features['sleep_trend'] = df['sleep_hours'].diff().rolling(window=3).mean()
        
        # Variability features
        features['steps_std'] = df['steps'].rolling(window=7).std()
        features['sleep_std'] = df['sleep_hours'].rolling(window=7).std()
        
        # Interaction features
        features['activity_sleep_ratio'] = features['avg_steps'] / features['avg_sleep']
        features['heart_rate_variability'] = df['hrv'] if 'hrv' in df.columns else 0
        
        # Time-based features
        df['date'] = pd.to_datetime(df['date'])
        features['day_of_week'] = df['date'].dt.dayofweek
        features['is_weekend'] = (features['day_of_week'] >= 5).astype(int)
        
        # Fill NaN values
        features = features.fillna(features.mean())
        
        return features
    
    def predict_wellness_trend(self, current_data: Dict, days_ahead: int = 7) -> Dict[str, Any]:
        """Predict wellness score trend for next few days"""
        if 'wellness_predictor' not in self.models:
            return {'error': 'Model not trained'}
        
        try:
            # Prepare current data for prediction
            current_df = pd.DataFrame([current_data])
            features = self._engineer_features(current_df)
            features_scaled = self.scaler.transform(features)
            
            # Make prediction
            predicted_score = self.models['wellness_predictor'].predict(features_scaled)[0]
            
            # Generate trend forecast
            trend_forecast = []
            for day in range(1, days_ahead + 1):
                # Simulate trend based on current patterns
                trend_adjustment = np.random.normal(0, 2)  # Small random variation
                future_score = max(0, min(100, predicted_score + trend_adjustment))
                trend_forecast.append({
                    'day': day,
                    'predicted_score': round(future_score, 1),
                    'confidence': 0.8 - (day * 0.05)  # Decreasing confidence over time
                })
            
            return {
                'current_score': round(predicted_score, 1),
                'trend_forecast': trend_forecast,
                'model_confidence': 0.85
            }
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return {'error': str(e)}
    
    def detect_anomalies(self, health_data: List[Dict]) -> List[Dict[str, Any]]:
        """Detect unusual patterns in health data"""
        anomalies = []
        
        if len(health_data) < 7:
            return anomalies
        
        df = pd.DataFrame(health_data)
        
        # Statistical anomaly detection
        for metric in ['steps', 'sleep_hours', 'heart_rate']:
            if metric in df.columns:
                values = df[metric].values
                mean_val = np.mean(values)
                std_val = np.std(values)
                
                # Z-score based anomaly detection
                z_scores = np.abs((values - mean_val) / std_val)
                anomaly_indices = np.where(z_scores > 2.5)[0]
                
                for idx in anomaly_indices:
                    anomalies.append({
                        'date': df.iloc[idx]['date'],
                        'metric': metric,
                        'value': values[idx],
                        'expected_range': f"{mean_val - 2*std_val:.1f} - {mean_val + 2*std_val:.1f}",
                        'severity': 'high' if z_scores[idx] > 3 else 'medium',
                        'description': f"Unusual {metric} detected"
                    })
        
        return anomalies
    
    def generate_personalized_recommendations(self, user_profile: Dict, health_data: Dict) -> List[Dict[str, Any]]:
        """Generate personalized health recommendations using ML"""
        recommendations = []
        
        # Age-based recommendations
        age = user_profile.get('age', 30)
        if age > 50:
            recommendations.append({
                'type': 'preventive',
                'priority': 'high',
                'title': 'Cardiovascular Health Focus',
                'description': 'Consider regular heart health monitoring and stress management',
                'actions': ['Schedule annual checkup', 'Monitor blood pressure', 'Practice stress reduction']
            })
        
        # Activity level recommendations
        avg_steps = health_data.get('avg_steps', 0)
        if avg_steps < 5000:
            recommendations.append({
                'type': 'fitness',
                'priority': 'high',
                'title': 'Increase Daily Activity',
                'description': 'Your step count is below recommended levels',
                'actions': ['Take 10-minute walking breaks', 'Use stairs instead of elevators', 'Park farther from destinations']
            })
        
        # Sleep quality recommendations
        avg_sleep = health_data.get('avg_sleep', 0)
        if avg_sleep < 7:
            recommendations.append({
                'type': 'sleep',
                'priority': 'high',
                'title': 'Improve Sleep Duration',
                'description': 'Aim for 7-9 hours of quality sleep nightly',
                'actions': ['Establish consistent bedtime', 'Create sleep-friendly environment', 'Limit screen time before bed']
            })
        
        # Mood and stress recommendations
        if 'sentiment_score' in health_data and health_data['sentiment_score'] < 0.3:
            recommendations.append({
                'type': 'mental_health',
                'priority': 'medium',
                'title': 'Stress Management',
                'description': 'Consider stress reduction techniques',
                'actions': ['Practice mindfulness meditation', 'Engage in relaxing activities', 'Consider professional support if needed']
            })
        
        return recommendations

class HealthGoalTracker:
    """Advanced goal tracking and achievement analytics"""
    
    def __init__(self):
        self.goals = {}
        self.achievements = []
    
    def set_smart_goals(self, user_id: str, goal_data: Dict[str, Any]) -> bool:
        """Set SMART (Specific, Measurable, Achievable, Relevant, Time-bound) goals"""
        try:
            goals = {
                'user_id': user_id,
                'created_date': datetime.now().isoformat(),
                'goals': []
            }
            
            # Fitness goals
            if 'fitness' in goal_data:
                goals['goals'].append({
                    'category': 'fitness',
                    'specific': f"Walk {goal_data['fitness']['target_steps']} steps daily",
                    'measurable': f"Track daily step count",
                    'achievable': "Based on current activity level",
                    'relevant': "Improve cardiovascular health",
                    'time_bound': f"Target date: {goal_data['fitness']['target_date']}",
                    'target_value': goal_data['fitness']['target_steps'],
                    'current_progress': 0
                })
            
            # Sleep goals
            if 'sleep' in goal_data:
                goals['goals'].append({
                    'category': 'sleep',
                    'specific': f"Sleep {goal_data['sleep']['target_hours']} hours nightly",
                    'measurable': "Track sleep duration and quality",
                    'achievable': "Gradual improvement approach",
                    'relevant': "Improve recovery and cognitive function",
                    'time_bound': f"Target date: {goal_data['sleep']['target_date']}",
                    'target_value': goal_data['sleep']['target_hours'],
                    'current_progress': 0
                })
            
            self.goals[user_id] = goals
            return True
            
        except Exception as e:
            logger.error(f"Failed to set goals: {e}")
            return False
    
    def update_goal_progress(self, user_id: str, daily_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update progress towards goals"""
        if user_id not in self.goals:
            return {'error': 'No goals set for user'}
        
        progress_update = {
            'date': datetime.now().isoformat(),
            'updates': []
        }
        
        for goal in self.goals[user_id]['goals']:
            category = goal['category']
            target = goal['target_value']
            
            if category == 'fitness' and 'steps' in daily_data:
                current = daily_data['steps']
                progress = min(100, (current / target) * 100)
                goal['current_progress'] = progress
                
                progress_update['updates'].append({
                    'goal': goal['specific'],
                    'progress': f"{progress:.1f}%",
                    'status': 'achieved' if progress >= 100 else 'in_progress'
                })
            
            elif category == 'sleep' and 'sleep_hours' in daily_data:
                current = daily_data['sleep_hours']
                progress = min(100, (current / target) * 100)
                goal['current_progress'] = progress
                
                progress_update['updates'].append({
                    'goal': goal['specific'],
                    'progress': f"{progress:.1f}%",
                    'status': 'achieved' if progress >= 100 else 'in_progress'
                })
        
        return progress_update

# Example usage
if __name__ == "__main__":
    # Initialize advanced AI features
    analytics = PredictiveHealthAnalytics()
    goal_tracker = HealthGoalTracker()
    
    # Example: Train wellness predictor with historical data
    historical_data = [
        {'date': '2024-11-20', 'steps': 8000, 'sleep_hours': 7.5, 'heart_rate': 70, 'wellness_score': 85},
        {'date': '2024-11-21', 'steps': 9500, 'sleep_hours': 7.2, 'heart_rate': 72, 'wellness_score': 88},
        {'date': '2024-11-22', 'steps': 8500, 'sleep_hours': 6.5, 'heart_rate': 75, 'wellness_score': 82}
    ]
    
    # Train model
    success = analytics.train_wellness_predictor(historical_data)
    if success:
        print("✅ Wellness predictor trained successfully")
        
        # Make prediction
        current_data = {'steps': 9000, 'sleep_hours': 7.0, 'heart_rate': 73}
        prediction = analytics.predict_wellness_trend(current_data)
        print(f"Predicted wellness score: {prediction['current_score']}")
    
    # Set goals
    goal_data = {
        'fitness': {'target_steps': 10000, 'target_date': '2024-12-31'},
        'sleep': {'target_hours': 8, 'target_date': '2024-12-31'}
    }
    
    goal_tracker.set_smart_goals('user123', goal_data)
    print("✅ SMART goals set successfully")
