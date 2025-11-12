import os

from dotenv import load_dotenv
import requests


load_dotenv()

url = "https://api.asi1.ai/v1/chat/completions"
headers = {
"Authorization": f"Bearer {os.getenv('ASI_ONE_API_KEY')}",
"Content-Type": "application/json"
}
body = {
"model": "asi1-mini",
"messages": [{"role": "user", "content": "Hello! How can you help me today?"}]
}
print(requests.post(url, headers=headers, json=body).json()["choices"][0]["message"]["content"])

