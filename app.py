
from flask import Flask, request

import json

app = Flask(__name__)

# Replace the URL with your Slack webhook URL
SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/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'

# Define a function to check if the payload is a spam notification
def is_spam(payload):
    if payload.get('Type') == 'SpamNotification':
        return True
    else:
        return False

# Define a function to send an alert to Slack
def send_slack_alert(payload, requests=None):
    if is_spam(payload):
        email = payload.get('Email')
        message = f"Spam notification received for email: {email}"
        data = {'text': message}
        headers = {'Content-type': 'application/json'}
        response = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(data), headers=headers)
        return response.status_code
    else:
        return None

# Define the endpoint for receiving a POST request with a JSON payload
@app.route('/process_payload', methods=['POST'])
def process_payload():
    payload = request.get_json()
    status_code = send_slack_alert(payload)
    if status_code == 200:
        return 'Slack alert sent successfully', 200
    else:
        return 'Error sending Slack alert', 500

# Run the app
if __name__ == '__main__':
    app.run()
