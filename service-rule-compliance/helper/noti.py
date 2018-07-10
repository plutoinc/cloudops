import requests
import json


WEB_HOOK_URL = "https://hooks.slack.com/services/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"


def notify(text):
    data = {
        'text': text,
        'username': 'cloudops',
        'icon_emoji': ':robot_face:'
    }
    response = requests.post(WEB_HOOK_URL, data=json.dumps(
        data), headers={'Content-Type': 'application/json'})

    print('Response: ' + str(response.text))
    print('Response code: ' + str(response.status_code))



