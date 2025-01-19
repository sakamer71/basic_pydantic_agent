from typing import Any
from pydantic_ai import Agent, RunContext
from .tools import ChatTools
from .config import SYSTEM_PROMPTS, TOOL_DESCRIPTIONS

class ChatAgent:
    def __init__(self, model: Any, prompt_type: str = 'default'):
        self.agent = Agent(
            model=model,
            system_prompt=SYSTEM_PROMPTS[prompt_type]
        )
        self._register_tools()
        
    def _register_tools(self):
        """Register all tools with the agent"""
        tools = ChatTools()
        
        # Register each tool with its description from config
        for tool_name, description in TOOL_DESCRIPTIONS.items():
            tool_method = getattr(tools, tool_name, None)
            if tool_method:
                # Update the tool's docstring with the configured description
                tool_method.__doc__ = description
                self.agent.tool_plain(tool_method)
        
    def chat(self, message: str, context: RunContext = None) -> RunContext:
        """Process a chat message and return the response"""
        if context:
            return self.agent.run_sync(message, message_history=context.all_messages())
        return self.agent.run_sync(message) 