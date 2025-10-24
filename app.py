from flask import Flask, render_template, jsonify, request
import json
import os
import sys
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Add the specialized AI agents directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'specialized AI agents'))

# Import the enhanced agents
from data_integration import HealthDataIntegrator
from fitness_tracking_agent import FitnessTrackingAgent
from sleep_analysis_agent import SleepAnalysisAgent
from journaling_sentiment_analysis_agent import JournalingSentimentAnalysisAgent
from Aggregate_insights import InsightsAggregator

class HealthDashboardAPI:
    """
    Main API class for the health dashboard system
    """
    
    def __init__(self):
        self.data_integrator = HealthDataIntegrator()
        self.fitness_agent = FitnessTrackingAgent()
        self.sleep_agent = SleepAnalysisAgent()
        self.sentiment_agent = JournalingSentimentAnalysisAgent()
        self.aggregator = InsightsAggregator()
        
        # Load or generate data
        self._load_or_generate_data()
    
    def _load_or_generate_data(self):
        """Load existing data or generate new data if not available"""
        try:
            # Try to load existing outputs
            self.fitness_data = self._load_json_file('fitness_tracking_output.json')
            self.sleep_data = self._load_json_file('sleep_analysis_output.json')
            self.sentiment_data = self._load_json_file('journaling_sentiment_analysis_output.json')
            self.insights_data = self._load_json_file('aggregated_insights.json')
            
            logger.info("Successfully loaded existing data")
            
        except FileNotFoundError:
            logger.info("Existing data not found, generating new data...")
            self._generate_new_data()
    
    def _load_json_file(self, filename):
        """Load JSON file with error handling"""
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filename} not found")
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from {filename}: {e}")
            raise
    
    def _generate_new_data(self):
        """Generate new data using the enhanced agents"""
        try:
            # Load and normalize mock data
            raw_data = self.data_integrator.load_mock_data('sundial land assignment/mock_data.json')
            normalized_data = self.data_integrator.normalize_data(raw_data)
            
            # Save normalized data
            self.data_integrator.export_normalized_data('normalized_health_data.json')
            
            # Run fitness analysis
            self.fitness_data = self.fitness_agent.analyze_fitness_data(normalized_data)
            with open('fitness_tracking_output.json', 'w') as f:
                # Convert numpy types to Python types for JSON serialization
                def convert_numpy_types(obj):
                    import numpy as np
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
                
                converted_data = convert_dict(self.fitness_data)
                json.dump(converted_data, f, indent=4)
            
            # Run sleep analysis
            self.sleep_data = self.sleep_agent.analyze_sleep_data(normalized_data)
            with open('sleep_analysis_output.json', 'w') as f:
                converted_sleep = convert_dict(self.sleep_data)
                json.dump(converted_sleep, f, indent=4)
            
            # Run sentiment analysis (using sample journal entries)
            journal_entries = [
                {"date": "2024-11-22", "entry": "I feel really anxious about the upcoming presentation. It's overwhelming and I can't stop worrying about it."},
                {"date": "2024-11-21", "entry": "Had a great day today! Felt accomplished after finishing all my tasks. I'm grateful for the support from my team."}
            ]
            self.sentiment_data = self.sentiment_agent.analyze_journaling_sentiment(journal_entries)
            with open('journaling_sentiment_analysis_output.json', 'w') as f:
                converted_sentiment = convert_dict(self.sentiment_data)
                json.dump(converted_sentiment, f, indent=4)
            
            # Aggregate insights
            self.insights_data = self.aggregator.aggregate_insights(
                self.fitness_data, self.sleep_data, self.sentiment_data
            )
            with open('aggregated_insights.json', 'w') as f:
                converted_insights = convert_dict(self.insights_data)
                json.dump(converted_insights, f, indent=4)
            
            logger.info("Successfully generated new data")
            
        except Exception as e:
            logger.error(f"Error generating new data: {e}")
            # Create fallback data
            self._create_fallback_data()
    
    def _create_fallback_data(self):
        """Create fallback data if generation fails"""
        self.fitness_data = {'error': 'Data generation failed'}
        self.sleep_data = {'error': 'Data generation failed'}
        self.sentiment_data = {'error': 'Data generation failed'}
        self.insights_data = {'error': 'Data generation failed'}

# Initialize the API
api = HealthDashboardAPI()

@app.route('/')
def dashboard():
    """Main dashboard route"""
    try:
        return render_template('dashboard.html', 
                             fitness_data=api.fitness_data, 
                             sleep_data=api.sleep_data, 
                             journal_data=api.sentiment_data, 
                             insights=api.insights_data)
    except Exception as e:
        logger.error(f"Error rendering dashboard: {e}")
        return f"Error loading dashboard: {e}", 500

@app.route('/api/health-data')
def api_health_data():
    """API endpoint for health data"""
    try:
        return jsonify({
            'fitness': api.fitness_data,
            'sleep': api.sleep_data,
            'sentiment': api.sentiment_data,
            'insights': api.insights_data,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in API endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/wellness-score')
def api_wellness_score():
    """API endpoint for wellness score"""
    try:
        if 'wellness_score' in api.insights_data:
            return jsonify({
                'wellness_score': api.insights_data['wellness_score'],
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'error': 'Wellness score not available'}), 404
    except Exception as e:
        logger.error(f"Error getting wellness score: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations')
def api_recommendations():
    """API endpoint for health recommendations"""
    try:
        recommendations = []
        
        if 'priority_recommendations' in api.insights_data:
            recommendations.extend(api.insights_data['priority_recommendations'])
        
        if 'holistic_insights' in api.insights_data:
            for insight in api.insights_data['holistic_insights']:
                recommendations.append({
                    'type': 'insight',
                    'content': insight
                })
        
        return jsonify({
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/refresh')
def api_refresh():
    """API endpoint to refresh data"""
    try:
        api._generate_new_data()
        return jsonify({
            'status': 'success',
            'message': 'Data refreshed successfully',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error refreshing data: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("Starting Health Dashboard API...")
    app.run(debug=True, host='0.0.0.0', port=5000)
