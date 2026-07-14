"""
Tests for agent components.
"""

import pytest
from app.agents import PlannerAgent, WriterAgent, CriticAgent, RewriterAgent
from app.models import ExecutionPlan


@pytest.mark.asyncio
async def test_planner_agent():
    """Test planner agent creates valid plan."""
    planner = PlannerAgent()
    question = "What is artificial intelligence?"
    
    plan = await planner.plan(question)
    
    assert isinstance(plan, ExecutionPlan)
    assert plan.question == question
    assert plan.total_steps > 0
    assert len(plan.steps) > 0
    assert all(step.step_id for step in plan.steps)


@pytest.mark.asyncio
async def test_writer_agent():
    """Test writer agent generates report."""
    writer = WriterAgent()
    question = "What is machine learning?"
    research_data = {
        "search_1": {
            "results": [
                {
                    "title": "Machine Learning Overview",
                    "content": "Machine learning is a subset of AI"
                }
            ]
        }
    }
    
    report = await writer.write_report(question, research_data)
    
    assert isinstance(report, str)
    assert len(report) > 0


@pytest.mark.asyncio
async def test_critic_agent():
    """Test critic agent evaluates report."""
    critic = CriticAgent()
    question = "What is AI?"
    report = "# AI Report\n\nArtificial Intelligence is a field of computer science."
    
    feedback = await critic.critique(question, report)
    
    assert feedback.status in ["PASS", "FAIL"]
    assert 0 <= feedback.completeness_score <= 1
    assert 0 <= feedback.factual_consistency_score <= 1
    assert 0 <= feedback.clarity_score <= 1
