"""
Quick start guide for the Enterprise Research Agent.
"""

import asyncio
from app.graph.workflow import ResearchAgentGraph
from app.utils.logging import logger


async def quickstart():
    """
    Quick start example.
    """
    # Initialize graph
    graph = ResearchAgentGraph()
    
    # Define research question
    question = "What are the key differences between LangGraph and CrewAI?"
    
    # Execute research
    logger.info(f"Researching: {question}")
    state = await graph.execute(question)
    
    # Display results
    print("\n" + "="*80)
    print("RESEARCH RESULTS")
    print("="*80)
    
    print(f"\nQuestion: {state.question}")
    print(f"\nFinal Answer:\n{state.final_answer}")
    
    if state.critic_feedback:
        print(f"\nQuality Assessment:")
        print(f"  Status: {state.critic_feedback.status}")
        print(f"  Completeness: {state.critic_feedback.completeness_score:.2f}")
        print(f"  Factual Consistency: {state.critic_feedback.factual_consistency_score:.2f}")
        print(f"  Clarity: {state.critic_feedback.clarity_score:.2f}")
    
    print(f"\nExecution Metrics:")
    print(f"  Total Duration: {state.execution_metrics.get('total_duration', 0):.2f}s")
    print(f"  Tool Calls: {state.execution_metrics.get('tool_calls', 0)}")
    print(f"  Retries: {state.execution_metrics.get('retry_count', 0)}")


if __name__ == "__main__":
    asyncio.run(quickstart())
