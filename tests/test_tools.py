"""
Tests for tools.
"""

import pytest
from app.tools.base import SearchTool, PythonTool, AnalysisTool
from app.models import ToolOutput, ToolType


@pytest.mark.asyncio
async def test_search_tool():
    """Test search tool execution."""
    search = SearchTool()
    query = "Python programming"
    
    output = await search.search(query)
    
    assert isinstance(output, ToolOutput)
    assert output.tool_name == "search"
    assert output.tool_type == ToolType.SEARCH
    assert output.status in ["success", "error"]
    assert output.execution_time >= 0


@pytest.mark.asyncio
async def test_python_tool():
    """Test Python tool execution."""
    python_tool = PythonTool()
    code = "result = 2 + 2"
    
    output = await python_tool.execute(code)
    
    assert isinstance(output, ToolOutput)
    assert output.tool_name == "python"
    assert output.tool_type == ToolType.PYTHON
    assert output.status in ["success", "error"]


@pytest.mark.asyncio
async def test_python_tool_rejects_unsafe_code():
    """Test Python tool rejects unsafe code."""
    python_tool = PythonTool()
    code = "import os; os.system('rm -rf /')"
    
    output = await python_tool.execute(code)
    
    assert output.status == "error"
    assert "not allowed" in output.error.lower() or "dangerous" in output.error.lower()


@pytest.mark.asyncio
async def test_analysis_tool():
    """Test analysis tool execution."""
    analysis = AnalysisTool()
    data = {"item1": "value1", "item2": "value2"}
    
    output = await analysis.analyze(data, "summary")
    
    assert isinstance(output, ToolOutput)
    assert output.tool_name == "analysis"
    assert output.tool_type == ToolType.ANALYSIS
    assert output.status == "success"
