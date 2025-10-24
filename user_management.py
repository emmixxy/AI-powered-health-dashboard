"""
User Management and Authentication System
Secure user accounts, data privacy, and personalization
"""

import hashlib
import secrets
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
from dataclasses import dataclass
import jwt

logger = logging.getLogger(__name__)

@dataclass
class User:
    """User data model"""
    user_id: str
    email: str
    name: str
    age: int
    created_at: datetime
    last_login: datetime
    preferences: Dict[str, Any]
    health_goals: Dict[str, Any]
    data_consent: bool
    privacy_settings: Dict[str, Any]

class UserManager:
    """Advanced user management system"""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.users = {}
        self.sessions = {}
        self.encryption_key = self._generate_encryption_key()
    
    def _generate_encryption_key(self) -> str:
        """Generate encryption key for user data"""
        return secrets.token_hex(32)
    
    def _hash_password(self, password: str) -> str:
        """Hash password with salt"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}:{password_hash.hex()}"
    
    def _verify_password(self, password: str, stored_hash: str) -> bool:
        """Verify password against stored hash"""
        try:
            salt, hash_part = stored_hash.split(':')
            password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return password_hash.hex() == hash_part
        except:
            return False
    
    def register_user(self, email: str, password: str, name: str, age: int, 
                     health_goals: Dict[str, Any] = None) -> Dict[str, Any]:
        """Register a new user with secure authentication"""
        try:
            # Check if user already exists
            if email in [user.email for user in self.users.values()]:
                return {'success': False, 'error': 'User already exists'}
            
            # Create user ID
            user_id = secrets.token_urlsafe(16)
            
            # Hash password
            password_hash = self._hash_password(password)
            
            # Create user object
            user = User(
                user_id=user_id,
                email=email,
                name=name,
                age=age,
                created_at=datetime.now(),
                last_login=datetime.now(),
                preferences={
                    'notifications': True,
                    'data_sharing': False,
                    'goal_reminders': True
                },
                health_goals=health_goals or {},
                data_consent=True,
                privacy_settings={
                    'data_retention_days': 365,
                    'anonymize_data': True,
                    'share_insights': False
                }
            )
            
            # Store user (in production, this would be in a database)
            self.users[user_id] = {
                'user': user,
                'password_hash': password_hash
            }
            
            # Generate JWT token
            token = self._generate_jwt_token(user_id)
            
            logger.info(f"User registered: {email}")
            return {
                'success': True,
                'user_id': user_id,
                'token': token,
                'message': 'User registered successfully'
            }
            
        except Exception as e:
            logger.error(f"Registration failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def authenticate_user(self, email: str, password: str) -> Dict[str, Any]:
        """Authenticate user login"""
        try:
            # Find user by email
            user_id = None
            for uid, user_data in self.users.items():
                if user_data['user'].email == email:
                    user_id = uid
                    break
            
            if not user_id:
                return {'success': False, 'error': 'User not found'}
            
            # Verify password
            user_data = self.users[user_id]
            if not self._verify_password(password, user_data['password_hash']):
                return {'success': False, 'error': 'Invalid password'}
            
            # Update last login
            user_data['user'].last_login = datetime.now()
            
            # Generate new token
            token = self._generate_jwt_token(user_id)
            
            logger.info(f"User authenticated: {email}")
            return {
                'success': True,
                'user_id': user_id,
                'token': token,
                'user_info': {
                    'name': user_data['user'].name,
                    'email': user_data['user'].email,
                    'age': user_data['user'].age
                }
            }
            
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _generate_jwt_token(self, user_id: str) -> str:
        """Generate JWT token for user session"""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(days=7),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify JWT token and return user info"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            user_id = payload['user_id']
            
            if user_id not in self.users:
                return {'valid': False, 'error': 'User not found'}
            
            user = self.users[user_id]['user']
            return {
                'valid': True,
                'user_id': user_id,
                'user_info': {
                    'name': user.name,
                    'email': user.email,
                    'age': user.age
                }
            }
            
        except jwt.ExpiredSignatureError:
            return {'valid': False, 'error': 'Token expired'}
        except jwt.InvalidTokenError:
            return {'valid': False, 'error': 'Invalid token'}
        except Exception as e:
            return {'valid': False, 'error': str(e)}
    
    def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> bool:
        """Update user preferences and settings"""
        try:
            if user_id not in self.users:
                return False
            
            user = self.users[user_id]['user']
            user.preferences.update(preferences)
            
            logger.info(f"Preferences updated for user: {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update preferences: {e}")
            return False
    
    def get_user_data_summary(self, user_id: str) -> Dict[str, Any]:
        """Get user data summary for dashboard"""
        if user_id not in self.users:
            return {'error': 'User not found'}
        
        user = self.users[user_id]['user']
        return {
            'user_id': user_id,
            'name': user.name,
            'email': user.email,
            'age': user.age,
            'member_since': user.created_at.isoformat(),
            'last_login': user.last_login.isoformat(),
            'preferences': user.preferences,
            'health_goals': user.health_goals,
            'privacy_settings': user.privacy_settings
        }
    
    def delete_user_data(self, user_id: str) -> bool:
        """Delete all user data (GDPR compliance)"""
        try:
            if user_id not in self.users:
                return False
            
            # Remove user data
            del self.users[user_id]
            
            # Remove any active sessions
            self.sessions = {k: v for k, v in self.sessions.items() if v != user_id}
            
            logger.info(f"User data deleted: {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete user data: {e}")
            return False

class DataPrivacyManager:
    """Advanced data privacy and compliance management"""
    
    def __init__(self):
        self.consent_records = {}
        self.data_retention_policies = {}
    
    def record_consent(self, user_id: str, consent_type: str, granted: bool) -> bool:
        """Record user consent for data processing"""
        try:
            consent_record = {
                'user_id': user_id,
                'consent_type': consent_type,
                'granted': granted,
                'timestamp': datetime.now().isoformat(),
                'ip_address': '127.0.0.1',  # Would be real IP in production
                'user_agent': 'Health Dashboard App'
            }
            
            if user_id not in self.consent_records:
                self.consent_records[user_id] = []
            
            self.consent_records[user_id].append(consent_record)
            
            logger.info(f"Consent recorded: {user_id} - {consent_type}: {granted}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to record consent: {e}")
            return False
    
    def check_consent(self, user_id: str, consent_type: str) -> bool:
        """Check if user has given consent for specific data processing"""
        if user_id not in self.consent_records:
            return False
        
        # Get most recent consent for this type
        recent_consents = [
            record for record in self.consent_records[user_id]
            if record['consent_type'] == consent_type
        ]
        
        if not recent_consents:
            return False
        
        # Return the most recent consent
        latest_consent = max(recent_consents, key=lambda x: x['timestamp'])
        return latest_consent['granted']
    
    def anonymize_user_data(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Anonymize user data for analysis"""
        anonymized = user_data.copy()
        
        # Remove personally identifiable information
        anonymized.pop('email', None)
        anonymized.pop('name', None)
        anonymized.pop('user_id', None)
        
        # Add anonymized identifier
        anonymized['anonymous_id'] = hashlib.sha256(
            f"{user_data.get('user_id', '')}{user_data.get('email', '')}".encode()
        ).hexdigest()[:16]
        
        return anonymized
    
    def get_data_retention_status(self, user_id: str) -> Dict[str, Any]:
        """Check data retention status for user"""
        if user_id not in self.consent_records:
            return {'status': 'no_data'}
        
        # Calculate data age
        oldest_record = min(
            self.consent_records[user_id],
            key=lambda x: x['timestamp']
        )
        
        data_age_days = (datetime.now() - datetime.fromisoformat(
            oldest_record['timestamp']
        )).days
        
        return {
            'status': 'active' if data_age_days < 365 else 'expired',
            'data_age_days': data_age_days,
            'retention_policy': '1 year',
            'action_required': data_age_days >= 365
        }

# Example usage
if __name__ == "__main__":
    # Initialize user management
    user_manager = UserManager("your-secret-key-here")
    privacy_manager = DataPrivacyManager()
    
    # Register a new user
    registration_result = user_manager.register_user(
        email="user@example.com",
        password="secure_password_123",
        name="John Doe",
        age=30,
        health_goals={
            'target_steps': 10000,
            'target_sleep': 8,
            'target_weight': 70
        }
    )
    
    if registration_result['success']:
        print("✅ User registered successfully")
        print(f"User ID: {registration_result['user_id']}")
        print(f"Token: {registration_result['token'][:20]}...")
        
        # Record consent
        privacy_manager.record_consent(
            registration_result['user_id'],
            'health_data_processing',
            True
        )
        
        # Check consent
        has_consent = privacy_manager.check_consent(
            registration_result['user_id'],
            'health_data_processing'
        )
        print(f"User consent for health data: {has_consent}")
    
    # Authenticate user
    auth_result = user_manager.authenticate_user(
        email="user@example.com",
        password="secure_password_123"
    )
    
    if auth_result['success']:
        print("✅ User authenticated successfully")
        print(f"Welcome, {auth_result['user_info']['name']}!")
