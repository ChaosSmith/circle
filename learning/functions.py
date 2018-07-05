import requests
import json

def fetch(channel):
    url = "http://10.88.111.49:8000/messages"
    params = {"api_key": "f1e07c90a0fc6c46f078aac9b20635"}

    response = requests.get(url = url, params = params)

    return response.text

text = fetch(53).text
print(text)
