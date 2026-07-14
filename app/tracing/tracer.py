"""
Tracing module for observability and debugging.
Implements execution tracing with optional LangSmith integration.
"""

import time
import json
from typing import Any, Dict, Optional
from datetime import datetime
from dataclasses import dataclass, field, asdict

from app.config import settings
from app.utils.logging import logger


@dataclass
class ExecutionTrace:
    """Represents a single execution trace event."""
    event_type: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    duration: float = 0.0
    component: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    status: str = "pending"  # pending, running, completed, failed


class ExecutionTracer:
    """Traces execution events for observability."""
    
    def __init__(self, enable_langsmith: bool = False):
        """
        Initialize tracer.
        
        Args:
            enable_langsmith: Enable LangSmith integration
        """
        self.traces: list[ExecutionTrace] = []
        self.enable_langsmith = enable_langsmith and settings.langsmith_enabled
        
        if self.enable_langsmith:
            self._setup_langsmith()
    
    def _setup_langsmith(self) -> None:
        """
        Setup LangSmith integration if enabled.
        """
        try:
            import os
            if settings.langsmith_api_key:
                os.environ["LANGSMITH_API_KEY"] = settings.langsmith_api_key
            if settings.langsmith_project:
                os.environ["LANGSMITH_PROJECT"] = settings.langsmith_project
            
            logger.info("LangSmith tracing enabled")
        except Exception as e:
            logger.warning(f"Failed to setup LangSmith: {e}")
    
    def trace_event(
        self,
        event_type: str,
        component: str,
        details: Dict[str, Any] = None,
        status: str = "completed"
    ) -> ExecutionTrace:
        """
        Record a traced event.
        
        Args:
            event_type: Type of event (planner_start, tool_execute, etc.)
            component: Component that generated event
            details: Event details
            status: Event status
        
        Returns:
            ExecutionTrace object
        """
        trace = ExecutionTrace(
            event_type=event_type,
            component=component,
            details=details or {},
            status=status
        )
        
        self.traces.append(trace)
        logger.debug(f"Trace: {event_type} from {component}")
        
        return trace
    
    def trace_duration(
        self,
        event_type: str,
        component: str,
        duration: float,
        details: Dict[str, Any] = None
    ) -> ExecutionTrace:
        """
        Record a traced event with duration.
        
        Args:
            event_type: Type of event
            component: Component name
            duration: Duration in seconds
            details: Event details
        
        Returns:
            ExecutionTrace object
        """
        trace = ExecutionTrace(
            event_type=event_type,
            component=component,
            duration=duration,
            details=details or {},
            status="completed"
        )
        
        self.traces.append(trace)
        logger.debug(f"Trace: {event_type} from {component} ({duration:.2f}s)")
        
        return trace
    
    def trace_error(
        self,
        event_type: str,
        component: str,
        error: str,
        details: Dict[str, Any] = None
    ) -> ExecutionTrace:
        """
        Record a traced error event.
        
        Args:
            event_type: Type of event
            component: Component name
            error: Error message
            details: Event details
        
        Returns:
            ExecutionTrace object
        """
        trace = ExecutionTrace(
            event_type=event_type,
            component=component,
            error=error,
            details=details or {},
            status="failed"
        )
        
        self.traces.append(trace)
        logger.error(f"Trace Error: {event_type} from {component} - {error}")
        
        return trace
    
    def get_trace_summary(self) -> Dict[str, Any]:
        """
        Get summary of all traces.
        
        Returns:
            Trace summary dictionary
        """
        total_duration = sum(t.duration for t in self.traces)
        event_counts = {}
        
        for trace in self.traces:
            event_counts[trace.event_type] = event_counts.get(trace.event_type, 0) + 1
        
        return {
            "total_events": len(self.traces),
            "total_duration": total_duration,
            "event_counts": event_counts,
            "errors": [t.error for t in self.traces if t.error],
            "traces": [asdict(t) for t in self.traces]
        }
    
    def export_traces(self, format: str = "json") -> str:
        """
        Export traces in specified format.
        
        Args:
            format: Export format (json)
        
        Returns:
            Exported traces
        """
        if format == "json":
            return json.dumps(
                [asdict(t) for t in self.traces],
                indent=2,
                default=str
            )
        
        raise ValueError(f"Unsupported export format: {format}")
