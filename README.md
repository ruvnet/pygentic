```
   ___                      _   _      
  / _ \/\_/\__ _  ___ _ __ | |_(_) ___ 
 / /_)/\_ _/ _` |/ _ \ '_ \| __| |/ __|
/ ___/  / \ (_| |  __/ | | | |_| | (__ 
\/      \_/\__, |\___|_| |_|\__|_|\___|
           |___/                       

    Created by rUv
```

### Introduction to Pygentic Framework

Pygentic is an innovative system designed to enhance the capabilities of AI assistants by providing a flexible and standardized API. 

Based on the robust architecture of the OpenAI Assistants API, Pygentic abstracts the complexities of integrating with different Large Language Models (LLMs), both local and remote. This abstraction ensures a consistent and seamless interaction regardless of the underlying model.

### What is the Pygentic Library?

The Pygentic library acts as a bridge between your application and various LLMs. It simplifies the process of connecting to different AI models by offering a uniform API, eliminating the need to manage the specifics of each model. Whether you're using OpenAI, a local model, or another remote service, Pygentic provides a reliable and consistent interface.

### Pygentic Agents

Pygentic introduces the concept of agents—intelligent assistants that can perform a range of tasks. These agents are configured to understand and respond to user inputs, utilizing different LLMs for processing. You can create and manage multiple agents, each tailored to specific functions or tasks, enhancing the versatility and efficiency of your AI-driven applications.

### Concurrency

Concurrency in Pygentic ensures that multiple tasks can be handled simultaneously without compromising performance. This is particularly important for applications requiring real-time responses or handling numerous requests at once. Pygentic's design leverages modern asynchronous programming techniques to manage these tasks efficiently, providing a smooth and responsive experience.

### Plugin Connector System

Pygentic's plugin connector system allows you to easily extend the core functionality by adding custom connectors without modifying the main codebase. This system uses a flexible configuration approach with TOML files, enabling you to define new connectors in separate Python files and dynamically load them into the application. This ensures seamless integration and easy updates while maintaining stability and performance.

### Serverless

Pygentic supports serverless architectures, enabling you to deploy your AI applications without the need to manage infrastructure. This approach reduces operational complexity and costs, as the serverless platform handles scaling, monitoring, and resource allocation automatically. You can focus on developing and refining your AI capabilities, while the serverless environment ensures robust and scalable 

### Open-Interpreter (Multi-Programming Language Support)

The open-interpreter feature of Pygentic allows for multi-programming language support, enabling your agents to understand and generate responses in various programming languages. This expands the reach of your applications, making them compatible with a variety of different software projects. The flexibility to interpret and interact in multiple programming languages enhances the usability and effectiveness of your AI solutions.

### Practical Applications

Pygentic can be applied across numerous practical scenarios:
- **Customer Support**: Deploy intelligent agents to handle customer queries, providing instant and accurate responses.
- **Content Generation**: Use AI to create engaging content in multiple languages, tailored to your audience.
- **Data Analysis**: Leverage AI for interpreting and analyzing large datasets, extracting meaningful insights.
- **Personal Assistants**: Develop personalized AI assistants to help with daily tasks, scheduling, and information retrieval.

Pygentic empowers developers to harness the power of AI with ease, offering a flexible and scalable solution for integrating advanced language models into various applications. Its consistent API, multi-language support, and serverless capabilities make it a valuable tool for modern AI-driven projects.

## Project Architecture

Here's a detailed breakdown of the directory structure and code blocks for each file.

### 1. **Directory Structure**

```
pygentic/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── assistants.py
│   │   ├── threads.py
│   │   ├── messages.py
│   │   ├── runs.py
│   └── services/
│       ├── __init__.py
│       ├── llm_service.py
│       ├── serverless_service.py
│       ├── open_interpreter_service.py
│       ├── database.py
│       ├── plugin_loader.py
│       ├── interfaces.py
├── tests/
│   ├── __init__.py
│   ├── test_assistants.py
│   ├── test_threads.py
│   ├── test_messages.py
│   ├── test_runs.py
├── connectors.toml
├── requirements.txt
└── README.md
```

## Installation

You can install the Pygentic library using pip:

```bash
pip install pygentic
```

## Running the Application

After installing the library, you can run the application using the following command:

```bash
pygentic
```

## Endpoints

### Assistants
- `POST /v1/assistants`: Create a new assistant.
- `GET /v1/assistants/{assistant_id}`: Retrieve an assistant by ID.
  - Note: The FastAPI UI now includes example JSON with test values for easier endpoint testing.

### Threads
- `POST /v1/threads`: Create a new thread.
- `GET /v1/threads/{thread_id}`: Retrieve a thread by ID.

### Messages
- `POST /v1/threads/{thread_id}/messages`: Add a message to a thread.
- `GET /v1/threads/{thread_id}/messages`: Retrieve messages in a thread.

### Runs
- `POST /v1/threads/{thread_id}/runs`: Run a thread with an assistant.
- `GET /v1/threads/{thread_id}/runs/{run_id}`: Retrieve a run by ID.
 
 ## TOML Configuration for Connectors

Pygentic uses a TOML configuration file to define and manage connectors for various services. This approach enhances flexibility, speed, concurrency, and stability by centralizing the configuration in an easily readable and editable format.

### Configuration Format

Create a `connectors.toml` file in your project root with the following structure:

```toml
[connectors]
    [connectors.database]
    url = "sqlite:///./test.db"
    
    [connectors.llm_service]
    model = "gpt-3.5-turbo"
    
    [connectors.serverless_service]
    endpoint = "https://api.example.com/endpoint"
```
## Parsing the Configuration File
The Pygentic library automatically parses the connectors.toml file at startup. Ensure your configuration file is correctly formatted and placed in the root directory of your project.
### Connectors in Pygentic

Pygentic's connectors provide a flexible and modular way to integrate various services into your AI applications. They abstract the complexities of interacting with different APIs, including the OpenAI Assistants API, allowing you to connect endpoints to various services without altering the core code. This section explains how connectors work and how you can create custom connectors.

### How Connectors Work

Connectors in Pygentic are designed to manage connections to various services such as databases, large language models (LLMs), and serverless endpoints. The default implementation includes an `OpenAIAssistantConnector` that interacts with the OpenAI Assistants API. However, you can easily create custom connectors to integrate other services.

#### Connector Classes

Pygentic includes several built-in connector classes:

- **DatabaseConnector**: Manages the connection to a database.
- **LLMServiceConnector**: Manages the connection to a large language model service.
- **ServerlessServiceConnector**: Manages the connection to a serverless endpoint.
- **OpenAIAssistantConnector**: Connects to the OpenAI Assistants API to handle various assistant operations.

These connectors are initialized with configurations from the `connectors.toml` file and used within FastAPI middleware to make services available to your endpoints.

### Creating Custom Connectors

Pygentic's modular structure allows users to extend its functionality by creating custom connectors without modifying the core code. Follow these steps to create and use your custom connectors:

#### Define a Custom Connector

Create a new file in your custom connectors directory (e.g., `custom_connectors/`) and define a class inheriting from `BaseConnector`.

**Example:**

```python
from app.services.interfaces import BaseConnector

class MyCustomConnector(BaseConnector):

    def initialize(self, config: dict):
        self.config = config
        self.connected = False

    async def connect(self):
        self.connected = True

    async def disconnect(self):
        self.connected = False

    async def generate_text(self, prompt: str) -> str:
        if not self.connected:
            await self.connect()
        return "Generated text based on prompt: " + prompt
```

#### Update Configuration

Add your custom connector configuration to the `connectors.toml` file.

**Example:**

```toml
[connectors]
    [connectors.database]
    url = "postgres://user:password@localhost/dbname"
    
    [connectors.llm_service]
    model = "gpt-4"
    
    [connectors.serverless_service]
    endpoint = "https://example.com/serverless"

    [connectors.mycustomconnector]
    custom_setting = "value"
```

#### Run the Application

Set the environment variable `PYGENTIC_PLUGIN_DIR` to point to your custom connectors directory, and then run the Pygentic application.

```bash
export PYGENTIC_PLUGIN_DIR=custom_connectors
pygentic
```

#### Access Custom Connector Methods

Your custom connector methods can be accessed within your FastAPI endpoints via `request.state`.

```python
@app.get("/custom_action")
async def custom_action(request: Request):
    result = await request.state.mycustomconnector.generate_text("Hello, Pygentic!")
    return {"result": result}
```

By following these steps, you can extend Pygentic's functionality with custom connectors tailored to your specific needs without modifying the core library code. This approach ensures that your integrations remain robust and adaptable to various services, providing a seamless and consistent API for your AI applications.

## Configuring Database Connectors

To switch the SQLite database to another persistence storage using the connectors system, modify the `connectors.toml` file in your project root. Below is an example configuration for a PostgreSQL setup:

```toml
[connectors]
    [connectors.database]
    url = "postgresql://user:password@localhost/dbname"
    
    [connectors.llm_service]
    model = "gpt-3.5-turbo"
    
    [connectors.serverless_service]
    endpoint = "https://api.example.com/endpoint"
```

This configuration demonstrates how to change the database connector from SQLite to PostgreSQL. Ensure that your PostgreSQL server is running and accessible at the specified URL.
