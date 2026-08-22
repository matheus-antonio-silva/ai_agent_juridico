import os
import requests

from dotenv import load_dotenv

load_dotenv()

url = "https://google.serper.dev/search"

headers = {
    "X-API-KEY": os.getenv("SERPER_API_KEY"),
    "Content-Type": "application/json"
}

payload = {
    "q": "Direito do consumidor Brasil"
}

response = requests.post(
    url,
    headers=headers,
    json=payload
)

print("Status:", response.status_code)
print(response.text)