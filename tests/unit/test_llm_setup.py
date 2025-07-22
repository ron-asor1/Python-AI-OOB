# tests/unit/test_llm_setup.py
import pytest
from unittest.mock import patch, MagicMock
from src.agent_core.llm_setup import initialize_llm
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

@patch('os.getenv')
def test_initialize_llm_with_key(mock_getenv):
    """
    Tests that initialize_llm successfully creates an LLM instance when GOOGLE_API_KEY is present.
    """
    mock_getenv.side_effect = lambda key, default=None: "TEST_API_KEY" if key == "GOOGLE_API_KEY" else default

    # Mock the ChatGoogleGenerativeAI constructor to avoid actual instantiation
    with patch('src.agent_core.llm_setup.ChatGoogleGenerativeAI') as MockChatGoogleGenerativeAI:
        llm_instance = initialize_llm()

        # Assert that os.getenv was called for the key
        mock_getenv.assert_called_with("GOOGLE_API_KEY")

        # Assert that ChatGoogleGenerativeAI was called with the correct parameters
        MockChatGoogleGenerativeAI.assert_called_once_with(
            model="gemini-2.0-flash",
            api_key=SecretStr("TEST_API_KEY")
        )
        # Assert that the function returned the mocked LLM instance
        assert llm_instance is MockChatGoogleGenerativeAI.return_value

@patch('os.getenv')
def test_initialize_llm_without_key(mock_getenv):
    """
    Tests that initialize_llm raises a ValueError when GOOGLE_API_KEY is missing.
    """
    mock_getenv.side_effect = lambda key, default=None: None if key == "GOOGLE_API_KEY" else default

    with pytest.raises(ValueError) as excinfo:
        initialize_llm()

    assert "GOOGLE_API_KEY environment variable not set" in str(excinfo.value)
    mock_getenv.assert_called_with("GOOGLE_API_KEY")