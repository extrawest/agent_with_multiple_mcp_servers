from contextlib import AsyncExitStack
from typing import List, Any
import asyncio

from mcp import ClientSession
from mcp.client.sse import sse_client
from langchain_mcp_adapters.tools import load_mcp_tools

from mcp_components.utils.logger import setup_logger

logger = setup_logger(__name__)


class MCPClientWrapper:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.session = None
        self.tools = []
        self._cleanup_lock: asyncio.Lock = asyncio.Lock()
        self.exit_stack: AsyncExitStack = AsyncExitStack()
        
    async def connect(self) -> None:
        mcp_path = "/sse"
        logger.info(f"Connecting to MCP server at {self.server_url}{mcp_path}")
        
        try:
            (read, write) = await self.exit_stack.enter_async_context(sse_client(f"{self.server_url}{mcp_path}"))
            session = await self.exit_stack.enter_async_context(ClientSession(read, write))

            self.session = session
            await self.session.initialize()
            logger.info("MCP session initialized successfully")
        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {str(e)}")
            raise
    
    async def load_tools(self) -> List[Any]:
        try:
            logger.info("Loading MCP tools...")
            self.tools = await load_mcp_tools(self.session)
            tool_names = [tool.name for tool in self.tools]
            logger.info(f"Loaded {len(self.tools)} tools: {tool_names}")
            return self.tools
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            logger.error(f"Failed to load tools: {str(e)}\n{error_details}")
            return []
    
    async def close(self) -> None:
        async with self._cleanup_lock:
            try:
                await self.exit_stack.aclose()
                self.session = None
            except Exception as e:
                logger.info("Error during cleanup: %s", str(e))
