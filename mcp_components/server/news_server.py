"""
MCP Server component that provides news tools via FastMCP.
"""
from typing import Literal

from fastmcp import FastMCP
from newsapi import NewsApiClient

from mcp_components.config.settings import settings
from mcp_components.utils.logger import setup_logger

logger = setup_logger(__name__)

mcp = FastMCP("news")
newsapi = NewsApiClient(api_key=settings.news_api_key)


@mcp.tool()
def fetch_news(query: str) -> dict[str, str]:
    """
        Get news articles related to the query.

        Args:
            query: User query

        Returns:
            Dictionary containing news articles
        """
    logger.info(f"Fetched news for {query}")
    response = newsapi.get_everything(q=query, language='en')
    logger.info(f"News response: {response}")
    return response



def run_server(host: str = "127.0.0.1", port: int = 7861, transport: Literal["stdio", "sse", "streamable-http"] = "sse") -> None:
    """
    Run the MCP server with specified transport, host and port.

    Args:
        host: Host address to bind the server
        port: Port number to listen on
        transport: Transport protocol ("sse" or "stdio")
    """
    logger.info(f"Starting MCP server on {host}:{port} with {transport} transport...")
    mcp.run(transport=transport, host=host, port=port)


if __name__ == "__main__":
    run_server()
