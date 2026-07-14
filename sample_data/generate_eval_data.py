"""
Utility to generate sample evaluation data.
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
import random


def generate_sample_evaluations(count: int = 5) -> list:
    """
    Generate sample evaluation data.
    
    Args:
        count: Number of sample evaluations to generate
    
    Returns:
        List of evaluation dictionaries
    """
    evaluations = []
    base_time = datetime.utcnow()
    
    questions = [
        "What is artificial intelligence?",
        "Compare Python and Rust for systems programming",
        "Explain quantum computing basics",
        "What are microservices and their advantages?",
        "How does blockchain technology work?",
    ]
    
    for i in range(count):
        timestamp = base_time - timedelta(hours=i)
        question = questions[i % len(questions)]
        
        evaluation = {
            "state_id": f"state_{i:04d}",
            "question": question,
            "timestamp": timestamp.isoformat(),
            "completed": True,
            "execution_metrics": {
                "total_duration": random.uniform(30, 120),
                "tool_calls": random.randint(3, 10),
                "search_queries": random.randint(1, 5),
                "python_executions": random.randint(0, 3),
                "retry_count": random.randint(0, 2)
            },
            "plan_steps": random.randint(3, 8),
            "tool_calls": random.randint(3, 10),
            "retry_count": random.randint(0, 2),
            "critic_pass": random.random() > 0.2,  # 80% pass rate
            "final_answer_length": random.randint(1000, 5000),
            "quality_scores": {
                "completeness": round(random.uniform(0.7, 1.0), 2),
                "factual_consistency": round(random.uniform(0.75, 1.0), 2),
                "clarity": round(random.uniform(0.7, 0.95), 2)
            }
        }
        
        evaluations.append(evaluation)
    
    return evaluations


if __name__ == "__main__":
    # Generate sample data
    sample_data = generate_sample_evaluations(10)
    
    # Save to file
    output_path = Path("evaluation.json")
    with open(output_path, "w") as f:
        json.dump(sample_data, f, indent=2, default=str)
    
    print(f"Generated {len(sample_data)} sample evaluations")
    print(f"Saved to {output_path}")
