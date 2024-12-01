from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json

def journaling_sentiment_analysis_agent(journal_entries):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_results = []

    for entry in journal_entries:
        sentiment_score = analyzer.polarity_scores(entry['entry'])
        sentiment = 'positive' if sentiment_score['compound'] > 0 else 'negative' if sentiment_score['compound'] < 0 else 'neutral'
        
        sentiment_results.append({
            "date": entry['date'],
            "sentiment": sentiment
        })
    
    positive = sum(1 for res in sentiment_results if res['sentiment'] == 'positive')
    negative = sum(1 for res in sentiment_results if res['sentiment'] == 'negative')
    neutral = sum(1 for res in sentiment_results if res['sentiment'] == 'neutral')
    
    summary = f"Your journal entries this week were {positive*100/len(journal_entries)}% positive, {negative*100/len(journal_entries)}% negative, {neutral*100/len(journal_entries)}% neutral."
    
    output = {
        "sentiment_results": sentiment_results,
        "summary": summary
    }

    return output

# Sample input data
journal_entries = [
    {"date": "2024-11-22", "entry": "I feel really anxious about the upcoming presentation. It's overwhelming."},
    {"date": "2024-11-21", "entry": "Had a great day today! Felt accomplished after finishing all my tasks."}
]

# Run the agent
output = journaling_sentiment_analysis_agent(journal_entries)

# Convert to JSON
output_json = json.dumps(output, indent=4)

# Save to file
with open('journaling_sentiment_output.json', 'w') as f:
    f.write(output_json)

print(output_json)  # Optional: Print the output to check
