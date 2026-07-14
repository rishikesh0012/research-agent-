"""Extended type hints and protocol definitions."""

from typing import Protocol, Any, Dict
from app.models import ToolOutput, AgentState


class Tool(Protocol):
    """Protocol for tool implementations."""
    
    async def execute(self, **kwargs: Any) -> ToolOutput:
        """Execute tool with given parameters."""
        ...


class Agent(Protocol):
    """Protocol for agent implementations."""
    
    async def process(self, state: AgentState) -> AgentState:
        """Process agent step."""
        ...
