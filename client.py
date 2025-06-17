from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_aws import ChatBedrockConverse
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["mathserver.py"],  # Ensure correct absolute path
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8000/mcp",  # Ensure server is running here
                "transport": "streamable_http",
            },
            "firecrawl": {
                "command": "python",
                "args": ["firecrawl_server.py"],  # New Firecrawl MCP server
                "transport": "stdio",
            }
        }
    )

    # Get tools from all MCP servers
    tools = await client.get_tools()
    
    # Initialize Bedrock model instead of Groq
    model = ChatBedrockConverse(
        model_id="eu.anthropic.claude-3-7-sonnet-20250219-v1:0",  # or any other Bedrock model
        temperature=0.1,
        credentials_profile_name=os.getenv("AWS_PROFILE"),  # Use AWS profile from env
        region_name=os.getenv("AWS_REGION", "us-east-1"),   # Default to us-east-1 if not specified
    )
    
    # Create agent with Bedrock model and all tools
    agent = create_react_agent(model, tools)

    print("🧮 Testing Math Server...")
    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    )
    print("Math response:", math_response['messages'][-1].content)

    print("\n🌤️ Testing Weather Server...")
    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in Berlin?"}]}
    )
    print("Weather response:", weather_response['messages'][-1].content)

    print("\n🔥 Testing Firecrawl Server...")
    firecrawl_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "Search for 'Python web scraping tools' and give me the top 3 results"}]}
    )
    print("Firecrawl response:", firecrawl_response['messages'][-1].content)

    print("\n🕷️ Testing Firecrawl Scraping...")
    scrape_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "Scrape the content from https://python.org and summarize what Python is"}]}
    )
    print("Scrape response:", scrape_response['messages'][-1].content)

if __name__ == "__main__":
    asyncio.run(main())