import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, ModelSettings, set_tracing_export_api_key
from agents.mcp import MCPServerStreamableHttp,MCPServerStreamableHttpParams

client = AsyncOpenAI(
    api_key="GEMINI_API_KEY_HERE",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(
    model ="gemini-2.5-flash",
    openai_client=client
)
config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=False
)


async def main(user_input:str)-> str:
    mcpparams = MCPServerStreamableHttpParams(url="http://127.0.0.1:8001/mcp/")
    async with MCPServerStreamableHttp(name="mcp-server",params=mcpparams) as server:
        agent = Agent(
            name="Assiatant",
            instructions="You are a helpful Assistant.",
            mcp_servers=[server],
            model_settings=ModelSettings(tool_choice="auto"),
        )
        result = await  Runner.run(agent, user_input, run_config=config)
        print(result.final_output)
    

asyncio.run(main("List my tasks using the MCP tools and this is the auth_token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzY4NzMyMTM3fQ.0tngGq1mdcdJPYnrimnxMpMMwhmcE4C_4mf4GBnlWJM you will need it to send request."))