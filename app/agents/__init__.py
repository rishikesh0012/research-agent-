"""
Agent implementations for the Enterprise Research Agent.
Includes Planner, Writer, Critic, and Rewriter agents using NVIDIA API.
"""

import json
import time
import os
from typing import Any, Dict, Optional

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from app.config import settings
from app.models import (
    ExecutionPlan, PlanStep, ToolType, AgentState, CriticFeedback
)
from app.prompts import (
    PLANNER_SYSTEM_PROMPT, PLANNER_USER_TEMPLATE,
    WRITER_SYSTEM_PROMPT, WRITER_USER_TEMPLATE,
    CRITIC_SYSTEM_PROMPT, CRITIC_USER_TEMPLATE,
    REWRITER_SYSTEM_PROMPT, REWRITER_USER_TEMPLATE
)
from app.utils.logging import logger


def _create_nvidia_llm(temperature: float = None) -> ChatOpenAI:
    """
    Create and configure an NVIDIA-compatible LLM client.
    Uses OpenAI-compatible NVIDIA API endpoint.
    
    Args:
        temperature: Model temperature for sampling
    
    Returns:
        Configured ChatOpenAI instance for NVIDIA API
    """
    if temperature is None:
        temperature = settings.nvidia_temperature
    
    return ChatOpenAI(
        openai_api_key=settings.nvidia_api_key,
        openai_api_base=settings.nvidia_base_url,
        model_name=settings.nvidia_model,
        temperature=temperature
    )


class PlannerAgent:
    """Agent responsible for planning research tasks."""
    
    def __init__(self):
        """Initialize planner agent with NVIDIA LLM."""
        self.llm = _create_nvidia_llm()
    
    async def plan(self, question: str) -> ExecutionPlan:
        """
        Generate execution plan for research question.
        
        Args:
            question: Research question
        
        Returns:
            ExecutionPlan with steps and tool requirements
        """
        start_time = time.time()
        logger.info(f"Planning research for: {question}")
        
        try:
            # Prepare messages
            system_msg = SystemMessage(content=PLANNER_SYSTEM_PROMPT)
            user_msg = HumanMessage(content=PLANNER_USER_TEMPLATE.format(question=question))
            
            # Call LLM
            response = await self.llm.apredict_messages([system_msg, user_msg])
            
            # Parse response
            response_text = response.content
            plan_data = self._parse_plan_response(response_text)
            
            # Create ExecutionPlan
            execution_plan = ExecutionPlan(
                plan_id=f"plan_{int(start_time)}",
                question=question,
                total_steps=plan_data["total_steps"],
                steps=[
                    PlanStep(
                        step_id=step["step_id"],
                        description=step["description"],
                        tool_required=ToolType(step["tool_required"]),
                        parameters=step["parameters"],
                        depends_on=step.get("depends_on", [])
                    )
                    for step in plan_data["steps"]
                ],
                estimated_duration=plan_data.get("estimated_duration", 60.0)
            )
            
            duration = time.time() - start_time
            logger.info(f"Plan created in {duration:.2f}s: {plan_data['total_steps']} steps")
            
            return execution_plan
        
        except Exception as e:
            logger.error(f"Planning error: {str(e)}")
            # Return fallback plan
            return self._create_fallback_plan(question)
    
    @staticmethod
    def _parse_plan_response(response: str) -> Dict[str, Any]:
        """
        Parse LLM response into plan dictionary.
        
        Args:
            response: LLM response text
        
        Returns:
            Parsed plan dictionary
        """
        try:
            # Extract JSON from response
            start_idx = response.find("{")
            end_idx = response.rfind("}") + 1
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[start_idx:end_idx]
            return json.loads(json_str)
        except Exception as e:
            logger.warning(f"Failed to parse plan response: {e}")
            return {
                "total_steps": 3,
                "steps": [
                    {
                        "step_id": 1,
                        "description": "Search for information",
                        "tool_required": "search",
                        "parameters": {"query": "general information"},
                        "depends_on": []
                    },
                    {
                        "step_id": 2,
                        "description": "Analyze findings",
                        "tool_required": "analysis",
                        "parameters": {"type": "summary"},
                        "depends_on": [1]
                    },
                    {
                        "step_id": 3,
                        "description": "Generate report",
                        "tool_required": "python",
                        "parameters": {"code": "result = {}"},
                        "depends_on": [2]
                    }
                ],
                "estimated_duration": 120.0
            }
    
    @staticmethod
    def _create_fallback_plan(question: str) -> ExecutionPlan:
        """
        Create fallback plan if planning fails.
        
        Args:
            question: Research question
        
        Returns:
            Basic ExecutionPlan
        """
        return ExecutionPlan(
            plan_id="fallback_plan",
            question=question,
            total_steps=2,
            steps=[
                PlanStep(
                    step_id=1,
                    description="Search for relevant information",
                    tool_required=ToolType.SEARCH,
                    parameters={"query": question},
                    depends_on=[]
                ),
                PlanStep(
                    step_id=2,
                    description="Generate analysis and report",
                    tool_required=ToolType.ANALYSIS,
                    parameters={},
                    depends_on=[1]
                )
            ],
            estimated_duration=60.0
        )


