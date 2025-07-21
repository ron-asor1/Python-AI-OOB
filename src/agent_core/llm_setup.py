# src/agent_core/llm_setup.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
import logging

logger = logging.getLogger(__name__)

def initialize_llm():
    """
    Loads environment variables and initializes the Google Generative AI model.
    """
    load_dotenv() # Load .env file

    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        logger.error("GOOGLE_API_KEY environment variable not set. Please set it in your .env file or system environment.")
        raise ValueError("GOOGLE_API_KEY environment variable not set. "
                         "Please set it in your .env file.")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        api_key=SecretStr(google_api_key)
    )
    logger.info("Google Generative AI LLM initialized.")
    return llm