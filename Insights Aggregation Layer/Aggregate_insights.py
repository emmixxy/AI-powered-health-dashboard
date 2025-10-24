import json

# Load the outputs from the three agents
# These would be loaded from the JSON files generated earlier
fitness_output = json.load(open('fitness_tracking_output.json'))
sleep_output = json.load(open('sleep_analysis_output.json'))
journaling_output = json.load(open('journaling_sentiment_analysis_output.json'))

# Function to aggregate insights from all agents
def aggregate_insights(fitness_output, sleep_output, journaling_output):
    aggregated_insights = []
    
    # Fitness Insight: Look at steps and recommend improvement if needed
    for entry in fitness_output['fitness_recommendations']:
        if entry['steps'] < 9000:
            aggregated_insights.append(f"Your activity level on {entry['date']} is low. Consider increasing your weekly activity by 10% to improve cardiovascular health.")
        else:
            aggregated_insights.append(f"Your activity level on {entry['date']} is sufficient. Keep up the good work!")
    
    # Sleep Insight: Look at sleep hours and give suggestions if needed
    for entry in sleep_output['sleep_analysis']:
        if entry['sleep_hours'] < 7:
            aggregated_insights.append(f"Your sleep on {entry['date']} is below the recommended 7 hours. Consider a consistent bedtime routine.")
        else:
            aggregated_insights.append(f"Your sleep on {entry['date']} is healthy. Keep up the good sleep habits!")
    
    # Journaling Sentiment Insight: Check if journal entries reflect negative emotions
    negative_entries = [entry for entry in journaling_output['sentiment_results'] if entry['sentiment'] == 'negative']
    if negative_entries:
        aggregated_insights.append(f"Your journal entries this week show some negative emotions. It might be helpful to try some mindfulness techniques to manage stress.")
    else:
        aggregated_insights.append("Your journal entries reflect a positive outlook. Keep up the good mental habits!")
    
    # Summary Insight: Combine insights for a holistic summary
    if len(negative_entries) > 2:
        aggregated_insights.append("Overall, it's important to focus on both physical and mental health. Consider integrating more relaxation and activity into your routine.")
    else:
        aggregated_insights.append("You're doing well! Keep focusing on maintaining balance in both physical and emotional well-being.")

    return aggregated_insights

# Get aggregated insights
aggregated_insights = aggregate_insights(fitness_output, sleep_output, journaling_output)

# Output the aggregated insights
insight_output = {
    "user_id": "12345",
    "insights": aggregated_insights
}

# Save the aggregated insights to a JSON file
with open('aggregated_insights.json', 'w') as f:
    json.dump(insight_output, f, indent=4)

# Print the result for preview
print(json.dumps(insight_output, indent=4))
