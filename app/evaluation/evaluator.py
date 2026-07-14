"""
Evaluation module for tracking and analyzing agent performance.
Collects metrics and stores execution history.
"""

import json
import time
from typing import Any, Dict, List, Optional
from datetime import datetime
from pathlib import Path

from app.models import AgentState, ExecutionMetrics
from app.utils.logging import logger


class ExecutionEvaluator:
    """Evaluates and tracks agent execution performance."""
    
    def __init__(self, eval_file: str = "evaluation.json"):
        """
        Initialize evaluator.
        
        Args:
            eval_file: Path to store evaluation results
        """
        self.eval_file = Path(eval_file)
        self.eval_file.parent.mkdir(parents=True, exist_ok=True)
        self.executions: List[Dict[str, Any]] = []
        self._load_evaluations()
    
    def _load_evaluations(self) -> None:
        """
        Load existing evaluations from file.
        """
        if self.eval_file.exists():
            try:
                with open(self.eval_file, "r") as f:
                    data = json.load(f)
                    self.executions = data if isinstance(data, list) else []
                    logger.info(f"Loaded {len(self.executions)} previous evaluations")
            except Exception as e:
                logger.warning(f"Failed to load evaluations: {e}")
                self.executions = []
    
    def evaluate(self, state: AgentState) -> Dict[str, Any]:
        """
        Evaluate a completed execution.
        
        Args:
            state: Final agent state
        
        Returns:
            Evaluation metrics dictionary
        """
        metrics = {
            "state_id": state.state_id,
            "question": state.question,
            "timestamp": datetime.utcnow().isoformat(),
            "completed": state.final_answer is not None,
            "execution_metrics": state.execution_metrics,
            "plan_steps": state.execution_plan.total_steps if state.execution_plan else 0,
            "tool_calls": len(state.tool_outputs),
            "retry_count": state.retry_count,
            "critic_pass": state.critic_feedback.status == "PASS" if state.critic_feedback else True,
            "final_answer_length": len(state.final_answer) if state.final_answer else 0,
            "quality_scores": {
                "completeness": state.critic_feedback.completeness_score if state.critic_feedback else 0.5,
                "factual_consistency": state.critic_feedback.factual_consistency_score if state.critic_feedback else 0.5,
                "clarity": state.critic_feedback.clarity_score if state.critic_feedback else 0.5
            }
        }
        
        # Store evaluation
        self.executions.append(metrics)
        self._save_evaluations()
        
        logger.info(f"Evaluation stored: {state.state_id}")
        return metrics
    
    def _save_evaluations(self) -> None:
        """
        Save evaluations to file.
        """
        try:
            with open(self.eval_file, "w") as f:
                json.dump(self.executions, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save evaluations: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get aggregated statistics from all executions.
        
        Returns:
            Statistics dictionary
        """
        if not self.executions:
            return {}
        
        completed = [e for e in self.executions if e["completed"]]
        failed = [e for e in self.executions if not e["completed"]]
        
        avg_duration = sum(e["execution_metrics"].get("total_duration", 0) for e in completed) / len(completed) if completed else 0
        avg_tool_calls = sum(e["tool_calls"] for e in completed) / len(completed) if completed else 0
        avg_steps = sum(e["plan_steps"] for e in completed) / len(completed) if completed else 0
        
        return {
            "total_executions": len(self.executions),
            "completed": len(completed),
            "failed": len(failed),
            "success_rate": len(completed) / len(self.executions) if self.executions else 0,
            "average_duration": avg_duration,
            "average_tool_calls": avg_tool_calls,
            "average_plan_steps": avg_steps,
            "total_retries": sum(e["retry_count"] for e in self.executions),
            "average_quality": {
                "completeness": sum(e["quality_scores"]["completeness"] for e in completed) / len(completed) if completed else 0,
                "factual_consistency": sum(e["quality_scores"]["factual_consistency"] for e in completed) / len(completed) if completed else 0,
                "clarity": sum(e["quality_scores"]["clarity"] for e in completed) / len(completed) if completed else 0
            }
        }
    
    def get_execution_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent execution history.
        
        Args:
            limit: Maximum number of executions to return
        
        Returns:
            List of recent executions
        """
        return self.executions[-limit:]
