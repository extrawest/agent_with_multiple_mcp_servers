# 🤖 MCP Agent Framework

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)]()
[![Maintainer](https://img.shields.io/static/v1?label=Yevhen%20Ruban&message=Maintainer&color=red)]()
[![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)]()
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![GitHub release](https://img.shields.io/badge/release-v1.0.0-blue)

A modular system for creating AI agents using the Model Context Protocol (MCP). This framework allows connecting to multiple MCP servers simultaneously, aggregating tools, and executing queries using LangChain agents.

## 🌟 Features

- 🔌 **Multi-server Connection**: Connect to multiple MCP servers simultaneously
- 🛠️ **Tool Aggregation**: Automatically collect and combine tools from all connected servers
- 🤖 **LangChain Integration**: Create React agents using the LangChain library
- 🔄 **Asynchronous Processing**: Fully asynchronous code with proper resource management
- 🧠 **OpenAI Integration**: Seamless integration with OpenAI models for intelligent agent responses
- 📊 **Detailed Logging**: Comprehensive logging of all operational stages for debugging
- 🧩 **Modular Architecture**: Clear separation into client and agent components

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/extrawest/agent_with_multiple_mcp_servers.git
cd agent_with_multiple_mcp_servers

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

### 3. Start MCP Servers

Before running the agent, you need to start the MCP servers. The project includes two different servers:

#### Stocks Server
Provides financial data tools using yfinance:
```bash
# Start the stocks server on port 7860
python -m mcp_components.server.stocks_server
```

#### News Server
Provides news retrieval tools using NewsAPI:
```bash
# Start the news server on port 7861
python -m mcp_components.server.news_server
```

### 4. Run the Agent

Once the servers are running, you can start the agent:
```bash
# Run the agent with connections to both MCP servers
python run_agent.py
```

### 5. Cursor IDE Integration

You can add the MCP servers to Cursor IDE by adding the following configuration to your Cursor settings:

```json
{
  "mcpServers": {
    "stocks-mcp-server": {
      "url": "http://127.0.0.1:7860/sse"
    },
    "news-mcp-server": {
      "url": "http://127.0.0.1:7861/sse"
    } 
  }
}
```

Make sure both servers are running before connecting through Cursor IDE.

## 📦 Project Structure

```
mcp_components/
├── agent/
│   └── agent.py       # AgentRunner implementation for working with MCP servers
├── client/
│   └── client.py      # Client for connecting to MCP servers
├── server/
│   ├── stocks_server.py  # MCP server providing stock market tools
│   └── news_server.py    # MCP server providing news retrieval tools
```

## 💻 Usage

### Direct MCP Client Usage

```python
from mcp_components.client.client import MCPClientWrapper
from typing import List, Any, Tuple

async def get_mcp_client(server_url: str) -> Tuple[MCPClientWrapper, List[Any]]:
    client = MCPClientWrapper(server_url)
    await client.connect()
    tools = await client.load_tools()
    return client, tools
```

## 🔧 Components

### AgentRunner

Class for creating and managing agents that can use tools from multiple MCP servers:

- `setup_with_multiple_mcp_servers()`: Connect to multiple MCP servers and aggregate tools
- `run_query()`: Execute a query using the agent
- `cleanup()`: Close all connections and free resources

### MCPClientWrapper

Class for connecting to MCP servers and loading tools:

- `connect()`: Establish a connection with an MCP server
- `load_tools()`: Load available tools from the server
- `close()`: Close the connection to the server

### MCP Servers

The framework includes two specialized MCP servers:

#### Stocks Server
- Provides financial data tools using yfinance
- Runs on port 7860 by default
- Tools:
  - `fetch_stock_info`: Get general company information
  - `fetch_quarterly_financials`: Get quarterly financial data
  - `fetch_annual_financials`: Get annual financial data

#### News Server
- Provides news retrieval tools using NewsAPI
- Runs on port 7861 by default
- Tools:
  - `fetch_news`: Get news articles related to a query

## 📋 Requirements

- Python 3.9+
- MCP 1.9.3+
- LangChain
- OpenAI API key (for using OpenAI models)
- NewsAPI key (for the news server)
- yfinance (for the stocks server)

## 🔍 Implementation Details

- **Asynchronous Context Managers**: Proper management of asynchronous resources using `AsyncExitStack`
- **Error Handling**: Robust exception handling at all levels
- **Connection Preservation**: Maintaining active connections for tool usage
- **Tool Aggregation**: Combining tools from different servers into a unified list
