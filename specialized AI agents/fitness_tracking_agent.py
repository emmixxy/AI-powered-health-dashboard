import json

def fitness_tracking_agent(data):
    activity_level = data['activity_level']
    
    if data['steps'] < 8000:
        recommendation = "Increase your steps to 10,000 daily for better cardiovascular health."
    elif data['calories_burned'] < 300:
        recommendation = "Try to burn at least 300 calories during your workouts for optimal results."
    else:
        recommendation = "Great job! Keep up the good work."
    
    output = {
        "steps": data['steps'],
        "calories_burned": data['calories_burned'],
        "active_minutes": data['active_minutes'],
        "recommendation": recommendation
    }
    
    return output

# Sample input data
data = {
    "steps": 7000,
    "calories_burned": 250,
    "active_minutes": 30,
    "activity_level": "moderate"
}

# Run the agent
output = fitness_tracking_agent(data)

# Convert to JSON
output_json = json.dumps(output, indent=4)

# Save to file
with open('fitness_tracking_output.json', 'w') as f:
    f.write(output_json)

print(output_json)  # Optional: Print the output to check
