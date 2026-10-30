import asyncio
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

async def main():
    mcp_url = os.getenv("MCP_URL", "http://127.0.0.1:8000/mcp")
    api_key = os.getenv("GROQ_API_KEY")
    model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    if not api_key:
        raise RuntimeError("Set GROQ_API_KEY in .env first.")

    # Connect to the running MCP server over Streamable HTTP.
    client = MultiServerMCPClient({
        "travel": {
            "transport": "http",
            "url": mcp_url,
        }
    })

    # Discover the tools exposed by the MCP server.
    tools = await client.get_tools()
    print("Discovered MCP tools:")
    for tool in tools:
        print(f" - {tool.name}: {tool.description}")

    model = ChatGroq(
        model=model_name,
        temperature=0,
        api_key=api_key,
    )

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

    question = input("Enter your travel question: ")
    result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    print("\nAgent answer:\n")
    print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
