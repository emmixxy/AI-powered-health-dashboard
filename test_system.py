#!/usr/bin/env python3
"""
System Test Script for Mind-Body Connection Dashboard
Tests the complete data processing pipeline
"""

import json
import sys
import os
from datetime import datetime

def test_data_integration():
    """Test the data integration layer"""
    print("🔍 Testing Data Integration Layer...")
    try:
        from data_integration import HealthDataIntegrator
        
        integrator = HealthDataIntegrator()
        raw_data = integrator.load_mock_data('sundial land assignment/mock_data.json')
        normalized_data = integrator.normalize_data(raw_data)
        
        print("✅ Data integration successful")
        print(f"   - User ID: {normalized_data['user_id']}")
        print(f"   - Metrics processed: {len(normalized_data['metrics'])}")
        return normalized_data
        
    except Exception as e:
        print(f"❌ Data integration failed: {e}")
        return None

def test_fitness_agent(health_data):
    """Test the fitness tracking agent"""
    print("\n🏃 Testing Fitness Tracking Agent...")
    try:
        sys.path.append('specialized AI agents')
        from fitness_tracking_agent import FitnessTrackingAgent
        
        agent = FitnessTrackingAgent()
        analysis = agent.analyze_fitness_data(health_data)
        
        print("✅ Fitness agent successful")
        print(f"   - Recommendations: {len(analysis['fitness_recommendations'])}")
        print(f"   - Fitness score: {analysis['performance_metrics']['fitness_score']:.1f}")
        return analysis
        
    except Exception as e:
        print(f"❌ Fitness agent failed: {e}")
        return None

def test_sleep_agent(health_data):
    """Test the sleep analysis agent"""
    print("\n😴 Testing Sleep Analysis Agent...")
    try:
        from sleep_analysis_agent import SleepAnalysisAgent
        
        agent = SleepAnalysisAgent()
        analysis = agent.analyze_sleep_data(health_data)
        
        print("✅ Sleep agent successful")
        print(f"   - Sleep entries: {len(analysis['sleep_analysis'])}")
        print(f"   - Sleep score: {analysis['sleep_quality_metrics']['sleep_score']:.1f}")
        return analysis
        
    except Exception as e:
        print(f"❌ Sleep agent failed: {e}")
        return None

def test_sentiment_agent():
    """Test the sentiment analysis agent"""
    print("\n🧠 Testing Sentiment Analysis Agent...")
    try:
        from journaling_sentiment_analysis_agent import JournalingSentimentAnalysisAgent
        
        agent = JournalingSentimentAnalysisAgent()
        journal_entries = [
            {"date": "2024-11-22", "entry": "I feel really anxious about the upcoming presentation. It's overwhelming."},
            {"date": "2024-11-21", "entry": "Had a great day today! Felt accomplished after finishing all my tasks."}
        ]
        analysis = agent.analyze_journaling_sentiment(journal_entries)
        
        print("✅ Sentiment agent successful")
        print(f"   - Entries analyzed: {len(analysis['sentiment_results'])}")
        print(f"   - Overall sentiment: {analysis['summary']['overall_sentiment']}")
        return analysis
        
    except Exception as e:
        print(f"❌ Sentiment agent failed: {e}")
        return None

def test_insights_aggregation(fitness_data, sleep_data, sentiment_data):
    """Test the insights aggregation layer"""
    print("\n🔗 Testing Insights Aggregation...")
    try:
        from Aggregate_insights import InsightsAggregator
        
        aggregator = InsightsAggregator()
        analysis = aggregator.aggregate_insights(fitness_data, sleep_data, sentiment_data)
        
        print("✅ Insights aggregation successful")
        print(f"   - Wellness score: {analysis['wellness_score']:.1f}")
        print(f"   - Holistic insights: {len(analysis['holistic_insights'])}")
        print(f"   - Priority recommendations: {len(analysis['priority_recommendations'])}")
        return analysis
        
    except Exception as e:
        print(f"❌ Insights aggregation failed: {e}")
        return None

def test_flask_app():
    """Test the Flask application"""
    print("\n🌐 Testing Flask Application...")
    try:
        from app import HealthDashboardAPI
        
        api = HealthDashboardAPI()
        print("✅ Flask app initialization successful")
        print(f"   - Fitness data loaded: {'fitness_recommendations' in api.fitness_data}")
        print(f"   - Sleep data loaded: {'sleep_analysis' in api.sleep_data}")
        print(f"   - Sentiment data loaded: {'sentiment_results' in api.sentiment_data}")
        print(f"   - Insights data loaded: {'wellness_score' in api.insights_data}")
        return True
        
    except Exception as e:
        print(f"❌ Flask app failed: {e}")
        return False

def main():
    """Run all system tests"""
    print("🚀 Starting Mind-Body Connection Dashboard System Tests")
    print("=" * 60)
    
    # Test data integration
    health_data = test_data_integration()
    if not health_data:
        print("\n❌ System test failed at data integration stage")
        return False
    
    # Test AI agents
    fitness_data = test_fitness_agent(health_data)
    sleep_data = test_sleep_agent(health_data)
    sentiment_data = test_sentiment_agent()
    
    if not all([fitness_data, sleep_data, sentiment_data]):
        print("\n❌ System test failed at AI agent stage")
        return False
    
    # Test insights aggregation
    insights_data = test_insights_aggregation(fitness_data, sleep_data, sentiment_data)
    if not insights_data:
        print("\n❌ System test failed at insights aggregation stage")
        return False
    
    # Test Flask application
    flask_success = test_flask_app()
    if not flask_success:
        print("\n❌ System test failed at Flask application stage")
        return False
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 ALL SYSTEM TESTS PASSED!")
    print("✅ Data Integration Layer")
    print("✅ Fitness Tracking Agent")
    print("✅ Sleep Analysis Agent")
    print("✅ Sentiment Analysis Agent")
    print("✅ Insights Aggregation Layer")
    print("✅ Flask Web Application")
    print("\n🚀 System is ready for deployment!")
    print("   Run 'python app.py' to start the dashboard")
    print("   Access at: http://localhost:5000")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
