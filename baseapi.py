import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

class BaseApi():
    def __init__(self):
        self.messages = []
        self.model_name = 'gpt-3.5-turbo'
        self.temperature = 0.5

    def make_openai_call_api(self):
        request_payload = {
                    'model': self.model_name,
                    'temperature': self.temperature,
                    'messages': self.messages,
                }
        response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {os.getenv(f"OPENAI_KEY")}',
                    'Content-Type': 'application/json',
                },
                json=request_payload,
            )
        print(response.text)
        res=json.loads(response.content.decode('utf-8'))
        res = res['choices'][0].get('message').get('content')
        print(res)
        return res

    def add_message(self,role, message):
        self.messages.append({"role": role, "content": message})


