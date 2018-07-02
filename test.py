import requests
import json

host = "http://127.0.0.1:5000/"

response = requests.get(host + "player")
print(response.text)
api_key = response.json()['api_key']

response = requests.post(
    url = host + 'messages',
    params={'api_key': api_key},
    data=json.dumps(
        {'content': 'This is a test message!', 'channel_id': None}
        )
    )
print(response.text)

response = requests.get(
    url = host + 'messages',
    params = {
        'channel_id': None,
        'api_key': api_key
        }
    )

print(response.text)
