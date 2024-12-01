from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# Load outputs from the previous steps
fitness_output = json.load(open('fitness_tracking_output.json'))
sleep_output = json.load(open('sleep_analysis_output.json'))
journaling_output = json.load(open('journaling_sentiment_analysis_output.json'))
insights_output = json.load(open('aggregated_insights.json'))

# Define route for dashboard
@app.route('/')
def dashboard():
    return render_template('dashboard.html', 
                           fitness_data=fitness_output, 
                           sleep_data=sleep_output, 
                           journal_data=journaling_output, 
                           insights=insights_output['insights'])

# Define route for API output (optional)
@app.route('/api')
def api_output():
    return jsonify(insights_output)

if __name__ == '__main__':
    app.run(debug=True)
