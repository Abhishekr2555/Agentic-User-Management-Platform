import os
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.mcp import MCPServerSSE


load_dotenv()

model_name = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")

groq_model = GroqModel(
    model_name=model_name,
)

mcp_server = MCPServerSSE(
    url="http://localhost:8001/sse"
)

weather_agent = Agent(
    model=groq_model,
    system_prompt=(
        "You are a helpful user management assistant. "
        "You can create, read, update, delete, and list users. "
        "Always confirm actions before performing destructive operations like deletions. "
        "When creating users, make sure to get all required information (name and email). "
        "Be friendly and professional in your interactions."
    ),
    toolsets=[mcp_server],
)
