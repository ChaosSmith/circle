import requests
import json

url = "http://10.88.111.49:8000/"

# response = requests.get(url)
#
# print(response.text)

api_key = "f1e07c90a0fc6c46f078aac9b20635"
params = {}
# params = {"api_key": api_key}
params["api_key"] = api_key
channel_id = 53
params["channel_id"] = channel_id
message = "Test Message One"

data = json.dumps({"content": message, "channel_id": channel_id})

response = requests.post(url=url+"messages",params=params, data=data)
print(response.text)

response = requests.get(url + "messages", params=params)
print(response.text)

def fetch(channel):
    url = "http://10.88.111.49:8000/messages"
    params = {"api_key": "f1e07c90a0fc6c46f078aac9b20635"}

    response = requests.get(url=url, params=params)

    return response
