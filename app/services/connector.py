from sqlalchemy import create_engine
from transformers import pipeline
import httpx

class DatabaseConnector:
    def __init__(self, config):
        self.engine = create_engine(config["url"])
    
    def get_engine(self):
        return self.engine

class LLMServiceConnector:
    def __init__(self, config):
        self.generator = pipeline(config["model"])
    
    def generate_text(self, prompt: str) -> str:
        return self.generator(prompt, max_length=50)[0]['generated_text']

class ServerlessServiceConnector:
    def __init__(self, config):
        self.endpoint = config["endpoint"]
    
    async def call_endpoint(self, data):
        async with httpx.AsyncClient() as client:
            response = await client.post(self.endpoint, json=data)
        return response.json()
