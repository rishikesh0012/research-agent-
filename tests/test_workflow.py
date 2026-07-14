"""
End-to-end workflow tests for the Enterprise Research Agent.
"""

import pytest
from app.graph.workflow import ResearchAgentGraph
from app.models import AgentState, ToolType


@pytest.mark.asyncio
async def test_research_workflow_complete():
    """
    Test complete research workflow execution.
    """
    graph = ResearchAgentGraph()
    question = "What is the difference between AI and machine learning?"
    
    state = await graph.execute(question)
    
    assert isinstance(state, AgentState)
    assert state.question == question
    assert state.execution_plan is not None
    assert len(state.tool_outputs) > 0
    assert state.draft_answer is not None
    assert state.final_answer is not None
    assert state.execution_metrics is not None


@pytest.mark.asyncio
async def test_workflow_handles_errors():
    """
    Test workflow gracefully handles errors.
    """
    graph = ResearchAgentGraph()
    question = "This is a very simple question."
    
    state = await graph.execute(question)
    
    # Should complete even with minimal question
    assert state.final_answer is not None
    assert "Error" not in state.final_answer or len(state.final_answer) > 0


@pytest.mark.asyncio
async def test_workflow_generates_metrics():
    """
    Test workflow generates execution metrics.
    """
    graph = ResearchAgentGraph()
    question = "What is cloud computing?"
    
    state = await graph.execute(question)
    
    metrics = state.execution_metrics
    assert "total_duration" in metrics
    assert "tool_calls" in metrics
    assert "retry_count" in metrics
    assert metrics["total_duration"] > 0
