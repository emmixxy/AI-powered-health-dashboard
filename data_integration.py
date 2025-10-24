"""
Data Integration Layer for Health Metrics
Handles data collection, normalization, and validation from wearable devices
"""

import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HealthDataIntegrator:
    """
    Unified data integration layer for health metrics from various sources
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.normalized_data = {}
        
    def load_mock_data(self, file_path: str) -> Dict[str, Any]:
        """
        Load and validate mock health data
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Validate data structure
            if not self._validate_data_structure(data):
                raise ValueError("Invalid data structure")
                
            logger.info(f"Successfully loaded mock data for user {data.get('user_id')}")
            return data
            
        except FileNotFoundError:
            logger.error(f"Mock data file not found: {file_path}")
            raise
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in mock data file: {file_path}")
            raise
    
    def _validate_data_structure(self, data: Dict) -> bool:
        """
        Validate that the data structure contains required fields
        """
        required_fields = ['user_id', 'metrics']
        if not all(field in data for field in required_fields):
            return False
            
        # Validate metrics structure
        for metric in data['metrics']:
            required_metric_fields = ['date', 'steps', 'heart_rate', 'sleep_hours']
            if not all(field in metric for field in required_metric_fields):
                return False
                
        return True
    
    def normalize_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize health data to a standard format
        """
        normalized = {
            'user_id': raw_data['user_id'],
            'data_source': 'mock_data',
            'last_updated': datetime.now().isoformat(),
            'metrics': []
        }
        
        for metric in raw_data['metrics']:
            normalized_metric = {
                'date': metric['date'],
                'physical_activity': {
                    'steps': int(metric['steps']),
                    'heart_rate': int(metric['heart_rate']),
                    'hrv': int(metric.get('hrv', 0))
                },
                'sleep': {
                    'duration_hours': float(metric['sleep_hours']),
                    'quality_score': self._calculate_sleep_quality(metric['sleep_hours'])
                },
                'derived_metrics': {
                    'activity_level': self._classify_activity_level(metric['steps']),
                    'heart_rate_zone': self._classify_heart_rate_zone(metric['heart_rate']),
                    'sleep_adequacy': self._assess_sleep_adequacy(metric['sleep_hours'])
                }
            }
            normalized['metrics'].append(normalized_metric)
        
        self.normalized_data = normalized
        return normalized
    
    def _calculate_sleep_quality(self, sleep_hours: float) -> str:
        """Calculate sleep quality based on duration"""
        if sleep_hours >= 7:
            return "excellent"
        elif sleep_hours >= 6:
            return "good"
        elif sleep_hours >= 5:
            return "fair"
        else:
            return "poor"
    
    def _classify_activity_level(self, steps: int) -> str:
        """Classify activity level based on steps"""
        if steps >= 10000:
            return "high"
        elif steps >= 5000:
            return "moderate"
        else:
            return "low"
    
    def _classify_heart_rate_zone(self, heart_rate: int) -> str:
        """Classify heart rate zone"""
        if heart_rate < 60:
            return "resting"
        elif heart_rate < 100:
            return "normal"
        elif heart_rate < 120:
            return "elevated"
        else:
            return "high"
    
    def _assess_sleep_adequacy(self, sleep_hours: float) -> str:
        """Assess if sleep duration is adequate"""
        if sleep_hours >= 7:
            return "adequate"
        elif sleep_hours >= 6:
            return "borderline"
        else:
            return "insufficient"
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """
        Generate a summary of all metrics
        """
        if not self.normalized_data:
            return {}
        
        metrics = self.normalized_data['metrics']
        
        summary = {
            'total_days': len(metrics),
            'average_steps': sum(m['physical_activity']['steps'] for m in metrics) / len(metrics),
            'average_heart_rate': sum(m['physical_activity']['heart_rate'] for m in metrics) / len(metrics),
            'average_sleep_hours': sum(m['sleep']['duration_hours'] for m in metrics) / len(metrics),
            'activity_distribution': self._get_activity_distribution(metrics),
            'sleep_quality_distribution': self._get_sleep_quality_distribution(metrics)
        }
        
        return summary
    
    def _get_activity_distribution(self, metrics: List[Dict]) -> Dict[str, int]:
        """Get distribution of activity levels"""
        distribution = {'high': 0, 'moderate': 0, 'low': 0}
        for metric in metrics:
            level = metric['derived_metrics']['activity_level']
            distribution[level] += 1
        return distribution
    
    def _get_sleep_quality_distribution(self, metrics: List[Dict]) -> Dict[str, int]:
        """Get distribution of sleep quality"""
        distribution = {'excellent': 0, 'good': 0, 'fair': 0, 'poor': 0}
        for metric in metrics:
            quality = metric['sleep']['quality_score']
            distribution[quality] += 1
        return distribution
    
    def export_normalized_data(self, file_path: str) -> None:
        """
        Export normalized data to JSON file
        """
        with open(file_path, 'w') as f:
            json.dump(self.normalized_data, f, indent=4)
        logger.info(f"Normalized data exported to {file_path}")

# Example usage and testing
if __name__ == "__main__":
    # Initialize the integrator
    integrator = HealthDataIntegrator()
    
    # Load and normalize mock data
    try:
        raw_data = integrator.load_mock_data('sundial land assignment/mock_data.json')
        normalized_data = integrator.normalize_data(raw_data)
        
        # Export normalized data
        integrator.export_normalized_data('normalized_health_data.json')
        
        # Generate summary
        summary = integrator.get_metrics_summary()
        print("Health Data Summary:")
        print(json.dumps(summary, indent=2))
        
    except Exception as e:
        logger.error(f"Error processing data: {e}")
