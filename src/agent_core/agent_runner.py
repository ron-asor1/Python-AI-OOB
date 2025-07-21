# src/agent_core/agent_runner.py
import asyncio
import os
import logging

from browser_use.agent.service import Agent
from src.agent_core.llm_setup import initialize_llm # Import from your new module
from src.utils.logger_setup import setup_logging    # Import your logging setup

logger = logging.getLogger(__name__) # Logger for this specific module

async def run_site_validation() -> None:
    """
    Orchestrates the browser automation task for site validation
    using a Google Generative AI model.
    """
    logger.info("Starting site validation process...")

    # Optional: Set to "0" to show the browser window, or "1" for headless (no visible window).
    # This can be overridden by environment variables (e.g., in GitHub Actions)
    # Convert string "1" or "0" from environment to boolean True/False
    browser_headless_env = os.getenv("BROWSER_USE_HEADLESS", "0") # Default to '0' (headed) locally
    os.environ["BROWSER_USE_HEADLESS"] = browser_headless_env
    logger.info(f"BROWSER_USE_HEADLESS set to: {browser_headless_env} (0=headed, 1=headless)")

    # Optional: Disable browser_use telemetry for cleaner logs in local development/CI
    telemetry_enabled_env = os.getenv("BROWSER_USE_TELEMETRY_ENABLED", "1") # Default to '1' (enabled)
    os.environ["BROWSER_USE_TELEMETRY_ENABLED"] = telemetry_enabled_env
    logger.info(f"BROWSER_USE_TELEMETRY_ENABLED set to: {telemetry_enabled_env}")


    validation_task = (
        "Important: I am UI automation tester performing validations. "
        "Open Website https://www.saucedemo.com/. "
        "Login with any given username and password on the first page. "
        "Post login, select any single product and add to cart. "
        "Press checkout. "
        "Store the total value of the order. "
        "Fill any details for firstname, lastname and zipcode. "
        "Press next. "
        "Press finish. "
        "Validate the message showing: Thank you for your order! "
        "Validate a Back Home button showing as well."
    )

    llm = initialize_llm() # Use your new LLM setup function
    logger.info("LLM initialized successfully for agent.")

    try:
        # NOTE: If you still encounter the 'ainvoke' Pydantic error,
        # you might need to revert to the manual patch/source modification
        # for browser_use.
        agent = Agent(task=validation_task, llm=llm, use_vision=True)
        logger.info("BrowserUse Agent initialized.")

        logger.info("🚀 Running site validation agent...")
        history = await agent.run()
        logger.info("\n✅ Final result:")
        final_result = history.final_result()
        logger.info(final_result)
        print(f"\nFinal Agent Result: {final_result}") # Also print for immediate console visibility
    except Exception as e:
        logger.exception(f"❌ An error occurred during agent execution: {e}")
        print(f"\n❌ An error occurred during agent execution: {e}") # Print error for immediate visibility

# Main execution block
if __name__ == "__main__":
    setup_logging() # Configure logging first
    asyncio.run(run_site_validation())