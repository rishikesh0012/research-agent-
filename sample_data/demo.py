"""
Utility script to demonstrate research agent capabilities.
"""

import asyncio
import json
from datetime import datetime

from app.graph.workflow import ResearchAgentGraph
from app.evaluation.evaluator import ExecutionEvaluator
from app.utils.logging import logger


async def demo_research():
    """
    Run demonstration research tasks.
    """
    logger.info("Starting Enterprise Research Agent Demo")
    
    graph = ResearchAgentGraph()
    evaluator = ExecutionEvaluator()
    
    # Example research questions
    questions = [
        "What are the key differences between LangGraph and CrewAI for building production AI agents?",
        "Explain how retrieval-augmented generation (RAG) works and its applications.",
        "What are the current trends in AI agent frameworks in 2024?"
    ]
    
    results = []
    
    for i, question in enumerate(questions, 1):
        logger.info(f"\nResearch Task {i}/3: {question}")
        print(f"\n{'='*80}")
        print(f"Task {i}: {question}")
        print(f"{'='*80}")
        
        try:
            # Execute research
            state = await graph.execute(question)
            
            # Evaluate
            metrics = evaluator.evaluate(state)
            
            # Display summary
            print(f"\n✓ Research completed in {metrics['execution_metrics']['total_duration']:.2f}s")
            print(f"  - Tool calls: {metrics['tool_calls']}")
            print(f"  - Retries: {metrics['retry_count']}")
            
            if state.critic_feedback:
                print(f"  - Quality Status: {state.critic_feedback.status}")
                print(f"    • Completeness: {state.critic_feedback.completeness_score:.2f}")
                print(f"    • Consistency: {state.critic_feedback.factual_consistency_score:.2f}")
                print(f"    • Clarity: {state.critic_feedback.clarity_score:.2f}")
            
            # Show first 500 chars of answer
            if state.final_answer:
                preview = state.final_answer[:500]
                print(f"\nAnswer preview:\n{preview}...\n")
            
            results.append(metrics)
        
        except Exception as e:
            logger.error(f"Error on task {i}: {str(e)}")
            print(f"✗ Error: {str(e)}\n")
    
    # Show aggregated statistics
    print(f"\n{'='*80}")
    print("AGGREGATED STATISTICS")
    print(f"{'='*80}")
    
    stats = evaluator.get_statistics()
    
    if stats:
        print(f"Total executions: {stats['total_executions']}")
        print(f"Completed: {stats['completed']}")
        print(f"Success rate: {stats['success_rate']:.1%}")
        print(f"Average duration: {stats['average_duration']:.2f}s")
        print(f"Average tool calls: {stats['average_tool_calls']:.1f}")
        print(f"\nAverage quality:")
        print(f"  - Completeness: {stats['average_quality']['completeness']:.2f}")
        print(f"  - Consistency: {stats['average_quality']['factual_consistency']:.2f}")
        print(f"  - Clarity: {stats['average_quality']['clarity']:.2f}")
    
    logger.info("Demo completed")


if __name__ == "__main__":
    print("\n🤖 Enterprise Research Agent - Demo\n")
    asyncio.run(demo_research())
