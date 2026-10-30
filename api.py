import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="Travel Planner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

async def ask_agent(question: str) -> str:
    mcp_url = os.getenv("MCP_URL", "http://127.0.0.1:8000/mcp")
    api_key = os.getenv("GROQ_API_KEY")
    model_name = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    if not api_key:
        raise RuntimeError("Set GROQ_API_KEY in .env first.")
    client = MultiServerMCPClient({
        "travel": {"transport": "http", "url": mcp_url}
    })
    tools = await client.get_tools()
    model = ChatGroq(model=model_name, temperature=0, api_key=api_key)
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=(
            "You are a careful travel-planning assistant. Use travel tools "
            "when helpful. Tool results are example data, not live booking "
            "information. Never invent current prices, opening hours, visa "
            "rules or availability. Ask a concise follow-up if needed."
        ),
    )
    result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    return result["messages"][-1].content

@app.post("/ask")
async def ask(q: Question):
    answer = await ask_agent(q.question)
    return {"answer": answer}

@app.get("/")
async def root():
    return FileResponse(Path(__file__).parent / "index.html")

@app.get("/health")
async def health():
    return {"status": "Travel Planner API is running. Send a question to /ask."}
