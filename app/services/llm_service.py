from app.models import Assistant, Thread, Message, Run
from liteLLM import LLMClient


class LLMService:
    client = LLMClient(api_key="your_api_key")

    @staticmethod
    async def create_assistant(assistant: Assistant):
        response = await LLMService.client.create_assistant(
            name=assistant.name,
            model=assistant.model,
            instructions=assistant.instructions,
            tools=assistant.tools,
        )
        return response

    @staticmethod
    async def get_assistant(assistant_id: str):
        response = await LLMService.client.get_assistant(assistant_id)
        return response

    @staticmethod
    async def create_thread(thread: Thread):
        response = await LLMService.client.create_thread(
            assistant_id=thread.assistant_id, messages=thread.messages
        )
        return response

    @staticmethod
    async def get_thread(thread_id: str):
        response = await LLMService.client.get_thread(thread_id)
        return response

    @staticmethod
    async def add_message(thread_id: str, message: Message):
        response = await LLMService.client.add_message(
            thread_id=thread_id, role=message.role, content=message.content
        )
        return response

    @staticmethod
    async def get_messages(thread_id: str):
        response = await LLMService.client.get_messages(thread_id)
        return response

    @staticmethod
    async def run_thread(thread_id: str, run: Run):
        response = await LLMService.client.run_thread(
            thread_id=thread_id, assistant_id=run.assistant_id
        )
        return response

    @staticmethod
    async def get_run(thread_id: str, run_id: str):
        response = await LLMService.client.get_run(thread_id, run_id)
        return response
