from typing import List, Any, Tuple, Dict

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from mcp_components.client.client import MCPClientWrapper
from mcp_components.config.settings import settings
from mcp_components.utils.logger import setup_logger

logger = setup_logger(__name__)


class AgentRunner:
    def __init__(self, model_name: str = "gpt-4o"):
        self.model_name = model_name
        self.model = ChatOpenAI(model=model_name, api_key=settings.openai_api_key)
        self.agent = None
        self.tools = []
        self.clients = []
        
    async def setup_with_multiple_mcp_servers(self, server_configs: List[Dict[str, str]]) -> None:
        all_tools = []
        
        for config in server_configs:
            server_url = config.get("url")
            
            logger.info(f"Connecting to server at {server_url}")

            client, tools = await get_mcp_client(server_url)
            
            if client:
                self.clients.append(client)
                
                if tools:
                    logger.info(f"Loaded {len(tools)} tools from {server_url}")
                    all_tools.extend(tools)
                else:
                    logger.warning(f"No tools were loaded from {server_url}")
            else:
                logger.warning(f"Could not establish connection to {server_url}")
        
        if all_tools:
            self.tools = all_tools
            self.agent = create_react_agent(self.model, self.tools)
            logger.info(f"LangChain agent created successfully with {len(all_tools)} tools")
        else:
            logger.error("No tools were loaded from any server, agent cannot be created")
    
    async def run_query(self, query: str) -> Dict[str, Any]:
        if not self.agent:
            raise RuntimeError("Agent not initialized. Call setup_with_mcp_tools() first.")
            
        logger.info(f"Running query: {query}")
        response = await self.agent.ainvoke({"messages": query})
        logger.info("Query completed successfully")
        return response
    
    async def cleanup(self) -> None:
        clients_to_close = list(reversed(self.clients))
        for client in clients_to_close:
            if client:
                try:
                    await client.close()
                except Exception as e:
                    logger.error(f"Error closing client: {str(e)}")
        
        logger.info(f"Closed {len(self.clients)} MCP client connections")
        self.clients = []

async def get_mcp_client(server_url: str) -> Tuple[MCPClientWrapper, List[Any]]:
    client = MCPClientWrapper(server_url)
    await client.connect()
    tools = await client.load_tools()
    return client, tools

