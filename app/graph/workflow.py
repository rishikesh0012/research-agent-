"""
LangGraph workflow orchestration for the Enterprise Research Agent.
Implements the complete research agent pipeline with state management and routing.
"""

import uuid
import time
from typing import Any, Dict, List

from langgraph.graph import StateGraph, END
from langchain_core.language_models import BaseLanguageModel

from app.models import AgentState, ToolType
from app.agents import PlannerAgent, WriterAgent, CriticAgent, RewriterAgent
from app.tools.base import SearchTool, PythonTool, AnalysisTool
from app.utils.logging import logger
from app.config import settings


class ResearchAgentGraph:
    """Main orchestrator for the research agent workflow using LangGraph."""
    
    def __init__(self):
        """Initialize graph with agents and tools."""
        self.planner = PlannerAgent()
        self.writer = WriterAgent()
        self.critic = CriticAgent()
        self.rewriter = RewriterAgent()
        
        self.search_tool = SearchTool()
        self.python_tool = PythonTool()
        self.analysis_tool = AnalysisTool()
        
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """
        Build LangGraph workflow graph.
        
        Returns:
            Compiled StateGraph
        """
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("planner", self._planner_node)
        workflow.add_node("executor", self._executor_node)
        workflow.add_node("writer", self._writer_node)
        workflow.add_node("critic", self._critic_node)
        workflow.add_node("rewriter", self._rewriter_node)
        
        # Set entry point
        workflow.set_entry_point("planner")
        
        # Add edges
        workflow.add_edge("planner", "executor")
        workflow.add_edge("executor", "writer")
        workflow.add_edge("writer", "critic")
        
        # Conditional routing from critic
        workflow.add_conditional_edges(
            "critic",
            self._critic_router,
            {
                "rewrite": "rewriter",
                "end": END
            }
        )
        
        # Rewriter goes to end
        workflow.add_edge("rewriter", END)
        
        return workflow.compile()
    
    async def _planner_node(self, state: AgentState) -> Dict[str, Any]:
        """
        Execute planner node.
        
        Args:
            state: Current agent state
        
        Returns:
            Updated state with execution plan
        """
        logger.info("Executing planner node")
        
        execution_plan = await self.planner.plan(state.question)
        state.execution_plan = execution_plan
        state.updated_at = __import__('datetime').datetime.utcnow()
        
        return {"execution_plan": execution_plan}
    
    async def _executor_node(self, state: AgentState) -> Dict[str, Any]:
        """
        Execute tool executor node.
        
        Args:
            state: Current agent state with execution plan
        
        Returns:
            Updated state with tool outputs
        """
        logger.info("Executing tool executor node")
        
        if not state.execution_plan:
            logger.error("No execution plan found")
            return {}
        
        tool_outputs = {}
        
        for step in state.execution_plan.steps:
            try:
                logger.info(f"Executing step {step.step_id}: {step.description}")
                
                if step.tool_required == ToolType.SEARCH:
                    output = await self.search_tool.search(
                        step.parameters.get("query", state.question)
                    )
                elif step.tool_required == ToolType.PYTHON:
                    output = await self.python_tool.execute(
                        step.parameters.get("code", "result = {}")
                    )
                elif step.tool_required == ToolType.ANALYSIS:
                    output = await self.analysis_tool.analyze(
                        step.parameters.get("data", {}),
                        step.parameters.get("type", "summary")
                    )
                else:
                    logger.warning(f"Unknown tool type: {step.tool_required}")
                    continue
                
                tool_outputs[f"step_{step.step_id}"] = output
                state.tool_outputs[f"step_{step.step_id}"] = output
                
            except Exception as e:
                logger.error(f"Error executing step {step.step_id}: {str(e)}")
                continue
        
        state.updated_at = __import__('datetime').datetime.utcnow()
        return {"tool_outputs": state.tool_outputs}
    
    async def _writer_node(self, state: AgentState) -> Dict[str, Any]:
        """
        Execute writer node to generate report.
        
        Args:
            state: Current agent state with tool outputs
        
        Returns:
            Updated state with draft answer
        """
        logger.info("Executing writer node")
        
        # Prepare research data from tool outputs
        research_data = {}
        for key, output in state.tool_outputs.items():
            if output.status == "success":
                research_data[key] = output.result
        
        # Generate report
        draft_answer = await self.writer.write_report(state.question, research_data)
        state.draft_answer = draft_answer
        state.updated_at = __import__('datetime').datetime.utcnow()
        
        return {"draft_answer": draft_answer}
    
    async def _critic_node(self, state: AgentState) -> Dict[str, Any]:
        """
        Execute critic node to evaluate report.
        
        Args:
            state: Current agent state with draft answer
        
        Returns:
            Updated state with critic feedback
        """
        logger.info("Executing critic node")
        
        if not state.draft_answer:
            logger.error("No draft answer to critique")
            state.critic_feedback = None
            return {}
        
        feedback = await self.critic.critique(state.question, state.draft_answer)
        state.critic_feedback = feedback
        state.updated_at = __import__('datetime').datetime.utcnow()
        
        return {"critic_feedback": feedback}
    
    async def _rewriter_node(self, state: AgentState) -> Dict[str, Any]:
        """
        Execute rewriter node to improve report.
        
        Args:
            state: Current agent state with critic feedback
        
        Returns:
            Updated state with final answer
        """
        logger.info("Executing rewriter node")
        
        if not state.draft_answer or not state.critic_feedback:
            logger.error("Missing draft answer or critic feedback")
            state.final_answer = state.draft_answer
            return {}
        
        # Format feedback for rewriter
        feedback_str = f"""
        Issues: {', '.join(state.critic_feedback.issues)}
        Suggestions: {', '.join(state.critic_feedback.suggestions)}
        Scores:
        - Completeness: {state.critic_feedback.completeness_score}
        - Factual Consistency: {state.critic_feedback.factual_consistency_score}
        - Clarity: {state.critic_feedback.clarity_score}
        """
        
        final_answer = await self.rewriter.rewrite(
            state.question,
            state.draft_answer,
            feedback_str
        )
        state.final_answer = final_answer
        state.retry_count += 1
        state.updated_at = __import__('datetime').datetime.utcnow()
        
        return {"final_answer": final_answer}
    
    def _critic_router(self, state: AgentState) -> str:
        """
        Route based on critic feedback.
        
        Args:
            state: Current agent state
        
        Returns:
            Next node name ("rewrite" or "end")
        """
        if not state.critic_feedback:
            return "end"
        
        # Pass if status is PASS or retry limit reached
        if state.critic_feedback.status == "PASS":
            logger.info("Critic PASSED - moving to end")
            state.final_answer = state.draft_answer
            return "end"
        
        # Fail if retry limit reached
        if state.retry_count >= settings.max_retries:
            logger.info("Retry limit reached - moving to end")
            state.final_answer = state.draft_answer
            return "end"
        
        logger.info("Critic FAILED - rewriting")
        return "rewrite"
    
    async def execute(self, question: str) -> AgentState:
        """
        Execute the complete research workflow.
        
        Args:
            question: Research question
        
        Returns:
            Final agent state with complete results
        """
        logger.info(f"Starting research workflow for: {question}")
        start_time = time.time()
        
        # Initialize state
        state = AgentState(
            state_id=str(uuid.uuid4()),
            question=question,
            execution_plan=None,
            tool_outputs={},
            intermediate_results={},
            draft_answer=None,
            critic_feedback=None,
            final_answer=None,
            retry_count=0,
            execution_metrics={}
        )
        
        try:
            # Execute graph
            # Note: This is a simplified execution. Full implementation would use graph.invoke()
            await self._planner_node(state)
            await self._executor_node(state)
            await self._writer_node(state)
            await self._critic_node(state)
            
            # Route based on critic
            route = self._critic_router(state)
            if route == "rewrite" and state.retry_count < settings.max_retries:
                await self._rewriter_node(state)
            else:
                if not state.final_answer:
                    state.final_answer = state.draft_answer
            
            # Calculate metrics
            duration = time.time() - start_time
            state.execution_metrics = {
                "total_duration": duration,
                "tool_calls": len(state.tool_outputs),
                "retry_count": state.retry_count,
                "critic_pass": state.critic_feedback.status == "PASS" if state.critic_feedback else True,
                "final_answer_length": len(state.final_answer) if state.final_answer else 0
            }
            
            logger.info(f"Workflow completed in {duration:.2f}s")
            return state
        
        except Exception as e:
            logger.error(f"Workflow error: {str(e)}")
            state.final_answer = f"Error during research: {str(e)}"
            state.execution_metrics = {
                "error": str(e),
                "total_duration": time.time() - start_time
            }
            return state
