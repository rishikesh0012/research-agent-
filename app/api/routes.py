"""
API endpoints for the Enterprise Research Agent.
Provides RESTful interface for research tasks.
"""

import uuid
from typing import Dict, Any, List
from datetime import datetime

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import ValidationError

from app.models import ResearchRequest, ResearchResponse, AgentState
from app.graph.workflow import ResearchAgentGraph
from app.evaluation.evaluator import ExecutionEvaluator
from app.tracing.tracer import ExecutionTracer
from app.utils.logging import logger
from app.utils.validators import validate_question


router = APIRouter(prefix="/api/v1", tags=["research"])

# Global instances
research_graph = ResearchAgentGraph()
evaluator = ExecutionEvaluator()
tracer = ExecutionTracer(enable_langsmith=True)

# Store for active research tasks
active_tasks: Dict[str, AgentState] = {}


@router.post("/research", response_model=ResearchResponse)
async def research(
    request: ResearchRequest,
    background_tasks: BackgroundTasks
) -> ResearchResponse:
    """
    Execute research task for given question.
    
    Args:
        request: ResearchRequest with question and parameters
        background_tasks: FastAPI background tasks
    
    Returns:
        ResearchResponse with results
    
    Raises:
        HTTPException: If validation or execution fails
    """
    try:
        # Validate question
        validate_question(request.question)
        logger.info(f"Research request: {request.question}")
        
        # Trace event
        tracer.trace_event(
            event_type="research_start",
            component="api",
            details={"question": request.question}
        )
        
        # Execute research workflow
        state = await research_graph.execute(request.question)
        
        # Store in active tasks
        active_tasks[state.state_id] = state
        
        # Evaluate execution
        metrics = evaluator.evaluate(state)
        
        # Trace completion
        tracer.trace_event(
            event_type="research_complete",
            component="api",
            details={"state_id": state.state_id}
        )
        
        # Build response
        response = ResearchResponse(
            state_id=state.state_id,
            question=state.question,
            final_answer=state.final_answer or "No answer generated",
            execution_plan=state.execution_plan,
            critic_feedback=state.critic_feedback,
            execution_metrics=state.execution_metrics
        )
        
        logger.info(f"Research completed: {state.state_id}")
        return response
    
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid request")
    except Exception as e:
        logger.error(f"Research error: {str(e)}")
        tracer.trace_error(
            event_type="research_error",
            component="api",
            error=str(e)
        )
        raise HTTPException(status_code=500, detail="Research failed")


@router.get("/research/{state_id}")
async def get_research_status(state_id: str) -> Dict[str, Any]:
    """
    Get status of active or completed research task.
    
    Args:
        state_id: ID of research task
    
    Returns:
        Status information
    
    Raises:
        HTTPException: If task not found
    """
    if state_id not in active_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    state = active_tasks[state_id]
    return {
        "state_id": state.state_id,
        "question": state.question,
        "status": "completed" if state.final_answer else "processing",
        "retry_count": state.retry_count,
        "execution_metrics": state.execution_metrics
    }


@router.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """
    Get aggregated metrics and statistics.
    
    Returns:
        Aggregated metrics
    """
    stats = evaluator.get_statistics()
    trace_summary = tracer.get_trace_summary()
    
    return {
        "evaluator_statistics": stats,
        "trace_summary": trace_summary,
        "active_tasks": len(active_tasks)
    }


@router.get("/history")
async def get_history(limit: int = 10) -> Dict[str, Any]:
    """
    Get execution history.
    
    Args:
        limit: Maximum number of executions to return
    
    Returns:
        Execution history
    """
    history = evaluator.get_execution_history(limit=limit)
    return {
        "total_stored": len(evaluator.executions),
        "history": history
    }


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    
    Returns:
        Health status
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


@router.get("/traces")
async def get_traces(format: str = "json") -> Dict[str, Any]:
    """
    Export execution traces.
    
    Args:
        format: Export format (json)
    
    Returns:
        Trace data
    """
    try:
        traces = tracer.export_traces(format=format)
        return {"format": format, "data": traces}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
