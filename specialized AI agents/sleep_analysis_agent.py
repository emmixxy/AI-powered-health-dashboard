import numpy as np
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SleepAnalysisAgent:
    """
    Advanced sleep analysis agent with comprehensive sleep pattern analysis
    """
    
    def __init__(self):
        self.sleep_goals = {
            'optimal_duration': 7.5,  # hours
            'minimum_duration': 6.0,  # hours
            'maximum_duration': 9.0,  # hours
            'consistency_threshold': 0.8  # 80% consistency
        }
    
    def analyze_sleep_data(self, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive sleep analysis with patterns and recommendations
        """
        try:
            metrics = health_data['metrics']
            
            # Extract sleep data
            sleep_data = []
            for metric in metrics:
                sleep_entry = {
                    'date': metric['date'],
                    'sleep_hours': metric['sleep']['duration_hours'],
                    'quality_score': metric['sleep']['quality_score'],
                    'adequacy': metric['derived_metrics']['sleep_adequacy']
                }
                sleep_data.append(sleep_entry)
            
            analysis = {
                'user_id': health_data['user_id'],
                'analysis_date': datetime.now().isoformat(),
                'sleep_analysis': sleep_data,
                'sleep_patterns': self._analyze_sleep_patterns(sleep_data),
                'sleep_quality_metrics': self._calculate_sleep_quality_metrics(sleep_data),
                'recommendations': self._generate_sleep_recommendations(sleep_data),
                'sleep_insights': self._generate_sleep_insights(sleep_data)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in sleep analysis: {e}")
            return self._get_error_response()
    
    def _analyze_sleep_patterns(self, sleep_data: List[Dict]) -> Dict[str, Any]:
        """Analyze sleep patterns and trends"""
        durations = [entry['sleep_hours'] for entry in sleep_data]
        quality_scores = [entry['quality_score'] for entry in sleep_data]
        
        return {
            'average_duration': np.mean(durations),
            'duration_consistency': self._calculate_consistency(durations),
            'quality_trend': self._calculate_quality_trend(quality_scores),
            'sleep_efficiency': self._calculate_sleep_efficiency(durations),
            'optimal_sleep_days': sum(1 for d in durations if 7 <= d <= 9),
            'insufficient_sleep_days': sum(1 for d in durations if d < 6),
            'excessive_sleep_days': sum(1 for d in durations if d > 9)
        }
    
    def _calculate_sleep_quality_metrics(self, sleep_data: List[Dict]) -> Dict[str, Any]:
        """Calculate comprehensive sleep quality metrics"""
        durations = [entry['sleep_hours'] for entry in sleep_data]
        quality_scores = [entry['quality_score'] for entry in sleep_data]
        
        # Quality distribution
        quality_dist = {'excellent': 0, 'good': 0, 'fair': 0, 'poor': 0}
        for score in quality_scores:
            quality_dist[score] += 1
        
        return {
            'overall_quality_score': self._calculate_overall_quality_score(durations, quality_scores),
            'quality_distribution': quality_dist,
            'sleep_score': self._calculate_sleep_score(durations),
            'recovery_index': self._calculate_recovery_index(durations, quality_scores),
            'sleep_debt': self._calculate_sleep_debt(durations)
        }
    
    def _generate_sleep_recommendations(self, sleep_data: List[Dict]) -> List[Dict[str, Any]]:
        """Generate personalized sleep recommendations"""
        recommendations = []
        
        for entry in sleep_data:
            duration = entry['sleep_hours']
            quality = entry['quality_score']
            
            if duration < 6:
                recommendation = "Your sleep duration is insufficient. Aim for 7-9 hours nightly for optimal health and recovery."
                priority = "high"
            elif duration > 9:
                recommendation = "You're sleeping more than recommended. Consider if you're getting quality sleep or if there are underlying health issues."
                priority = "medium"
            elif quality == 'poor':
                recommendation = "Focus on sleep quality. Consider sleep hygiene practices like consistent bedtime and screen-free hour before bed."
                priority = "high"
            elif quality == 'fair':
                recommendation = "Your sleep is adequate but could be improved. Try maintaining a consistent sleep schedule."
                priority = "medium"
            else:
                recommendation = "Excellent sleep habits! Continue maintaining your current sleep routine."
                priority = "low"
            
            recommendations.append({
                'date': entry['date'],
                'recommendation': recommendation,
                'priority': priority,
                'sleep_hours': duration,
                'quality_score': quality
            })
        
        return recommendations
    
    def _generate_sleep_insights(self, sleep_data: List[Dict]) -> List[str]:
        """Generate actionable sleep insights"""
        insights = []
        durations = [entry['sleep_hours'] for entry in sleep_data]
        avg_duration = np.mean(durations)
        
        # Duration insights
        if avg_duration < 6:
            insights.append("Your average sleep duration is critically low. Chronic sleep deprivation can impact cognitive function and physical health.")
        elif avg_duration < 7:
            insights.append("You're getting less sleep than recommended. Even small increases in sleep duration can improve your daily performance.")
        elif avg_duration > 9:
            insights.append("You're sleeping more than the recommended amount. This might indicate poor sleep quality or underlying health conditions.")
        else:
            insights.append("Your sleep duration is within the healthy range. Focus on maintaining consistency in your sleep schedule.")
        
        # Consistency insights
        consistency = self._calculate_consistency(durations)
        if consistency < 0.7:
            insights.append("Your sleep schedule is inconsistent. Try to go to bed and wake up at the same time every day, even on weekends.")
        else:
            insights.append("Good sleep consistency! Maintaining a regular sleep schedule helps regulate your body's internal clock.")
        
        # Quality insights
        quality_dist = {'excellent': 0, 'good': 0, 'fair': 0, 'poor': 0}
        for entry in sleep_data:
            quality_dist[entry['quality_score']] += 1
        
        total_days = len(sleep_data)
        poor_quality_days = quality_dist['poor'] + quality_dist['fair']
        if poor_quality_days / total_days > 0.5:
            insights.append("Your sleep quality needs improvement. Consider sleep hygiene practices like limiting caffeine, creating a dark bedroom, and avoiding screens before bed.")
        
        return insights
    
    def _calculate_consistency(self, durations: List[float]) -> float:
        """Calculate sleep duration consistency"""
        if len(durations) < 2:
            return 1.0
        return 1.0 - (np.std(durations) / np.mean(durations))
    
    def _calculate_quality_trend(self, quality_scores: List[str]) -> str:
        """Calculate trend in sleep quality"""
        if len(quality_scores) < 2:
            return "stable"
        
        # Convert quality scores to numbers
        quality_nums = []
        for score in quality_scores:
            if score == 'excellent':
                quality_nums.append(4)
            elif score == 'good':
                quality_nums.append(3)
            elif score == 'fair':
                quality_nums.append(2)
            else:
                quality_nums.append(1)
        
        if quality_nums[-1] > quality_nums[0]:
            return "improving"
        elif quality_nums[-1] < quality_nums[0]:
            return "declining"
        else:
            return "stable"
    
    def _calculate_sleep_efficiency(self, durations: List[float]) -> float:
        """Calculate sleep efficiency based on duration consistency"""
        if not durations:
            return 0.0
        return min(100, (np.mean(durations) / self.sleep_goals['optimal_duration']) * 100)
    
    def _calculate_overall_quality_score(self, durations: List[float], quality_scores: List[str]) -> float:
        """Calculate overall sleep quality score (0-100)"""
        duration_score = min(100, (np.mean(durations) / self.sleep_goals['optimal_duration']) * 100)
        
        # Convert quality scores to numbers
        quality_nums = []
        for score in quality_scores:
            if score == 'excellent':
                quality_nums.append(100)
            elif score == 'good':
                quality_nums.append(75)
            elif score == 'fair':
                quality_nums.append(50)
            else:
                quality_nums.append(25)
        
        quality_score = np.mean(quality_nums)
        
        return (duration_score + quality_score) / 2
    
    def _calculate_sleep_score(self, durations: List[float]) -> float:
        """Calculate sleep score based on duration and consistency"""
        if not durations:
            return 0.0
        
        avg_duration = np.mean(durations)
        consistency = self._calculate_consistency(durations)
        
        # Duration component (0-70 points)
        if 7 <= avg_duration <= 9:
            duration_score = 70
        elif 6 <= avg_duration < 7 or 9 < avg_duration <= 10:
            duration_score = 50
        else:
            duration_score = 30
        
        # Consistency component (0-30 points)
        consistency_score = consistency * 30
        
        return duration_score + consistency_score
    
    def _calculate_recovery_index(self, durations: List[float], quality_scores: List[str]) -> float:
        """Calculate recovery index based on sleep quality and duration"""
        if not durations:
            return 0.0
        
        # Duration factor
        avg_duration = np.mean(durations)
        duration_factor = min(1.0, avg_duration / self.sleep_goals['optimal_duration'])
        
        # Quality factor
        quality_nums = []
        for score in quality_scores:
            if score == 'excellent':
                quality_nums.append(1.0)
            elif score == 'good':
                quality_nums.append(0.8)
            elif score == 'fair':
                quality_nums.append(0.6)
            else:
                quality_nums.append(0.4)
        
        quality_factor = np.mean(quality_nums)
        
        return (duration_factor + quality_factor) / 2 * 100
    
    def _calculate_sleep_debt(self, durations: List[float]) -> float:
        """Calculate accumulated sleep debt"""
        if not durations:
            return 0.0
        
        optimal_duration = self.sleep_goals['optimal_duration']
        total_debt = sum(max(0, optimal_duration - duration) for duration in durations)
        return total_debt
    
    def _get_error_response(self) -> Dict[str, Any]:
        """Return error response when analysis fails"""
        return {
            'user_id': 'unknown',
            'analysis_date': datetime.now().isoformat(),
            'error': 'Sleep analysis failed',
            'sleep_analysis': [],
            'sleep_patterns': {},
            'sleep_quality_metrics': {},
            'recommendations': [],
            'sleep_insights': ['Unable to analyze sleep data at this time.']
        }

# Example usage
if __name__ == "__main__":
    # Load normalized data
    try:
        with open('normalized_health_data.json', 'r') as f:
            health_data = json.load(f)
        
        # Initialize and run sleep agent
        sleep_agent = SleepAnalysisAgent()
        analysis = sleep_agent.analyze_sleep_data(health_data)
        
        # Save output
        with open('sleep_analysis_output.json', 'w') as f:
            json.dump(analysis, f, indent=4)
        
        print("Sleep analysis completed successfully!")
        print(f"Generated {len(analysis['sleep_analysis'])} sleep recommendations")
        
    except FileNotFoundError:
        logger.error("Normalized health data file not found. Please run data_integration.py first.")
    except Exception as e:
        logger.error(f"Error running sleep analysis: {e}")
