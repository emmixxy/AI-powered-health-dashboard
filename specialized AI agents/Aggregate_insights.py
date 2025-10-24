import json
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InsightsAggregator:
    """
    Advanced insights aggregation layer that combines outputs from all AI agents
    to provide holistic health recommendations
    """
    
    def __init__(self):
        self.correlation_weights = {
            'fitness_sleep': 0.3,
            'fitness_mood': 0.4,
            'sleep_mood': 0.3
        }
    
    def aggregate_insights(self, fitness_data: Dict, sleep_data: Dict, sentiment_data: Dict) -> Dict[str, Any]:
        """
        Aggregate insights from all agents to provide comprehensive health recommendations
        """
        try:
            aggregated_analysis = {
                'user_id': fitness_data.get('user_id', 'unknown'),
                'analysis_date': datetime.now().isoformat(),
                'holistic_insights': [],
                'correlation_analysis': {},
                'priority_recommendations': [],
                'wellness_score': 0.0,
                'trend_analysis': {},
                'action_plan': []
            }
            
            # Generate holistic insights
            aggregated_analysis['holistic_insights'] = self._generate_holistic_insights(
                fitness_data, sleep_data, sentiment_data
            )
            
            # Analyze correlations between different health metrics
            aggregated_analysis['correlation_analysis'] = self._analyze_correlations(
                fitness_data, sleep_data, sentiment_data
            )
            
            # Generate priority recommendations
            aggregated_analysis['priority_recommendations'] = self._generate_priority_recommendations(
                fitness_data, sleep_data, sentiment_data
            )
            
            # Calculate overall wellness score
            aggregated_analysis['wellness_score'] = self._calculate_wellness_score(
                fitness_data, sleep_data, sentiment_data
            )
            
            # Analyze trends
            aggregated_analysis['trend_analysis'] = self._analyze_trends(
                fitness_data, sleep_data, sentiment_data
            )
            
            # Generate action plan
            aggregated_analysis['action_plan'] = self._generate_action_plan(
                fitness_data, sleep_data, sentiment_data
            )
            
            return aggregated_analysis
            
        except Exception as e:
            logger.error(f"Error in insights aggregation: {e}")
            return self._get_error_response()
    
    def _generate_holistic_insights(self, fitness_data: Dict, sleep_data: Dict, sentiment_data: Dict) -> List[str]:
        """Generate holistic insights that consider all health dimensions"""
        insights = []
        
        # Analyze fitness and sleep correlation
        if 'performance_metrics' in fitness_data and 'sleep_patterns' in sleep_data:
            avg_steps = fitness_data['performance_metrics'].get('average_steps', 0)
            avg_sleep = sleep_data['sleep_patterns'].get('average_duration', 0)
            
            if avg_steps > 8000 and avg_sleep >= 7:
                insights.append("Excellent balance between physical activity and sleep! Your lifestyle supports optimal health.")
            elif avg_steps < 5000 and avg_sleep < 6:
                insights.append("Both your activity level and sleep duration need attention. Consider a gradual approach to improve both areas.")
            elif avg_steps > 8000 and avg_sleep < 6:
                insights.append("High activity with insufficient sleep may lead to burnout. Prioritize sleep for better recovery.")
        
        # Analyze mood and physical health correlation
        if 'summary' in sentiment_data and 'performance_metrics' in fitness_data:
            overall_sentiment = sentiment_data['summary'].get('overall_sentiment', 'neutral')
            fitness_score = fitness_data['performance_metrics'].get('fitness_score', 0)
            
            if overall_sentiment == 'positive' and fitness_score > 70:
                insights.append("Great synergy between your mental and physical well-being! This positive cycle supports overall health.")
            elif overall_sentiment == 'negative' and fitness_score < 50:
                insights.append("Your mood and physical activity both need attention. Consider starting with light exercise to boost both mood and fitness.")
        
        # Analyze sleep and mood correlation
        if 'sleep_quality_metrics' in sleep_data and 'summary' in sentiment_data:
            sleep_score = sleep_data['sleep_quality_metrics'].get('sleep_score', 0)
            overall_sentiment = sentiment_data['summary'].get('overall_sentiment', 'neutral')
            
            if sleep_score > 80 and overall_sentiment == 'positive':
                insights.append("Quality sleep is supporting your positive mood. Maintain your current sleep routine.")
            elif sleep_score < 50 and overall_sentiment == 'negative':
                insights.append("Poor sleep quality may be contributing to low mood. Focus on sleep hygiene to improve both sleep and emotional well-being.")
        
        return insights
    
    def _analyze_correlations(self, fitness_data: Dict, sleep_data: Dict, sentiment_data: Dict) -> Dict[str, Any]:
        """Analyze correlations between different health metrics"""
        correlations = {}
        
        # Fitness-Sleep correlation
        if 'performance_metrics' in fitness_data and 'sleep_patterns' in sleep_data:
            fitness_score = fitness_data['performance_metrics'].get('fitness_score', 0)
            sleep_score = sleep_data['sleep_quality_metrics'].get('sleep_score', 0)
            
            if fitness_score > 70 and sleep_score > 70:
                correlations['fitness_sleep'] = {
                    'strength': 'strong_positive',
                    'description': 'High fitness levels correlate with good sleep quality'
                }
            elif fitness_score < 50 and sleep_score < 50:
                correlations['fitness_sleep'] = {
                    'strength': 'strong_negative',
                    'description': 'Low fitness and poor sleep may be interconnected'
                }
            else:
                correlations['fitness_sleep'] = {
                    'strength': 'moderate',
                    'description': 'Some correlation between fitness and sleep patterns'
                }
        
        # Mood-Physical activity correlation
        if 'summary' in sentiment_data and 'performance_metrics' in fitness_data:
            sentiment_dist = sentiment_data['summary'].get('sentiment_distribution', {})
            positive_pct = sentiment_dist.get('positive_percentage', 0)
            fitness_score = fitness_data['performance_metrics'].get('fitness_score', 0)
            
            if positive_pct > 60 and fitness_score > 70:
                correlations['mood_fitness'] = {
                    'strength': 'strong_positive',
                    'description': 'Positive mood correlates with high fitness levels'
                }
            elif positive_pct < 40 and fitness_score < 50:
                correlations['mood_fitness'] = {
                    'strength': 'strong_negative',
                    'description': 'Low mood and low fitness may be related'
                }
        
        return correlations
    
    def _generate_priority_recommendations(self, fitness_data: Dict, sleep_data: Dict, sentiment_data: Dict) -> List[Dict[str, Any]]:
        """Generate priority-based recommendations"""
        recommendations = []
        
        # High priority: Critical health issues
        if 'sleep_patterns' in sleep_data:
            avg_sleep = sleep_data['sleep_patterns'].get('average_duration', 0)
            if avg_sleep < 6:
                recommendations.append({
                    'priority': 'high',
                    'category': 'sleep',
                    'recommendation': 'Sleep duration is critically low. This should be your top priority for health improvement.',
                    'action': 'Establish a consistent bedtime routine and aim for 7-9 hours nightly.'
                })
        
        if 'summary' in sentiment_data:
            negative_pct = sentiment_data['summary'].get('sentiment_distribution', {}).get('negative_percentage', 0)
            if negative_pct > 60:
                recommendations.append({
                    'priority': 'high',
                    'category': 'mental_health',
                    'recommendation': 'High frequency of negative emotions detected. Consider professional support.',
                    'action': 'Reach out to a mental health professional or trusted support system.'
                })
        
        # Medium priority: Improvement areas
        if 'performance_metrics' in fitness_data:
            fitness_score = fitness_data['performance_metrics'].get('fitness_score', 0)
            if fitness_score < 60:
                recommendations.append({
                    'priority': 'medium',
                    'category': 'fitness',
                    'recommendation': 'Fitness levels could be improved for better health outcomes.',
                    'action': 'Start with 30 minutes of moderate activity daily, gradually increasing intensity.'
                })
        
        # Low priority: Maintenance
        if 'performance_metrics' in fitness_data and 'sleep_patterns' in sleep_data:
            fitness_score = fitness_data['performance_metrics'].get('fitness_score', 0)
            sleep_score = sleep_data['sleep_quality_metrics'].get('sleep_score', 0)
            
            if fitness_score > 80 and sleep_score > 80:
                recommendations.append({
                    'priority': 'low',
                    'category': 'maintenance',
                    'recommendation': 'Excellent health metrics! Focus on maintaining current habits.',
                    'action': 'Continue current routine and consider adding variety to prevent plateau.'
                })
        
        return recommendations
    
    def _calculate_wellness_score(self, fitness_data: Dict, sleep_data: Dict, sentiment_data: Dict) -> float:
        """Calculate overall wellness score (0-100)"""
        scores = []
        
        # Fitness component (0-40 points)
        if 'performance_metrics' in fitness_data:
            fitness_score = fitness_data['performance_metrics'].get('fitness_score', 0)
            scores.append(fitness_score * 0.4)
        
        # Sleep component (0-35 points)
        if 'sleep_quality_metrics' in sleep_data:
            sleep_score = sleep_data['sleep_quality_metrics'].get('sleep_score', 0)
            scores.append(sleep_score * 0.35)
        
        # Mood component (0-25 points)
        if 'summary' in sentiment_data:
            positive_pct = sentiment_data['summary'].get('sentiment_distribution', {}).get('positive_percentage', 0)
            mood_score = positive_pct
            scores.append(mood_score * 0.25)
        
        return sum(scores) if scores else 0.0
    
    def _analyze_trends(self, fitness_data: Dict, sleep_data: Dict, sentiment_data: Dict) -> Dict[str, Any]:
        """Analyze overall health trends"""
        trends = {}
        
        # Fitness trends
        if 'trends' in fitness_data:
            fitness_trend = fitness_data['trends'].get('steps_trend', 'stable')
            trends['fitness'] = fitness_trend
        
        # Sleep trends
        if 'sleep_patterns' in sleep_data:
            sleep_trend = sleep_data['sleep_patterns'].get('quality_trend', 'stable')
            trends['sleep'] = sleep_trend
        
        # Mood trends
        if 'sentiment_trends' in sentiment_data:
            mood_trend = sentiment_data['sentiment_trends'].get('trend', 'stable')
            trends['mood'] = mood_trend
        
        # Overall trend assessment
        improving_trends = sum(1 for trend in trends.values() if trend == 'improving')
        declining_trends = sum(1 for trend in trends.values() if trend == 'declining')
        
        if improving_trends > declining_trends:
            trends['overall'] = 'improving'
        elif declining_trends > improving_trends:
            trends['overall'] = 'declining'
        else:
            trends['overall'] = 'stable'
        
        return trends
    
    def _generate_action_plan(self, fitness_data: Dict, sleep_data: Dict, sentiment_data: Dict) -> List[Dict[str, Any]]:
        """Generate actionable steps for health improvement"""
        action_plan = []
        
        # Week 1 actions
        action_plan.append({
            'week': 1,
            'focus': 'Foundation',
            'actions': [
                'Establish consistent sleep schedule (same bedtime and wake time)',
                'Start with 10-minute daily walks',
                'Practice 5 minutes of daily gratitude journaling'
            ]
        })
        
        # Week 2-4 actions
        action_plan.append({
            'week': '2-4',
            'focus': 'Building Habits',
            'actions': [
                'Increase daily steps to 7,000-8,000',
                'Implement sleep hygiene practices',
                'Add 10 minutes of mindfulness or meditation'
            ]
        })
        
        # Month 2+ actions
        action_plan.append({
            'week': '2+ months',
            'focus': 'Optimization',
            'actions': [
                'Aim for 10,000 daily steps',
                'Maintain 7-9 hours of quality sleep',
                'Develop stress management techniques'
            ]
        })
        
        return action_plan
    
    def _get_error_response(self) -> Dict[str, Any]:
        """Return error response when aggregation fails"""
        return {
            'user_id': 'unknown',
            'analysis_date': datetime.now().isoformat(),
            'error': 'Insights aggregation failed',
            'holistic_insights': [],
            'correlation_analysis': {},
            'priority_recommendations': [],
            'wellness_score': 0.0,
            'trend_analysis': {},
            'action_plan': []
        }

# Example usage
if __name__ == "__main__":
    try:
        # Load agent outputs
        with open('fitness_tracking_output.json', 'r') as f:
            fitness_data = json.load(f)
        
        with open('sleep_analysis_output.json', 'r') as f:
            sleep_data = json.load(f)
        
        with open('journaling_sentiment_analysis_output.json', 'r') as f:
            sentiment_data = json.load(f)
        
        # Initialize and run aggregator
        aggregator = InsightsAggregator()
        aggregated_analysis = aggregator.aggregate_insights(fitness_data, sleep_data, sentiment_data)
        
        # Save output
        with open('aggregated_insights.json', 'w') as f:
            json.dump(aggregated_analysis, f, indent=4)
        
        print("Insights aggregation completed successfully!")
        print(f"Wellness Score: {aggregated_analysis['wellness_score']:.1f}/100")
        print(f"Generated {len(aggregated_analysis['holistic_insights'])} holistic insights")
        
    except FileNotFoundError as e:
        logger.error(f"Required data file not found: {e}")
    except Exception as e:
        logger.error(f"Error running insights aggregation: {e}")
