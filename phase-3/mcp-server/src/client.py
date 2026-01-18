import json
import asyncio
from typing import Optional
from mcp import ClientSession
from contextlib import AsyncExitStack
from mcp.client.streamable_http import streamable_http_client
from mcp.types import( ListToolsResult, CallToolResult)

class MCPClient:
    def __init__(self, server_url):
        self._server_url : str = server_url
        self._session: Optional[ClientSession] = None
        self._exit_stack:AsyncExitStack= AsyncExitStack()

    async def connection(self):
        _read, _write, _ = await self._exit_stack.enter_async_context(
            streamable_http_client(self._server_url)
        )
        self._session = await self._exit_stack.enter_async_context(
            ClientSession(_read,_write)
        )
        await self._session.initialize()
        return self._session
    
    async def Cleanup(self):
        await self._exit_stack.aclose()

    async def __aenter__(self):
        await self.connection()
        return self
    
    async def __aexit__(self,*args):
        await self.Cleanup()
        self._session = None

    # Tools
    async def tool_list(self)-> ListToolsResult:
        assert self._session, "Session Not Found"
        res = await self._session.list_tools()
        return res.tools
    
    async def tool_call(self, tool_name:str, arguments:dict[str,any])->CallToolResult:
        assert self._session, "Session Not Found"
        res = await self._session.call_tool(name=tool_name, arguments=arguments)
        return res.content
    
   

async def main():
    async with MCPClient("http://localhost:8001/mcp") as client:
        print("-"*100)
        auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzY4NzI2MTcyfQ._7ntnVJDJO1MwRjtTVUUN5fw1yBjKQRm4Sh4SFDuAQM"
        
        tool_list = await client.tool_list()
        for tool in tool_list:
            print(tool.name)
    
        list_tasks = await client.tool_call("list_tasks", arguments={"status":"all", "auth_token":auth_token})
        for tasks in list_tasks:
            print(tasks.text, "/n")

        post_task = await client.tool_call("add_task", arguments={"title":"MCP Testing Adding", "description":"Testting mcp tool by posting Tasks", "auth_token":auth_token})
        print(post_task)

        update_task = await client.tool_call("update_task", arguments={"task_id":"668f9e1c-e36b-4552-9084-fae98dc9de75","title":"change to Hello", "description":"Testting mcp tool by posting Tasks", "auth_token":auth_token})
        print(update_task)

        complete_task = await client.tool_call("complete_task", arguments={"task_id":"49796900-7a5e-4414-bb73-15e9b346d000", "auth_token":auth_token})
        print(complete_task)

        delete_task = await client.tool_call("delete_task", arguments={"task_id":"07f70962-2763-4f48-b81c-b744e7016595", "auth_token":auth_token})
        print(delete_task)
        
        
asyncio.run(main())