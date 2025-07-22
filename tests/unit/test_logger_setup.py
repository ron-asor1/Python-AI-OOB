# tests/unit/test_logger_setup.py
import pytest
import logging
import os
from unittest.mock import patch, MagicMock

from src.utils.logger_setup import setup_logging
@pytest.fixture(autouse=True)
def clean_loggers():
    """Fixture to clean up loggers before and after each test."""
    # Clean up handlers before test
    for handler in logging.getLogger().handlers[:]:
        logging.getLogger().removeHandler(handler)
    yield
    # Clean up handlers after test
    for handler in logging.getLogger().handlers[:]:
        logging.getLogger().removeHandler(handler)


@patch('os.makedirs') # Mock makedirs to prevent actual folder creation during test
@patch('logging.FileHandler') # Mock FileHandler to prevent actual file creation
def test_setup_logging_configures_handlers(mock_file_handler, mock_makedirs):
    """
    Tests that setup_logging adds console and file handlers correctly.
    """
    setup_logging()

    root_logger = logging.getLogger()
    assert root_logger.level == logging.INFO

    # Check for console handler
    console_handler_found = False
    for handler in root_logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            console_handler_found = True
            assert handler.level == logging.INFO
            # Can also assert on formatter if needed: isinstance(handler.formatter, logging.Formatter)
            break
    assert console_handler_found, "Console handler not found"

    # Check for file handler (mocked)
    mock_file_handler.assert_called_once()
    # You can inspect the call args if needed, e.g., mock_file_handler.call_args[0][0] for path

    # Check os.makedirs was called for the log directory
    mock_makedirs.assert_called_once_with("data/logs", exist_ok=True)

@patch('os.makedirs')
@patch('logging.FileHandler')
def test_setup_logging_removes_existing_handlers(mock_file_handler, mock_makedirs):
    """
    Tests that setup_logging removes existing handlers before adding new ones.
    """
    # Add a dummy handler
    dummy_handler = logging.StreamHandler()
    logging.getLogger().addHandler(dummy_handler)
    assert len(logging.getLogger().handlers) == 1

    setup_logging()
    # After setup_logging, the dummy handler should be gone and new ones added
    assert len(logging.getLogger().handlers) == 2 # Console + (mocked) File

    # Ensure the dummy handler is not among the new ones (by checking it's been removed)
    assert dummy_handler not in logging.getLogger().handlers
