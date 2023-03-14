from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

SLACK_APP_TOKEN = "xoxb-4927881068675-4933413928963-r4mRXL9uTvmlfQJMxiiBJomt"
SLACK_CHANNEL_ID = "C04T8U6KMGW"

def send_slack_alert(alert_message, email):
    if not email:
        return False

    slack_data = {
        "text": f"New spam notification received for {email}: {alert_message}",
        "channel": SLACK_CHANNEL_ID
    }
    headers = {"Content-type": "application/json", "Authorization": f"Bearer {SLACK_APP_TOKEN}"}
    response = requests.post("https://slack.com/api/chat.postMessage", headers=headers, data=json.dumps(slack_data))
    if response.status_code == 200:
        return True
    else:
        return False

@app.route('/')
def index():
    return "Hello, World!"


@app.route('/process_payload', methods=['POST'])
def process_payload():
    if request.method == 'POST':
        payload = request.get_json()
        is_spam = payload.get('is_spam')
        email = payload.get('email')

        if is_spam and email:
            alert_message = f"New spam notification received for {email}: {json.dumps(payload)}"
            if send_slack_alert(alert_message, email):
                return "Alert sent to Slack successfully"
            else:
                return "Failed to send alert to Slack"
        else:
            return "Payload not processed. Not a spam notification."
    else:
        return "Method not allowed"


if __name__ == '__main__':
    app.run(debug=True)


