"""
CLI utility for running research tasks from command line.
"""

import asyncio
import json
from typing import Optional

from app.graph.workflow import ResearchAgentGraph
from app.evaluation.evaluator import ExecutionEvaluator
from app.utils.logging import logger
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table


class ResearchCLI:
    """Command-line interface for research agent."""
    
    def __init__(self):
        """Initialize CLI."""
        self.console = Console()
        self.graph = ResearchAgentGraph()
        self.evaluator = ExecutionEvaluator()
    
    async def research(self, question: str, max_retries: int = 1, verbose: bool = False) -> None:
        """
        Execute research task from CLI.
        
        Args:
            question: Research question
            max_retries: Maximum retries if critique fails
            verbose: Enable verbose output
        """
        self.console.print(
            Panel(
                f"[bold cyan]Enterprise Research Agent[/bold cyan]\n{question}",
                title="Research Task",
                expand=False
            )
        )
        
        try:
            # Execute research
            state = await self.graph.execute(question)
            
            # Display results
            self._display_results(state, verbose)
            
            # Evaluate
            metrics = self.evaluator.evaluate(state)
            self._display_metrics(metrics)
        
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")
    
    def _display_results(self, state, verbose: bool) -> None:
        """
        Display research results.
        
        Args:
            state: Final agent state
            verbose: Enable verbose output
        """
        # Display execution plan
        if state.execution_plan and verbose:
            self.console.print("\n[bold]Execution Plan[/bold]")
            plan_table = Table(title="Steps")
            plan_table.add_column("Step", style="cyan")
            plan_table.add_column("Description", style="magenta")
            plan_table.add_column("Tool", style="green")
            
            for step in state.execution_plan.steps:
                plan_table.add_row(
                    str(step.step_id),
                    step.description,
                    step.tool_required.value
                )
            
            self.console.print(plan_table)
        
        # Display final report
        self.console.print("\n[bold]Final Report[/bold]")
        if state.final_answer:
            self.console.print(Markdown(state.final_answer))
        else:
            self.console.print("[yellow]No report generated[/yellow]")
        
        # Display critic feedback
        if state.critic_feedback:
            self.console.print("\n[bold]Quality Assessment[/bold]")
            feedback_table = Table(title="Scores")
            feedback_table.add_column("Metric", style="cyan")
            feedback_table.add_column("Score", style="green")
            
            feedback_table.add_row(
                "Status",
                f"[{'green' if state.critic_feedback.status == 'PASS' else 'red'}]{state.critic_feedback.status}[/]"
            )
            feedback_table.add_row(
                "Completeness",
                f"{state.critic_feedback.completeness_score:.2f}"
            )
            feedback_table.add_row(
                "Factual Consistency",
                f"{state.critic_feedback.factual_consistency_score:.2f}"
            )
            feedback_table.add_row(
                "Clarity",
                f"{state.critic_feedback.clarity_score:.2f}"
            )
            
            self.console.print(feedback_table)
    
    def _display_metrics(self, metrics: dict) -> None:
        """
        Display execution metrics.
        
        Args:
            metrics: Execution metrics dictionary
        """
        self.console.print("\n[bold]Execution Metrics[/bold]")
        
        metrics_table = Table(title="Performance")
        metrics_table.add_column("Metric", style="cyan")
        metrics_table.add_column("Value", style="green")
        
        if "execution_metrics" in metrics:
            exec_metrics = metrics["execution_metrics"]
            metrics_table.add_row(
                "Total Duration",
                f"{exec_metrics.get('total_duration', 0):.2f}s"
            )
            metrics_table.add_row(
                "Tool Calls",
                str(metrics.get("tool_calls", 0))
            )
            metrics_table.add_row(
                "Retries",
                str(metrics.get("retry_count", 0))
            )
        
        self.console.print(metrics_table)
    
    def show_statistics(self) -> None:
        """
        Display aggregated statistics.
        """
        stats = self.evaluator.get_statistics()
        
        if not stats:
            self.console.print("[yellow]No statistics available[/yellow]")
            return
        
        self.console.print(
            Panel(
                "[bold cyan]Execution Statistics[/bold cyan]",
                title="Statistics",
                expand=False
            )
        )
        
        stats_table = Table()
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="green")
        
        stats_table.add_row("Total Executions", str(stats.get("total_executions", 0)))
        stats_table.add_row("Completed", str(stats.get("completed", 0)))
        stats_table.add_row("Success Rate", f"{stats.get('success_rate', 0):.1%}")
        stats_table.add_row(
            "Average Duration",
            f"{stats.get('average_duration', 0):.2f}s"
        )
        
        quality = stats.get("average_quality", {})
        stats_table.add_row(
            "Avg Completeness",
            f"{quality.get('completeness', 0):.2f}"
        )
        stats_table.add_row(
            "Avg Consistency",
            f"{quality.get('factual_consistency', 0):.2f}"
        )
        stats_table.add_row(
            "Avg Clarity",
            f"{quality.get('clarity', 0):.2f}"
        )
        
        self.console.print(stats_table)


async def main():
    """Main CLI entry point."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python -m app.cli <question> [--verbose] [--stats]")
        print("\nExample:")
        print("  python -m app.cli 'What is AI?' --verbose")
        sys.exit(1)
    
    cli = ResearchCLI()
    
    # Parse arguments
    question = sys.argv[1]
    verbose = "--verbose" in sys.argv
    show_stats = "--stats" in sys.argv
    
    if show_stats:
        cli.show_statistics()
    else:
        await cli.research(question, verbose=verbose)


if __name__ == "__main__":
    asyncio.run(main())
