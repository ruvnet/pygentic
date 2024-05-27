# app/services/open_interpreter_service.py
import asyncio
from app.services.connector import ServerlessServiceConnector
from app import config

serverless_service = ServerlessServiceConnector(config["connectors"]["serverless_service"])

async def handle_request(data):
    response = await serverless_service.call_endpoint(data)
    return response

async def main(data):
    tasks = [handle_request(data) for _ in range(10)]
    results = await asyncio.gather(*tasks)
    return results
