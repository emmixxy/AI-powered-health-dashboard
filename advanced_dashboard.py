"""
Advanced Dashboard Features
Real-time updates, notifications, and interactive features
"""

import json
import asyncio
import websockets
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
from flask import Flask, render_template, jsonify, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room
import threading
import time

logger = logging.getLogger(__name__)

class RealTimeHealthMonitor:
    """Real-time health monitoring and notifications"""
    
    def __init__(self, socketio):
        self.socketio = socketio
        self.connected_users = {}
        self.health_alerts = {}
        self.monitoring_active = False
    
    def start_monitoring(self, user_id: str):
        """Start real-time monitoring for a user"""
        self.connected_users[user_id] = {
            'connected_at': datetime.now(),
            'last_heartbeat': datetime.now(),
            'monitoring_active': True
        }
        
        # Start background monitoring thread
        if not self.monitoring_active:
            self.monitoring_active = True
            threading.Thread(target=self._monitor_health_data, daemon=True).start()
        
        logger.info(f"Started monitoring for user: {user_id}")
    
    def stop_monitoring(self, user_id: str):
        """Stop monitoring for a user"""
        if user_id in self.connected_users:
            del self.connected_users[user_id]
            logger.info(f"Stopped monitoring for user: {user_id}")
    
    def _monitor_health_data(self):
        """Background thread for health monitoring"""
        while self.monitoring_active:
            try:
                for user_id in list(self.connected_users.keys()):
                    # Simulate health data monitoring
                    health_data = self._get_latest_health_data(user_id)
                    
                    # Check for alerts
                    alerts = self._check_health_alerts(user_id, health_data)
                    
                    if alerts:
                        self._send_health_alert(user_id, alerts)
                    
                    # Send real-time update
                    self._send_health_update(user_id, health_data)
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                time.sleep(5)
    
    def _get_latest_health_data(self, user_id: str) -> Dict[str, Any]:
        """Get latest health data for user"""
        # In production, this would fetch from database
        return {
            'timestamp': datetime.now().isoformat(),
            'steps': 8500,
            'heart_rate': 75,
            'sleep_hours': 6.5,
            'wellness_score': 85.1
        }
    
    def _check_health_alerts(self, user_id: str, health_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for health alerts and anomalies"""
        alerts = []
        
        # Heart rate alert
        if health_data.get('heart_rate', 0) > 100:
            alerts.append({
                'type': 'heart_rate_high',
                'severity': 'medium',
                'message': 'Your heart rate is elevated. Consider rest or stress management.',
                'timestamp': datetime.now().isoformat()
            })
        
        # Sleep duration alert
        if health_data.get('sleep_hours', 0) < 6:
            alerts.append({
                'type': 'sleep_insufficient',
                'severity': 'high',
                'message': 'You need more sleep. Aim for 7-9 hours nightly.',
                'timestamp': datetime.now().isoformat()
            })
        
        # Activity alert
        if health_data.get('steps', 0) < 3000:
            alerts.append({
                'type': 'activity_low',
                'severity': 'low',
                'message': 'Consider taking a short walk to boost your activity.',
                'timestamp': datetime.now().isoformat()
            })
        
        return alerts
    
    def _send_health_alert(self, user_id: str, alerts: List[Dict[str, Any]]):
        """Send health alert to user"""
        for alert in alerts:
            self.socketio.emit('health_alert', {
                'user_id': user_id,
                'alert': alert
            }, room=user_id)
            
            logger.info(f"Health alert sent to {user_id}: {alert['message']}")
    
    def _send_health_update(self, user_id: str, health_data: Dict[str, Any]):
        """Send real-time health update to user"""
        self.socketio.emit('health_update', {
            'user_id': user_id,
            'data': health_data
        }, room=user_id)

class InteractiveDashboard:
    """Interactive dashboard with advanced features"""
    
    def __init__(self, socketio):
        self.socketio = socketio
        self.user_sessions = {}
        self.dashboard_analytics = {}
    
    def initialize_user_session(self, user_id: str, preferences: Dict[str, Any]):
        """Initialize interactive session for user"""
        self.user_sessions[user_id] = {
            'preferences': preferences,
            'active_widgets': ['wellness_score', 'fitness_trend', 'sleep_analysis'],
            'last_interaction': datetime.now(),
            'customization': {
                'theme': 'light',
                'layout': 'grid',
                'notifications': True
            }
        }
        
        logger.info(f"Initialized dashboard session for user: {user_id}")
    
    def handle_widget_interaction(self, user_id: str, widget_type: str, action: str, data: Dict[str, Any]):
        """Handle user interactions with dashboard widgets"""
        if user_id not in self.user_sessions:
            return {'error': 'User session not found'}
        
        session_data = self.user_sessions[user_id]
        session_data['last_interaction'] = datetime.now()
        
        # Track analytics
        if user_id not in self.dashboard_analytics:
            self.dashboard_analytics[user_id] = {
                'interactions': [],
                'widget_usage': {},
                'session_duration': 0
            }
        
        # Record interaction
        interaction = {
            'widget_type': widget_type,
            'action': action,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        
        self.dashboard_analytics[user_id]['interactions'].append(interaction)
        
        # Update widget usage stats
        widget_key = f"{widget_type}_{action}"
        self.dashboard_analytics[user_id]['widget_usage'][widget_key] = \
            self.dashboard_analytics[user_id]['widget_usage'].get(widget_key, 0) + 1
        
        # Handle specific widget actions
        response = self._process_widget_action(user_id, widget_type, action, data)
        
        return response
    
    def _process_widget_action(self, user_id: str, widget_type: str, action: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process specific widget actions"""
        if widget_type == 'wellness_score' and action == 'drill_down':
            return {
                'action': 'show_detailed_breakdown',
                'data': {
                    'fitness_component': 40.0,
                    'sleep_component': 35.0,
                    'mood_component': 25.0,
                    'trends': ['fitness_improving', 'sleep_stable', 'mood_positive']
                }
            }
        
        elif widget_type == 'fitness_trend' and action == 'set_goal':
            return {
                'action': 'goal_setting_interface',
                'data': {
                    'current_steps': data.get('current_steps', 0),
                    'suggested_goals': [8000, 10000, 12000],
                    'achievement_timeline': '30 days'
                }
            }
        
        elif widget_type == 'sleep_analysis' and action == 'view_patterns':
            return {
                'action': 'show_sleep_patterns',
                'data': {
                    'weekly_average': 7.2,
                    'consistency_score': 0.85,
                    'recommendations': [
                        'Maintain consistent bedtime',
                        'Limit screen time before bed',
                        'Create sleep-friendly environment'
                    ]
                }
            }
        
        return {'action': 'acknowledged', 'data': {}}
    
    def get_user_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get user's dashboard analytics"""
        if user_id not in self.dashboard_analytics:
            return {'error': 'No analytics data found'}
        
        analytics = self.dashboard_analytics[user_id]
        
        # Calculate session duration
        if user_id in self.user_sessions:
            session_start = self.user_sessions[user_id]['last_interaction']
            session_duration = (datetime.now() - session_start).total_seconds()
            analytics['session_duration'] = session_duration
        
        return {
            'total_interactions': len(analytics['interactions']),
            'most_used_widget': max(analytics['widget_usage'].items(), key=lambda x: x[1])[0] if analytics['widget_usage'] else None,
            'session_duration_minutes': analytics['session_duration'] / 60,
            'engagement_score': self._calculate_engagement_score(analytics)
        }
    
    def _calculate_engagement_score(self, analytics: Dict[str, Any]) -> float:
        """Calculate user engagement score"""
        interactions = len(analytics['interactions'])
        session_duration = analytics['session_duration']
        
        # Simple engagement calculation
        if session_duration > 0:
            engagement = min(100, (interactions / (session_duration / 60)) * 10)
        else:
            engagement = 0
        
        return round(engagement, 1)

class NotificationSystem:
    """Advanced notification system for health insights"""
    
    def __init__(self, socketio):
        self.socketio = socketio
        self.notification_queue = []
        self.user_notification_preferences = {}
    
    def send_notification(self, user_id: str, notification_type: str, message: str, 
                         priority: str = 'medium', data: Dict[str, Any] = None):
        """Send notification to user"""
        notification = {
            'id': f"notif_{int(time.time())}",
            'user_id': user_id,
            'type': notification_type,
            'message': message,
            'priority': priority,
            'timestamp': datetime.now().isoformat(),
            'data': data or {},
            'read': False
        }
        
        # Add to queue
        self.notification_queue.append(notification)
        
        # Send via WebSocket
        self.socketio.emit('notification', notification, room=user_id)
        
        logger.info(f"Notification sent to {user_id}: {message}")
    
    def get_user_notifications(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get user's recent notifications"""
        user_notifications = [
            n for n in self.notification_queue 
            if n['user_id'] == user_id
        ]
        
        # Sort by timestamp (newest first)
        user_notifications.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return user_notifications[:limit]
    
    def mark_notification_read(self, user_id: str, notification_id: str) -> bool:
        """Mark notification as read"""
        for notification in self.notification_queue:
            if notification['id'] == notification_id and notification['user_id'] == user_id:
                notification['read'] = True
                return True
        return False

# Example usage with Flask-SocketIO
def create_advanced_dashboard_app():
    """Create Flask app with advanced dashboard features"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    # Initialize components
    health_monitor = RealTimeHealthMonitor(socketio)
    dashboard = InteractiveDashboard(socketio)
    notifications = NotificationSystem(socketio)
    
    @socketio.on('connect')
    def handle_connect():
        user_id = request.sid  # In production, get from JWT token
        health_monitor.start_monitoring(user_id)
        emit('connected', {'status': 'success'})
    
    @socketio.on('disconnect')
    def handle_disconnect():
        user_id = request.sid
        health_monitor.stop_monitoring(user_id)
    
    @socketio.on('widget_interaction')
    def handle_widget_interaction(data):
        user_id = request.sid
        response = dashboard.handle_widget_interaction(
            user_id, 
            data['widget_type'], 
            data['action'], 
            data.get('data', {})
        )
        emit('widget_response', response)
    
    @socketio.on('get_notifications')
    def handle_get_notifications():
        user_id = request.sid
        user_notifications = notifications.get_user_notifications(user_id)
        emit('notifications_list', user_notifications)
    
    return app, socketio

if __name__ == "__main__":
    app, socketio = create_advanced_dashboard_app()
    print("🚀 Advanced Dashboard with real-time features ready!")
    print("Features:")
    print("✅ Real-time health monitoring")
    print("✅ Interactive widgets")
    print("✅ WebSocket notifications")
    print("✅ User analytics")
    print("✅ Health alerts")
    
    # Run the app
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
