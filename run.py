# run.py
import asyncio
import logging
from src.agent_core.agent_runner import run_site_validation
from src.utils.logger_setup import setup_logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    setup_logging() # Ensure logging is set up for the main execution
    logger.info("Application started via run.py")
    asyncio.run(run_site_validation())