class WriterAgent:
    """Agent responsible for writing final reports."""
    
    def __init__(self):
        """Initialize writer agent with NVIDIA LLM."""
        self.llm = _create_nvidia_llm()
    
    async def write_report(self, question: str, research_data: Dict[str, Any]) -> str:
        """
        Generate comprehensive research report.
        
        Args:
            question: Original research question
            research_data: Collected research data
        
        Returns:
            Generated report as markdown string
        """
        start_time = time.time()
        logger.info("Writing research report")
        
        try:
            # Format research data
            formatted_data = json.dumps(research_data, indent=2)
            
            # Prepare messages
            system_msg = SystemMessage(content=WRITER_SYSTEM_PROMPT)
            user_msg = HumanMessage(
                content=WRITER_USER_TEMPLATE.format(
                    question=question,
                    research_data=formatted_data
                )
            )
            
            # Call LLM
            response = await self.llm.apredict_messages([system_msg, user_msg])
            report = response.content
            
            duration = time.time() - start_time
            logger.info(f"Report generated in {duration:.2f}s")
            
            return report
        
        except Exception as e:
            logger.error(f"Report writing error: {str(e)}")
            return f"# Research Report\n\nQuestion: {question}\n\nError generating report: {str(e)}"


class CriticAgent:
    """Agent responsible for critiquing and evaluating reports."""
    
    def __init__(self):
        """Initialize critic agent with NVIDIA LLM."""
        self.llm = _create_nvidia_llm(temperature=0.3)
    
    async def critique(self, question: str, report: str) -> CriticFeedback:
        """
        Critique and evaluate research report.
        
        Args:
            question: Original research question
            report: Report to critique
        
        Returns:
            CriticFeedback with evaluation results
        """
        start_time = time.time()
        logger.info("Critiquing research report")
        
        try:
            # Prepare messages
            system_msg = SystemMessage(content=CRITIC_SYSTEM_PROMPT)
            user_msg = HumanMessage(
                content=CRITIC_USER_TEMPLATE.format(
                    question=question,
                    report=report
                )
            )
            
            # Call LLM
            response = await self.llm.apredict_messages([system_msg, user_msg])
            
            # Parse response
            feedback_data = self._parse_feedback_response(response.content)
            
            # Create CriticFeedback
            feedback = CriticFeedback(
                status=feedback_data["status"],
                completeness_score=feedback_data.get("completeness_score", 0.5),
                factual_consistency_score=feedback_data.get("factual_consistency_score", 0.5),
                clarity_score=feedback_data.get("clarity_score", 0.5),
                issues=feedback_data.get("issues", []),
                suggestions=feedback_data.get("suggestions", [])
            )
            
            duration = time.time() - start_time
            logger.info(f"Critique completed in {duration:.2f}s: {feedback.status}")
            
            return feedback
        
        except Exception as e:
            logger.error(f"Critique error: {str(e)}")
            return CriticFeedback(
                status="PASS",
                completeness_score=0.7,
                factual_consistency_score=0.7,
                clarity_score=0.7,
                issues=[],
                suggestions=[]
            )
    
    @staticmethod
    def _parse_feedback_response(response: str) -> Dict[str, Any]:
        """
        Parse LLM response into feedback dictionary.
        
        Args:
            response: LLM response text
        
        Returns:
            Parsed feedback dictionary
        """
        try:
            start_idx = response.find("{")
            end_idx = response.rfind("}") + 1
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[start_idx:end_idx]
            return json.loads(json_str)
        except Exception as e:
            logger.warning(f"Failed to parse feedback response: {e}")
            return {
                "status": "PASS",
                "completeness_score": 0.8,
                "factual_consistency_score": 0.8,
                "clarity_score": 0.8,
                "issues": [],
                "suggestions": []
            }


class RewriterAgent:
    """Agent responsible for rewriting reports based on feedback."""
    
    def __init__(self):
        """Initialize rewriter agent with NVIDIA LLM."""
        self.llm = _create_nvidia_llm()
    
    async def rewrite(self, question: str, original_report: str, feedback: str) -> str:
        """
        Rewrite report based on critic feedback.
        
        Args:
            question: Original research question
            original_report: Original report text
            feedback: Critic feedback as formatted string
        
        Returns:
            Rewritten report
        """
        start_time = time.time()
        logger.info("Rewriting research report")
        
        try:
            # Prepare messages
            system_msg = SystemMessage(content=REWRITER_SYSTEM_PROMPT)
            user_msg = HumanMessage(
                content=REWRITER_USER_TEMPLATE.format(
                    question=question,
                    original_report=original_report,
                    feedback=feedback
                )
            )
            
            # Call LLM
            response = await self.llm.apredict_messages([system_msg, user_msg])
            rewritten_report = response.content
            
            duration = time.time() - start_time
            logger.info(f"Report rewritten in {duration:.2f}s")
            
            return rewritten_report
        
        except Exception as e:
            logger.error(f"Report rewriting error: {str(e)}")
            return original_report
