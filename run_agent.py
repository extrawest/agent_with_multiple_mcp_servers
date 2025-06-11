import asyncio

from mcp_components.agent.agent import AgentRunner
from mcp_components.utils.logger import setup_logger

logger = setup_logger(__name__)


async def run_agent_with_multiple_servers():
    logger.info("Starting agent runner...")
    agent_runner = AgentRunner()

    try:
        server_configs = [
            {"url": "http://127.0.0.1:7860"},
            {"url": "http://127.0.0.1:7861"}
        ]

        await agent_runner.setup_with_multiple_mcp_servers(server_configs)

        if agent_runner.agent:
            query = "Summarize AAPL financials and analyze sentiment of recent news about the company"
            response = await agent_runner.run_query(query)

            logger.info("\n=== LANGCHAIN AGENT RESPONSE ===")
            logger.info(response)
        else:
            logger.error("Agent was not initialized properly, cannot run query")
    except Exception as e:
        logger.error(f"Error running agent: {str(e)}")
    finally:
        await agent_runner.cleanup()

    logger.info("Agent runner completed")


if __name__ == "__main__":
    asyncio.run(run_agent_with_multiple_servers())
