"""
Tests for the hello module.

This test suite verifies the correctness of the hello function.
"""
from hello import hello

def test_hello():
    """
    Test that the hello function correctly formats the greeting.
    """
    assert hello("world") == "hello world"
    assert hello("guru") == "hello guru"
