"""
MCP Server component that provides stock-related tools via FastMCP.
"""
from typing import Dict, Any, Literal

import yfinance as yf
from fastmcp import FastMCP
from pandas import DataFrame

from mcp_components.utils.logger import setup_logger

logger = setup_logger(__name__)

mcp = FastMCP("stocks")


@mcp.tool()
def fetch_stock_info(symbol: str) -> Dict[str, Any]:
    """
    Get Company's general information.
    
    Args:
        symbol: Stock ticker symbol
        
    Returns:
        Dictionary containing company information
    """
    logger.info(f"Fetching stock info for {symbol}")
    stock = yf.Ticker(symbol)
    return stock.info


@mcp.tool()
def fetch_quarterly_financials(symbol: str) -> DataFrame:
    """
    Get stock quarterly financials.
    
    Args:
        symbol: Stock ticker symbol
        
    Returns:
        DataFrame with quarterly financial data
    """
    logger.info(f"Fetching stock quarterly financials for {symbol}")
    stock = yf.Ticker(symbol)
    return stock.quarterly_financials.T


@mcp.tool()
def fetch_annual_financials(symbol: str) -> DataFrame:
    """
    Get stock annual financials.
    
    Args:
        symbol: Stock ticker symbol
        
    Returns:
        DataFrame with annual financial data
    """
    logger.info(f"Fetching stock annual financials for {symbol}")
    stock = yf.Ticker(symbol)
    return stock.financials.T


def run_server(host: str = "127.0.0.1", port: int = 7860, transport: Literal["stdio", "sse", "streamable-http"] = "sse") -> None:
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
