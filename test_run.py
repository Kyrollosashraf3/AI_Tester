import requests

url = "http://127.0.0.1:8000/run"
response = requests.post(url)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
