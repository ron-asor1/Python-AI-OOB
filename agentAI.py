import asyncio
import os
from dotenv import load_dotenv

from browser_use.agent.service import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
from typing import Any

load_dotenv()

class BrowserUseGoogleGenerativeAI(ChatGoogleGenerativeAI):
    pass

async def run_site_validation() -> None:
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set. "
                         "Please set it in your .env file.")

    os.environ["BROWSER_USE_HEADLESS"] = "0" # Show browser window
    os.environ["BROWSER_USE_TELEMETRY_ENABLED"] = "0"

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

    llm = BrowserUseGoogleGenerativeAI(
        model="gemini-2.0-flash",
        api_key=SecretStr(google_api_key)
    )

    print("🚀 Running site validation agent...\n")
    try:
        agent = Agent(task=validation_task, llm=llm, use_vision=True)
        history = await agent.run()
        print("\n✅ Final result:")
        print(history.final_result())
    except Exception as e:
        print(f"\n❌ An error occurred during agent execution: {e}")

if __name__ == "__main__":
    asyncio.run(run_site_validation())