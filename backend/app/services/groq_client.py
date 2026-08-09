import requests
from typing import List


class GroqClient:
    def __init__(self, api_key: str, model: str, url: str):
        self.api_key = api_key
        self.model = model
        self.url = url

    def generate(self, messages: List[dict]) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000,
        }
        response = requests.post(self.url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
