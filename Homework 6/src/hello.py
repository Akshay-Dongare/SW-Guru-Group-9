"""
Main hello module for Homework 6.

This module provides a very simple function to demonstrate packaging,
testing, and automated documentation generation in Python.
"""

def hello(x: str) -> str:
    """
    Returns a greeting string.

    Args:
        x (str): The name or subject to greet.

    Returns:
        str: A string in the format "hello {x}".
    """
    return f"hello {x}"
