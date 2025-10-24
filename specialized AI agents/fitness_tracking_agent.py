import json
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FitnessTrackingAgent:
    """
    Advanced fitness tracking agent with comprehensive health analysis
    """
    
    def __init__(self):
        self.activity_goals = {
            'steps_daily': 10000,
            'calories_daily': 500,
            'active_minutes_daily': 30
        }
    
    def analyze_fitness_data(self, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive fitness analysis with trends and recommendations
        """
        try:
            metrics = health_data['metrics']
            
            # Calculate trends and statistics
            steps_data = [m['physical_activity']['steps'] for m in metrics]
            heart_rate_data = [m['physical_activity']['heart_rate'] for m in metrics]
            
            analysis = {
                'user_id': health_data['user_id'],
                'analysis_date': datetime.now().isoformat(),
                'fitness_recommendations': [],
                'trends': self._calculate_trends(metrics),
                'performance_metrics': self._calculate_performance_metrics(metrics),
                'health_insights': self._generate_health_insights(metrics)
            }
            
            # Generate daily recommendations
            for metric in metrics:
                recommendation = self._generate_daily_recommendation(metric)
                analysis['fitness_recommendations'].append({
                    'date': metric['date'],
                    'steps': metric['physical_activity']['steps'],
                    'heart_rate': metric['physical_activity']['heart_rate'],
                    'activity_level': metric['derived_metrics']['activity_level'],
                    'recommendation': recommendation,
                    'goal_progress': self._calculate_goal_progress(metric)
                })
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in fitness analysis: {e}")
            return self._get_error_response()
    
    def _calculate_trends(self, metrics: List[Dict]) -> Dict[str, Any]:
        """Calculate fitness trends over time"""
        steps = [m['physical_activity']['steps'] for m in metrics]
        heart_rates = [m['physical_activity']['heart_rate'] for m in metrics]
        
        return {
            'steps_trend': 'increasing' if len(steps) > 1 and steps[-1] > steps[0] else 'decreasing',
            'heart_rate_trend': 'stable' if np.std(heart_rates) < 5 else 'variable',
            'consistency_score': self._calculate_consistency_score(steps),
            'improvement_rate': self._calculate_improvement_rate(steps)
        }
    
    def _calculate_performance_metrics(self, metrics: List[Dict]) -> Dict[str, Any]:
        """Calculate key performance metrics"""
        steps = [m['physical_activity']['steps'] for m in metrics]
        heart_rates = [m['physical_activity']['heart_rate'] for m in metrics]
        
        return {
            'average_steps': np.mean(steps),
            'max_steps': np.max(steps),
            'min_steps': np.min(steps),
            'average_heart_rate': np.mean(heart_rates),
            'fitness_score': self._calculate_fitness_score(steps, heart_rates),
            'goal_achievement_rate': self._calculate_goal_achievement_rate(steps)
        }
    
    def _generate_health_insights(self, metrics: List[Dict]) -> List[str]:
        """Generate actionable health insights"""
        insights = []
        steps = [m['physical_activity']['steps'] for m in metrics]
        heart_rates = [m['physical_activity']['heart_rate'] for m in metrics]
        
        # Activity insights
        avg_steps = np.mean(steps)
        if avg_steps < 5000:
            insights.append("Your daily step count is significantly below recommended levels. Consider taking short walks throughout the day.")
        elif avg_steps < 8000:
            insights.append("You're making good progress on daily steps. Try to reach 10,000 steps for optimal health benefits.")
        else:
            insights.append("Excellent activity level! Your step count indicates good cardiovascular health.")
        
        # Heart rate insights
        avg_hr = np.mean(heart_rates)
        if avg_hr > 80:
            insights.append("Your resting heart rate is elevated. Consider stress management techniques and regular exercise.")
        elif avg_hr < 60:
            insights.append("Your heart rate indicates good cardiovascular fitness. Keep up the excellent work!")
        
        # Consistency insights
        consistency = self._calculate_consistency_score(steps)
        if consistency < 0.7:
            insights.append("Your activity levels vary significantly. Try to maintain more consistent daily exercise habits.")
        
        return insights
    
    def _generate_daily_recommendation(self, metric: Dict) -> str:
        """Generate personalized daily recommendation"""
        steps = metric['physical_activity']['steps']
        activity_level = metric['derived_metrics']['activity_level']
        
        if activity_level == 'low':
            return "Consider taking a 30-minute walk or doing light exercises to boost your activity level."
        elif activity_level == 'moderate':
            return "Good activity level! Try to add some strength training or increase your walking pace."
        else:
            return "Excellent activity level! Consider adding variety with different types of exercises."
    
    def _calculate_goal_progress(self, metric: Dict) -> Dict[str, float]:
        """Calculate progress towards fitness goals"""
        steps = metric['physical_activity']['steps']
        return {
            'steps_progress': min(100, (steps / self.activity_goals['steps_daily']) * 100),
            'goal_status': 'achieved' if steps >= self.activity_goals['steps_daily'] else 'in_progress'
        }
    
    def _calculate_consistency_score(self, steps: List[int]) -> float:
        """Calculate how consistent daily activity is"""
        if len(steps) < 2:
            return 1.0
        return 1.0 - (np.std(steps) / np.mean(steps))
    
    def _calculate_improvement_rate(self, steps: List[int]) -> float:
        """Calculate rate of improvement over time"""
        if len(steps) < 2:
            return 0.0
        return (steps[-1] - steps[0]) / steps[0] if steps[0] > 0 else 0.0
    
    def _calculate_fitness_score(self, steps: List[int], heart_rates: List[int]) -> float:
        """Calculate overall fitness score (0-100)"""
        steps_score = min(100, (np.mean(steps) / 10000) * 100)
        hr_score = max(0, 100 - (np.mean(heart_rates) - 60) * 2)
        return (steps_score + hr_score) / 2
    
    def _calculate_goal_achievement_rate(self, steps: List[int]) -> float:
        """Calculate percentage of days goals were achieved"""
        if not steps:
            return 0.0
        achieved_days = sum(1 for step in steps if step >= self.activity_goals['steps_daily'])
        return (achieved_days / len(steps)) * 100
    
    def _get_error_response(self) -> Dict[str, Any]:
        """Return error response when analysis fails"""
        return {
            'user_id': 'unknown',
            'analysis_date': datetime.now().isoformat(),
            'error': 'Analysis failed',
            'fitness_recommendations': [],
            'trends': {},
            'performance_metrics': {},
            'health_insights': ['Unable to analyze fitness data at this time.']
        }

# Example usage
if __name__ == "__main__":
    # Load normalized data
    try:
        with open('normalized_health_data.json', 'r') as f:
            health_data = json.load(f)
        
        # Initialize and run fitness agent
        fitness_agent = FitnessTrackingAgent()
        analysis = fitness_agent.analyze_fitness_data(health_data)
        
        # Save output
        with open('fitness_tracking_output.json', 'w') as f:
            # Convert numpy types to Python types for JSON serialization
            def convert_numpy_types(obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                return obj
            
            # Recursively convert numpy types
            def convert_dict(d):
                if isinstance(d, dict):
                    return {k: convert_dict(v) for k, v in d.items()}
                elif isinstance(d, list):
                    return [convert_dict(item) for item in d]
                else:
                    return convert_numpy_types(d)
            
            converted_analysis = convert_dict(analysis)
            json.dump(converted_analysis, f, indent=4)
        
        print("Fitness analysis completed successfully!")
        print(f"Generated {len(analysis['fitness_recommendations'])} daily recommendations")
        
    except FileNotFoundError:
        logger.error("Normalized health data file not found. Please run data_integration.py first.")
    except Exception as e:
        logger.error(f"Error running fitness analysis: {e}")
