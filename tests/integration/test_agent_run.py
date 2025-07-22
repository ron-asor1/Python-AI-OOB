# src/agent_core/agent_runner.py
import asyncio
import os
import logging

from browser_use.agent.service import Agent
from src.agent_core.llm_setup import initialize_llm
from src.utils.logger_setup import setup_logging # Keep this, as the main script will still use it
from src.utils.constants import VALIDATION_TASK # <--- NEW IMPORT

logger = logging.getLogger(__name__)

async def run_site_validation() -> None:
    """
    Orchestrates the browser automation task for site validation
    using a Google Generative AI model.
    """
    logger.info("Starting site validation process...")

    # Optional: Set to "0" to show the browser window, or "1" for headless (no visible window).
    # This can be overridden by environment variables (e.g., in GitHub Actions)
    browser_headless_env = os.getenv("BROWSER_USE_HEADLESS", "0")
    os.environ["BROWSER_USE_HEADLESS"] = browser_headless_env
    logger.info(f"BROWSER_USE_HEADLESS set to: {browser_headless_env} (0=headed, 1=headless)")

    telemetry_enabled_env = os.getenv("BROWSER_USE_TELEMETRY_ENABLED", "1")
    os.environ["BROWSER_USE_TELEMETRY_ENABLED"] = telemetry_enabled_env
    logger.info(f"BROWSER_USE_TELEMETRY_ENABLED set to: {telemetry_enabled_env}")

    llm = initialize_llm()
    logger.info("LLM initialized successfully for agent.")

    try:
        agent = Agent(task=VALIDATION_TASK, llm=llm, use_vision=True)
        logger.info("BrowserUse Agent initialized.")

        logger.info("🚀 Running site validation agent...")
        history = await agent.run()
        logger.info("\n✅ Final result:")
        final_result = history.final_result()
        logger.info(final_result)
        print(f"\nFinal Agent Result: {final_result}")
    except Exception as e:
        logger.exception(f"❌ An error occurred during agent execution: {e}")
        print(f"\n❌ An error occurred during agent execution: {e}")


# No if __name__ == "__main__": block here.
# The main entry point for running the application will be a separate script
# (e.g., a new 'main.py' or a 'run.py' in the project root if desired).
# Or, you can make agent_runner.py executable directly if it returns to its own main.
# For now, we'll keep the module execution via 'python -m ...'