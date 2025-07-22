# tests/conftest.py
import pytest

# Define common constants or helpers for tests here
@pytest.helpers.register
def get_expected_validation_task():
    """Returns the exact validation task string used in agent_runner."""
    return (
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

# To register the helper, you might need:
# pip install pytest-helpers
# or just define a regular function and import it.