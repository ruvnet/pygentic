import httpx
from app.services.interfaces import BaseConnector

class OpenAIAssistantConnector(BaseConnector):
    def initialize(self, config: dict):
        self.api_key = config.get("api_key", "your-default-api-key")
        self.base_url = "https://api.openai.com/v1"

    async def connect(self):
        pass

    async def disconnect(self):
        pass

    async def generate_text(self, prompt: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"prompt": prompt, "max_tokens": 50}
            )
        response_data = response.json()
        return response_data['choices'][0]['text']

    async def create_assistant(self, data: dict):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/assistants",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=data
            )
        return response.json()

    async def get_assistant(self, assistant_id: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/assistants/{assistant_id}",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
        return response.json()

    async def create_thread(self, data: dict):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/threads",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=data
            )
        return response.json()

    async def get_thread(self, thread_id: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/threads/{thread_id}",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
        return response.json()

    async def add_message(self, thread_id: str, data: dict):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/threads/{thread_id}/messages",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=data
            )
        return response.json()

    async def get_messages(self, thread_id: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/threads/{thread_id}/messages",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
        return response.json()

    async def run_thread(self, thread_id: str, data: dict):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/threads/{thread_id}/runs",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=data
            )
        return response.json()

    async def get_run(self, thread_id: str, run_id: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/threads/{thread_id}/runs/{run_id}",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
        return response.json()
