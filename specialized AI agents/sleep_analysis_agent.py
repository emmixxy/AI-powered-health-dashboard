import numpy as np
import json

def sleep_analysis_agent(sleep_data):
    sleep_durations = np.array([entry['sleep_hours'] for entry in sleep_data])
    
    if np.mean(sleep_durations) < 6.5:
        recommendation = "Your average sleep time has dropped below 6 hours. Consider a consistent bedtime routine."
    else:
        recommendation = "Your sleep patterns are healthy. Keep it up!"
    
    output = {
        "sleep_data": sleep_data,
        "recommendation": recommendation
    }
    
    return output

# Sample input data
sleep_data = [
    {"date": "2024-11-22", "sleep_hours": 6.5},
    {"date": "2024-11-21", "sleep_hours": 7.2}
]

# Run the agent
output = sleep_analysis_agent(sleep_data)

# Convert to JSON
output_json = json.dumps(output, indent=4)

# Save to file
with open('sleep_analysis_output.json', 'w') as f:
    f.write(output_json)

print(output_json)  # Optional: Print the output to check
