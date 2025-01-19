"""
Chatbot package for CLI-based AI interactions
"""

from .models import get_model
from .agent import ChatAgent
from .cli import ChatCLI
from .tools import ChatTools

# Version of the chatbot package
__version__ = "0.1.0"

# Expose key classes and functions at package level
__all__ = [
    'get_model',
    'ChatAgent',
    'ChatCLI',
    'ChatTools'
] 