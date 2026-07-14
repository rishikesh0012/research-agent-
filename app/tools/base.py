"""
Tool implementations for the Enterprise Research Agent.
Includes search, Python execution, and analysis tools.
"""

import asyncio
import json
import time
from typing import Any, Dict, List, Optional
from datetime import datetime

from langchain_community.tools.tavily_search import TavilySearchResults
from app.models import ToolOutput, ToolType, SearchResult, SearchToolOutput, PythonToolOutput
from app.config import settings
from app.utils.logging import logger
from app.utils.validators import sanitize_query, validate_python_code


class SearchTool:
    """Tavily-based search tool for research queries."""
    
    def __init__(self):
        """Initialize search tool."""
        self.call_count = 0
        self.client = None

        if getattr(settings, "tavily_api_key", None):
            self.client = TavilySearchResults(
                api_key=settings.tavily_api_key,
                max_results=settings.tavily_max_results
            )
    
    async def search(self, query: str) -> ToolOutput:
        """
        Execute search query using Tavily API.
        
        Args:
            query: Search query string
        
        Returns:
            ToolOutput with structured search results
        """
        start_time = time.time()
        self.call_count += 1
        
        try:
            query = sanitize_query(query)

            if self.client is None:
                return ToolOutput(
                    tool_name="search",
                    tool_type=ToolType.SEARCH,
                    status="success",
                    result={
                        "query": query,
                        "results": [],
                        "message": "Tavily disabled. No search performed."
                    },
                    execution_time=0.0
                )
            logger.info(f"Executing search query: {query}")
            
            # Run search in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            raw_results = await loop.run_in_executor(
                None,
                lambda: self.client.invoke({"query": query})
            )
            
            # Parse results
            results = self._parse_results(raw_results)
            execution_time = time.time() - start_time
            
            output = SearchToolOutput(
                query=query,
                results=results,
                total_results=len(results),
                execution_time=execution_time
            )
            
            logger.info(f"Search completed: {len(results)} results in {execution_time:.2f}s")
            
            return ToolOutput(
                tool_name="search",
                tool_type=ToolType.SEARCH,
                status="success",
                result=output.dict(),
                execution_time=execution_time
            )
        
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Search tool error: {str(e)}")
            
            return ToolOutput(
                tool_name="search",
                tool_type=ToolType.SEARCH,
                status="error",
                result=None,
                error=str(e),
                execution_time=execution_time
            )
    
    @staticmethod
    def _parse_results(raw_results: List[Dict]) -> List[SearchResult]:
        """
        Parse raw Tavily results into structured SearchResult objects.
        
        Args:
            raw_results: Raw results from Tavily API
        
        Returns:
            List of structured SearchResult objects
        """
        parsed = []
        for result in raw_results:
            try:
                search_result = SearchResult(
                    title=result.get("title", "Unknown"),
                    url=result.get("url", ""),
                    content=result.get("content", "")[:1000],  # Limit content length
                    source=result.get("source", "Unknown"),
                    relevance_score=result.get("score", 0.0)
                )
                parsed.append(search_result)
            except Exception as e:
                logger.warning(f"Failed to parse search result: {e}")
                continue
        
        return parsed


class PythonTool:
    """Safe Python code execution tool for calculations and analysis."""
    
    ALLOWED_GLOBALS = {
        "__builtins__": {
            "len": len,
            "str": str,
            "int": int,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "sum": sum,
            "max": max,
            "min": min,
            "abs": abs,
            "round": round,
            "sorted": sorted,
            "enumerate": enumerate,
            "zip": zip,
            "range": range,
            "print": print,
        }
    }
    
    def __init__(self):
        """Initialize Python tool."""
        self.execution_count = 0
        self._setup_namespace()
    
    def _setup_namespace(self) -> None:
        """Setup safe namespace for code execution."""
        self.namespace = self.ALLOWED_GLOBALS.copy()
        
        # Add safe libraries
        try:
            import pandas as pd
            self.namespace["pd"] = pd
        except ImportError:
            logger.warning("pandas not available")
        
        try:
            import numpy as np
            self.namespace["np"] = np
        except ImportError:
            logger.warning("numpy not available")
        
        try:
            import json
            self.namespace["json"] = json
        except ImportError:
            pass
    
    async def execute(self, code: str) -> ToolOutput:
        """
        Execute Python code in restricted environment.
        
        Args:
            code: Python code to execute
        
        Returns:
            ToolOutput with execution result
        """
        start_time = time.time()
        self.execution_count += 1
        
        try:
            # Validate code
            validate_python_code(code)
            logger.info(f"Executing Python code (execution #{self.execution_count})")
            
            # Execute in thread pool
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self._safe_exec(code)
            )
            
            execution_time = time.time() - start_time
            
            output = PythonToolOutput(
                code=code,
                result=result,
                error=None,
                execution_time=execution_time
            )
            
            logger.info(f"Python execution completed in {execution_time:.2f}s")
            
            return ToolOutput(
                tool_name="python",
                tool_type=ToolType.PYTHON,
                status="success",
                result=output.dict(),
                execution_time=execution_time
            )
        
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Python tool error: {str(e)}")
            
            return ToolOutput(
                tool_name="python",
                tool_type=ToolType.PYTHON,
                status="error",
                result=None,
                error=str(e),
                execution_time=execution_time
            )
    
    def _safe_exec(self, code: str) -> Any:
        """
        Safely execute Python code with timeout.
        
        Args:
            code: Code to execute
        
        Returns:
            Execution result
        """
        local_namespace = {}
        exec(code, self.namespace, local_namespace)
        
        # Return last expression if it exists
        return local_namespace.get("result", None)


class AnalysisTool:
    """Tool for analyzing and processing collected data."""
    
    def __init__(self):
        """Initialize analysis tool."""
        self.analysis_count = 0
    
    async def analyze(self, data: Dict[str, Any], analysis_type: str) -> ToolOutput:
        """
        Perform analysis on collected data.
        
        Args:
            data: Data to analyze
            analysis_type: Type of analysis to perform
        
        Returns:
            ToolOutput with analysis results
        """
        start_time = time.time()
        self.analysis_count += 1
        
        try:
            logger.info(f"Performing {analysis_type} analysis")
            
            if analysis_type == "comparison":
                result = self._comparison_analysis(data)
            elif analysis_type == "summary":
                result = self._summary_analysis(data)
            else:
                raise ValueError(f"Unknown analysis type: {analysis_type}")
            
            execution_time = time.time() - start_time
            
            return ToolOutput(
                tool_name="analysis",
                tool_type=ToolType.ANALYSIS,
                status="success",
                result=result,
                execution_time=execution_time
            )
        
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Analysis tool error: {str(e)}")
            
            return ToolOutput(
                tool_name="analysis",
                tool_type=ToolType.ANALYSIS,
                status="error",
                result=None,
                error=str(e),
                execution_time=execution_time
            )
    
    @staticmethod
    def _comparison_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comparison analysis on data.
        
        Args:
            data: Data to compare
        
        Returns:
            Comparison analysis results
        """
        return {
            "type": "comparison",
            "items_compared": len(data),
            "data": data
        }
    
    @staticmethod
    def _summary_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform summary analysis on data.
        
        Args:
            data: Data to summarize
        
        Returns:
            Summary analysis results
        """
        return {
            "type": "summary",
            "items_summarized": len(data),
            "data": data
        }
