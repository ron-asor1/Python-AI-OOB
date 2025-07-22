# tests/integration/test_agent_first_step.py
import pytest
import asyncio
from unittest.mock import patch, AsyncMock, MagicMock
import logging

from src.agent_core.agent_runner import run_site_validation
from src.agent_core.llm_setup import initialize_llm
from browser_use.agent.service import Agent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

@pytest.mark.asyncio
@patch('src.agent_core.llm_setup.initialize_llm') # Mock LLM setup
@patch('browser_use.agent.service.Agent')        # Mock the Agent class itself
async def test_agent_attempts_initial_page_open(mock_agent_cls, mock_initialize_llm):
    """
    Tests that the agent is initialized and attempts to open the initial URL.
    Mocks the LLM and the Agent's run method to control behavior.
    """
    logger.info("\n--- Running Integration Test: Agent Initial Page Open ---")

    # Configure mocks
    mock_llm_instance = MagicMock()
    mock_initialize_llm.return_value = mock_llm_instance

    mock_agent_instance = AsyncMock() # Agent.run() is async, so mock it with AsyncMock
    mock_agent_cls.return_value = mock_agent_instance

    # Mock the history object that agent.run() returns
    mock_history = MagicMock()
    mock_history.final_result.return_value = "Mocked final result: Agent attempted opening URL."
    mock_agent_instance.run.return_value = mock_history

    # Call the function that sets up and runs the agent
    await run_site_validation()

    # Assertions
    mock_initialize_llm.assert_called_once() # LLM should have been initialized

    # Agent should have been instantiated with the task and LLM
    mock_agent_cls.assert_called_once_with(
        task=pytest.helpers.get_expected_validation_task(), # Helper to get task string
        llm=mock_llm_instance,
        use_vision=True
    )

    # Agent's run method should have been called
    mock_agent_instance.run.assert_awaited_once()

    logger.info("--- Integration Test: Agent Initial Page Open PASSED ---")