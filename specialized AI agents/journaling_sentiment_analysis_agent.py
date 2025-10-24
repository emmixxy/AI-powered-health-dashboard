from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JournalingSentimentAnalysisAgent:
    """
    Advanced journaling sentiment analysis agent with comprehensive emotional insights
    """
    
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        self.emotion_keywords = {
            'anxiety': ['anxious', 'worried', 'nervous', 'stressed', 'overwhelmed', 'panic'],
            'depression': ['sad', 'depressed', 'down', 'hopeless', 'empty', 'lonely'],
            'anger': ['angry', 'frustrated', 'irritated', 'mad', 'furious', 'annoyed'],
            'joy': ['happy', 'excited', 'joyful', 'cheerful', 'elated', 'thrilled'],
            'fear': ['scared', 'afraid', 'terrified', 'fearful', 'worried', 'concerned'],
            'gratitude': ['grateful', 'thankful', 'appreciate', 'blessed', 'fortunate']
        }
    
    def analyze_journaling_sentiment(self, journal_entries: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Comprehensive sentiment analysis with emotional insights and trends
        """
        try:
            analysis = {
                'user_id': '12345',  # Default user ID
                'analysis_date': datetime.now().isoformat(),
                'sentiment_results': [],
                'emotional_insights': [],
                'sentiment_trends': {},
                'wellness_recommendations': [],
                'summary': {}
            }
            
            # Analyze each journal entry
            for entry in journal_entries:
                sentiment_result = self._analyze_single_entry(entry)
                analysis['sentiment_results'].append(sentiment_result)
            
            # Calculate overall trends and insights
            analysis['sentiment_trends'] = self._calculate_sentiment_trends(analysis['sentiment_results'])
            analysis['emotional_insights'] = self._generate_emotional_insights(analysis['sentiment_results'])
            analysis['wellness_recommendations'] = self._generate_wellness_recommendations(analysis['sentiment_results'])
            analysis['summary'] = self._generate_summary(analysis['sentiment_results'])
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return self._get_error_response()
    
    def _analyze_single_entry(self, entry: Dict[str, str]) -> Dict[str, Any]:
        """Analyze a single journal entry for sentiment and emotions"""
        text = entry['entry']
        date = entry['date']
        
        # VADER sentiment analysis
        sentiment_scores = self.analyzer.polarity_scores(text)
        
        # Determine overall sentiment
        compound_score = sentiment_scores['compound']
        if compound_score >= 0.05:
            sentiment = 'positive'
        elif compound_score <= -0.05:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        # Detect specific emotions
        emotions = self._detect_emotions(text)
        
        # Calculate emotional intensity
        emotional_intensity = self._calculate_emotional_intensity(sentiment_scores, emotions)
        
        # Generate entry-specific insights
        insights = self._generate_entry_insights(sentiment, emotions, emotional_intensity)
        
        return {
            'date': date,
            'sentiment': sentiment,
            'sentiment_scores': sentiment_scores,
            'emotions_detected': emotions,
            'emotional_intensity': emotional_intensity,
            'insights': insights,
            'text_length': len(text.split()),
            'readability_score': self._calculate_readability_score(text)
        }
    
    def _detect_emotions(self, text: str) -> List[str]:
        """Detect specific emotions in the text"""
        text_lower = text.lower()
        detected_emotions = []
        
        for emotion, keywords in self.emotion_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_emotions.append(emotion)
        
        return detected_emotions
    
    def _calculate_emotional_intensity(self, sentiment_scores: Dict, emotions: List[str]) -> str:
        """Calculate the intensity of emotional expression"""
        compound = abs(sentiment_scores['compound'])
        emotion_count = len(emotions)
        
        if compound >= 0.7 or emotion_count >= 3:
            return 'high'
        elif compound >= 0.4 or emotion_count >= 2:
            return 'medium'
        else:
            return 'low'
    
    def _generate_entry_insights(self, sentiment: str, emotions: List[str], intensity: str) -> List[str]:
        """Generate insights for a single journal entry"""
        insights = []
        
        if sentiment == 'negative' and 'anxiety' in emotions:
            insights.append("This entry shows signs of anxiety. Consider stress management techniques.")
        elif sentiment == 'negative' and 'depression' in emotions:
            insights.append("This entry suggests low mood. It might be helpful to engage in activities you enjoy.")
        elif sentiment == 'positive' and 'gratitude' in emotions:
            insights.append("Great to see gratitude in your writing! This practice can improve overall well-being.")
        elif intensity == 'high':
            insights.append("This entry shows strong emotional expression. Consider if you need additional support.")
        
        return insights
    
    def _calculate_sentiment_trends(self, sentiment_results: List[Dict]) -> Dict[str, Any]:
        """Calculate sentiment trends over time"""
        if len(sentiment_results) < 2:
            return {'trend': 'insufficient_data'}
        
        # Calculate trend direction
        recent_sentiments = [r['sentiment'] for r in sentiment_results[-3:]]  # Last 3 entries
        earlier_sentiments = [r['sentiment'] for r in sentiment_results[:-3]] if len(sentiment_results) > 3 else []
        
        if not earlier_sentiments:
            return {'trend': 'insufficient_data'}
        
        recent_positive = sum(1 for s in recent_sentiments if s == 'positive') / len(recent_sentiments)
        earlier_positive = sum(1 for s in earlier_sentiments if s == 'positive') / len(earlier_sentiments)
        
        if recent_positive > earlier_positive + 0.2:
            trend = 'improving'
        elif recent_positive < earlier_positive - 0.2:
            trend = 'declining'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'recent_sentiment_distribution': self._calculate_sentiment_distribution(recent_sentiments),
            'overall_sentiment_distribution': self._calculate_sentiment_distribution([r['sentiment'] for r in sentiment_results])
        }
    
    def _calculate_sentiment_distribution(self, sentiments: List[str]) -> Dict[str, float]:
        """Calculate distribution of sentiments"""
        total = len(sentiments)
        if total == 0:
            return {'positive': 0, 'negative': 0, 'neutral': 0}
        
        return {
            'positive': sum(1 for s in sentiments if s == 'positive') / total,
            'negative': sum(1 for s in sentiments if s == 'negative') / total,
            'neutral': sum(1 for s in sentiments if s == 'neutral') / total
        }
    
    def _generate_emotional_insights(self, sentiment_results: List[Dict]) -> List[str]:
        """Generate comprehensive emotional insights"""
        insights = []
        
        # Analyze emotion patterns
        all_emotions = []
        for result in sentiment_results:
            all_emotions.extend(result['emotions_detected'])
        
        emotion_counts = {}
        for emotion in all_emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Generate insights based on emotion patterns
        if emotion_counts.get('anxiety', 0) > len(sentiment_results) * 0.3:
            insights.append("You've been experiencing anxiety frequently. Consider mindfulness or relaxation techniques.")
        
        if emotion_counts.get('depression', 0) > len(sentiment_results) * 0.2:
            insights.append("Your entries show signs of low mood. Consider reaching out to a mental health professional.")
        
        if emotion_counts.get('gratitude', 0) > len(sentiment_results) * 0.3:
            insights.append("Great job practicing gratitude! This positive habit can significantly improve your well-being.")
        
        # Analyze sentiment patterns
        negative_entries = [r for r in sentiment_results if r['sentiment'] == 'negative']
        if len(negative_entries) > len(sentiment_results) * 0.5:
            insights.append("Your recent entries show predominantly negative sentiment. Consider activities that bring you joy.")
        
        return insights
    
    def _generate_wellness_recommendations(self, sentiment_results: List[Dict]) -> List[str]:
        """Generate personalized wellness recommendations"""
        recommendations = []
        
        # Analyze overall sentiment
        positive_count = sum(1 for r in sentiment_results if r['sentiment'] == 'positive')
        negative_count = sum(1 for r in sentiment_results if r['sentiment'] == 'negative')
        
        if negative_count > positive_count:
            recommendations.append("Consider incorporating daily gratitude practice into your routine.")
            recommendations.append("Try engaging in activities that bring you joy and relaxation.")
        
        # Analyze emotional patterns
        anxiety_entries = [r for r in sentiment_results if 'anxiety' in r['emotions_detected']]
        if len(anxiety_entries) > len(sentiment_results) * 0.3:
            recommendations.append("For managing anxiety, try deep breathing exercises or meditation.")
            recommendations.append("Consider establishing a consistent daily routine to reduce uncertainty.")
        
        depression_entries = [r for r in sentiment_results if 'depression' in r['emotions_detected']]
        if len(depression_entries) > len(sentiment_results) * 0.2:
            recommendations.append("If you're feeling consistently down, consider reaching out to a mental health professional.")
            recommendations.append("Try to maintain social connections and engage in activities you used to enjoy.")
        
        return recommendations
    
    def _generate_summary(self, sentiment_results: List[Dict]) -> Dict[str, Any]:
        """Generate comprehensive summary of sentiment analysis"""
        total_entries = len(sentiment_results)
        if total_entries == 0:
            return {'error': 'No entries to analyze'}
        
        positive = sum(1 for r in sentiment_results if r['sentiment'] == 'positive')
        negative = sum(1 for r in sentiment_results if r['sentiment'] == 'negative')
        neutral = sum(1 for r in sentiment_results if r['sentiment'] == 'neutral')
        
        # Calculate average emotional intensity
        intensities = [r['emotional_intensity'] for r in sentiment_results]
        high_intensity = sum(1 for i in intensities if i == 'high')
        
        return {
            'total_entries': total_entries,
            'sentiment_distribution': {
                'positive_percentage': (positive / total_entries) * 100,
                'negative_percentage': (negative / total_entries) * 100,
                'neutral_percentage': (neutral / total_entries) * 100
            },
            'emotional_intensity': {
                'high_intensity_percentage': (high_intensity / total_entries) * 100
            },
            'overall_sentiment': 'positive' if positive > negative else 'negative' if negative > positive else 'neutral'
        }
    
    def _calculate_readability_score(self, text: str) -> float:
        """Calculate a simple readability score"""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        
        if len(sentences) == 0 or len(words) == 0:
            return 0.0
        
        avg_words_per_sentence = len(words) / len(sentences)
        return min(100, max(0, 100 - (avg_words_per_sentence - 10) * 2))
    
    def _get_error_response(self) -> Dict[str, Any]:
        """Return error response when analysis fails"""
        return {
            'user_id': 'unknown',
            'analysis_date': datetime.now().isoformat(),
            'error': 'Sentiment analysis failed',
            'sentiment_results': [],
            'emotional_insights': [],
            'sentiment_trends': {},
            'wellness_recommendations': [],
            'summary': {'error': 'Analysis failed'}
        }

# Example usage
if __name__ == "__main__":
    # Sample journal entries
    journal_entries = [
        {"date": "2024-11-22", "entry": "I feel really anxious about the upcoming presentation. It's overwhelming and I can't stop worrying about it."},
        {"date": "2024-11-21", "entry": "Had a great day today! Felt accomplished after finishing all my tasks. I'm grateful for the support from my team."},
        {"date": "2024-11-20", "entry": "Feeling a bit down today. Nothing seems to be going right and I'm struggling to find motivation."}
    ]
    
    try:
        # Initialize and run sentiment agent
        sentiment_agent = JournalingSentimentAnalysisAgent()
        analysis = sentiment_agent.analyze_journaling_sentiment(journal_entries)
        
        # Save output
        with open('journaling_sentiment_analysis_output.json', 'w') as f:
            json.dump(analysis, f, indent=4)
        
        print("Sentiment analysis completed successfully!")
        print(f"Analyzed {len(analysis['sentiment_results'])} journal entries")
        print(f"Overall sentiment: {analysis['summary']['overall_sentiment']}")
        
    except Exception as e:
        logger.error(f"Error running sentiment analysis: {e}")
