# Mind-Body Connection Dashboard

## 🏥 Overview
The Mind-Body Connection Dashboard is an innovative health analytics system that processes data from wearable devices and journaling entries through specialized AI agents to provide comprehensive health insights. The system demonstrates advanced AI integration, modular design, and actionable health recommendations.

## ✨ Key Features

### 🤖 Specialized AI Agents
- **Fitness Tracking Agent**: Advanced physical activity analysis with goal tracking and performance metrics
- **Sleep Analysis Agent**: Comprehensive sleep pattern analysis with quality scoring and recovery insights
- **Sentiment Analysis Agent**: Emotional well-being analysis through journal entry sentiment analysis

### 📊 Comprehensive Analytics
- **Holistic Health Insights**: Cross-domain correlation analysis between fitness, sleep, and mood
- **Wellness Scoring**: Multi-dimensional health assessment (0-100 scale)
- **Priority Recommendations**: Categorized health recommendations by urgency
- **Trend Analysis**: Long-term health pattern identification

### 🎨 Modern Dashboard
- **Responsive Design**: Mobile-friendly interface with beautiful visualizations
- **Real-time Updates**: Live health metrics and recommendations
- **Interactive Elements**: Engaging user experience with hover effects and animations
- **Action Plans**: Step-by-step health improvement guides

## 🏗️ System Architecture

```
Data Sources → Data Integration → AI Agents → Insights Aggregation → Dashboard
     ↓              ↓                ↓              ↓                ↓
Wearable APIs   Normalization   Specialized    Holistic Analysis   User Interface
Mock Data       Validation      Processing    Correlation         REST API
Journal Entries Enrichment      Analysis      Recommendations     Visualization
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd sundial-lands-project
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the dashboard**:
   Open your browser and navigate to `http://localhost:5000`

## 📁 Project Structure

```
sundial-lands-project/
├── app.py                              # Main Flask application
├── dashboard.html                      # Dashboard interface
├── data_integration.py                 # Data integration layer
├── requirements.txt                   # Python dependencies
├── SYSTEM_ARCHITECTURE.md             # System architecture documentation
├── README.md                          # This file
├── specialized AI agents/             # AI agent implementations
│   ├── fitness_tracking_agent.py      # Fitness analysis agent
│   ├── sleep_analysis_agent.py        # Sleep analysis agent
│   ├── journaling_sentiment_analysis_agent.py  # Sentiment analysis agent
│   └── Aggregate_insights.py          # Insights aggregation
├── sundial land assignment/           # Mock data and legacy files
│   └── mock_data.json                 # Sample health data
└── Flask Dashboard/                   # Output files
    ├── fitness_tracking_output.json
    ├── sleep_analysis_output.json
    ├── journaling_sentiment_analysis_output.json
    └── aggregated_insights.json
```

## 🔧 API Endpoints

### Main Dashboard
- **GET** `/` - Main dashboard interface

### Health Data API
- **GET** `/api/health-data` - Complete health data from all agents
- **GET** `/api/wellness-score` - Overall wellness score
- **GET** `/api/recommendations` - Health recommendations
- **POST** `/api/refresh` - Refresh data and regenerate insights

## 📊 Data Processing Pipeline

### 1. Data Integration
- Loads mock health data from JSON files
- Normalizes data to standard format
- Enriches metrics with derived values
- Validates data structure and completeness

### 2. AI Agent Processing
- **Fitness Agent**: Analyzes steps, heart rate, and activity levels
- **Sleep Agent**: Processes sleep duration, quality, and patterns
- **Sentiment Agent**: Evaluates emotional well-being from journal entries

### 3. Insights Aggregation
- Correlates data across all health domains
- Generates holistic health insights
- Creates priority-based recommendations
- Calculates overall wellness score

## 🎯 Key Metrics

### Fitness Metrics
- Daily step count and trends
- Heart rate analysis and zones
- Activity level classification
- Fitness score (0-100)
- Goal achievement tracking

### Sleep Metrics
- Sleep duration and quality
- Sleep efficiency and recovery
- Sleep debt calculation
- Pattern consistency analysis
- Sleep score (0-100)

### Emotional Metrics
- Sentiment analysis (positive/negative/neutral)
- Emotion detection (anxiety, joy, gratitude, etc.)
- Emotional intensity assessment
- Mood trend analysis
- Wellness recommendations

## 🔍 Sample Data Structure

### Input Data (Mock)
```json
{
  "user_id": "12345",
  "metrics": [
    {
      "date": "2024-11-22",
      "steps": 8500,
      "heart_rate": 75,
      "sleep_hours": 6.5,
      "hrv": 45
    }
  ]
}
```

### Output Insights
```json
{
  "wellness_score": 78.5,
  "holistic_insights": [
    "Excellent balance between physical activity and sleep!"
  ],
  "priority_recommendations": [
    {
      "priority": "medium",
      "category": "fitness",
      "recommendation": "Fitness levels could be improved",
      "action": "Start with 30 minutes of moderate activity daily"
    }
  ]
}
```

## 🛠️ Development

### Running Individual Components

1. **Data Integration**:
   ```bash
   python data_integration.py
   ```

2. **Fitness Agent**:
   ```bash
   python "specialized AI agents/fitness_tracking_agent.py"
   ```

3. **Sleep Agent**:
   ```bash
   python "specialized AI agents/sleep_analysis_agent.py"
   ```

4. **Sentiment Agent**:
   ```bash
   python "specialized AI agents/journaling_sentiment_analysis_agent.py"
   ```

5. **Insights Aggregation**:
   ```bash
   python "specialized AI agents/Aggregate_insights.py"
   ```

### Adding New Data Sources

1. Extend `HealthDataIntegrator` class in `data_integration.py`
2. Implement new data source methods
3. Update normalization logic
4. Test with sample data

### Creating New AI Agents

1. Create new agent class following existing patterns
2. Implement analysis methods
3. Add to main application in `app.py`
4. Update dashboard template

## 🔒 Security Considerations

- Input validation for all data sources
- Error handling and logging
- Graceful degradation on failures
- No sensitive data storage (mock data only)

## 🚀 Future Enhancements

### Planned Features
- **Real Wearable API Integration**: Fitbit, Apple HealthKit, Google Fit
- **Machine Learning Models**: Predictive health analytics
- **Mobile Application**: Native iOS/Android apps
- **Social Features**: Health challenges and community
- **Advanced Analytics**: Anomaly detection and personalized coaching

### Technical Improvements
- **Database Integration**: Persistent data storage
- **Authentication**: User management and security
- **Real-time Processing**: WebSocket connections
- **Microservices**: Containerized deployment

## 📈 Performance Metrics

- **Response Time**: < 2 seconds for dashboard load
- **Data Processing**: Handles 30+ days of health data
- **Memory Usage**: Optimized for efficient processing
- **Scalability**: Modular design supports horizontal scaling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests and documentation
5. Submit a pull request

## 📄 License

This project is part of a technical assessment demonstrating AI agent integration and health analytics capabilities.

## 🆘 Support

For questions or issues:
1. Check the system architecture documentation
2. Review the API endpoints
3. Examine the sample data structures
4. Test individual components
or reach me via my email: kosokogbemi@gmail.com

---

**Built with ❤️ for health and wellness**

