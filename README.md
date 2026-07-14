# Enterprise Research Agent - NVIDIA Edition

**Production-quality AI Research Agent** with LangGraph orchestration, tool-based research execution, and self-critique for portfolio-grade quality. **Now powered by NVIDIA AI Foundation Models API.**

## Overview

The Enterprise Research Agent is a sophisticated agentic AI system that answers complex research questions through:

1. **Planning** - Breaking down research questions into logical steps
2. **Tool Execution** - Gathering data via search and analysis tools
3. **Report Writing** - Synthesizing findings into comprehensive reports
4. **Self-Critique** - Evaluating report quality and completeness
5. **Rewriting** - Improving reports based on feedback

This is **not** a chatbot—it's a production-ready research orchestration system demonstrating enterprise AI engineering practices.

---

## What's New: NVIDIA Migration ✨

### Powered by NVIDIA AI Foundation Models
- **LLM Provider**: NVIDIA AI Foundation Models (via OpenAI-compatible API)
- **Default Model**: Meta Llama 2 70B Chat
- **API Endpoint**: https://integrate.api.nvidia.com/v1
- **Zero Breaking Changes**: Existing architecture, workflows, and tests remain unchanged

### Migration Highlights
- ✅ Complete NVIDIA API integration
- ✅ OpenAI-compatible endpoint (drop-in replacement)
- ✅ All agents (Planner, Writer, Critic, Rewriter) updated
- ✅ Configuration moved to NVIDIA environment variables
- ✅ No changes to LangGraph workflow or business logic
- ✅ Full backward compatibility with existing test suite

---

## Architecture

```
User Question
    ↓
Planner Agent (Plan Research) [NVIDIA LLM]
    ↓
Tool Executor (Search, Python, Analysis)
    ↓
Writer Agent (Synthesize Report) [NVIDIA LLM]
    ↓
Critic Agent (Evaluate Quality) [NVIDIA LLM]
    ↓
    ├→ PASS → Final Report
    └→ FAIL → Rewriter Agent [NVIDIA LLM] → Final Report
```

### Core Components

- **Planner Agent**: Breaks questions into executable tasks using NVIDIA LLM
- **Search Tool**: Tavily-based web search for research data
- **Python Tool**: Safe code execution for calculations and analysis
- **Analysis Tool**: Data aggregation and comparison
- **Writer Agent**: Report generation with NVIDIA LLM
- **Critic Agent**: Quality evaluation using NVIDIA LLM
- **Rewriter Agent**: Improvement based on feedback via NVIDIA LLM
- **LangGraph Orchestrator**: Workflow coordination and state management

---

## Installation

### Prerequisites
- Python 3.11+
- NVIDIA API key (from https://build.nvidia.com)
- Tavily Search API key

### Setup

1. **Clone repository**
```bash
git clone https://github.com/rishikesh0012/research-agent-.git
cd research-agent-
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API keys
export NVIDIA_API_KEY="nvapi-your-key"
export NVIDIA_MODEL="meta/llama-2-70b-chat"
export NVIDIA_BASE_URL="https://integrate.api.nvidia.com/v1"
export TAVILY_API_KEY="tvly-your-key"
```

---

## Configuration

### Environment Variables

```bash
# NVIDIA API Configuration
NVIDIA_API_KEY=nvapi-your-api-key-here
NVIDIA_MODEL=meta/llama-2-70b-chat
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1

# Tavily Search
TAVILY_API_KEY=tvly-...

# Application
DEBUG=false
LOG_LEVEL=INFO

# LangSmith (Optional)
LANGSMITH_ENABLED=false
LANGSMITH_API_KEY=...
LANGSMITH_PROJECT=...

# Server
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
FASTAPI_RELOAD=true
```

### Available NVIDIA Models

You can use any model available in the NVIDIA catalog:
- `meta/llama-2-70b-chat` (default)
- `mistralai/mistral-large`
- `mistralai/mistral-medium`
- `mistralai/mixtral-8x7b-instruct-v0.1`
- And more from https://build.nvidia.com/explore/discover

---

## Running Locally

### Start the server

```bash
uvicorn app.main:app --reload
```

Server runs at `http://localhost:8000`

### Interactive API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## API Examples

### 1. Execute Research Task

```bash
curl -X POST "http://localhost:8000/api/v1/research" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Compare LangGraph and CrewAI for production AI agents",
    "max_retries": 1,
    "timeout_seconds": 300
  }'
```

### 2. Get Research Status

```bash
curl "http://localhost:8000/api/v1/research/{state_id}"
```

### 3. Get Metrics

```bash
curl "http://localhost:8000/api/v1/metrics"
```

### 4. Health Check

```bash
curl "http://localhost:8000/api/v1/health"
```

---

## Testing

### Run all tests
```bash
pytest -v
```

### Run with coverage
```bash
pytest --cov=app --cov-report=html
```

---

## Code Quality

- ✅ **Type Hints**: Full type annotations throughout
- ✅ **Pydantic Models**: Strongly-typed data structures
- ✅ **Error Handling**: Comprehensive exception handling
- ✅ **Logging**: Rich-formatted structured logging
- ✅ **SOLID Principles**: Modular, reusable components
- ✅ **NVIDIA Integration**: Seamless API integration

---

## NVIDIA Migration Summary

### Files Modified

| File | Changes |
|------|----------|
| `app/config.py` | Replaced OpenAI settings with NVIDIA API configuration |
| `app/agents/__init__.py` | Updated all agents to use NVIDIA LLM via OpenAI-compatible API |
| `.env.example` | Replaced OpenAI env vars with NVIDIA equivalents |
| `app/production.py` | Added NVIDIA model logging |
| `README.md` | Updated documentation for NVIDIA |

### No Breaking Changes

- ✅ LangGraph workflow unchanged
- ✅ FastAPI endpoints unchanged
- ✅ Prompt templates unchanged
- ✅ Tool implementations unchanged
- ✅ Evaluation system unchanged
- ✅ All tests pass

---

## License

MIT License - see LICENSE file for details

---

## Author

**Rishikesh KG** - AI Engineer & Senior Software Architect

---

## Resources

- [NVIDIA AI Foundation Models](https://build.nvidia.com)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Tavily Search API](https://tavily.com/)

---

**Built with production-quality AI engineering practices** ✨
**Now powered by NVIDIA AI Foundation Models** 🚀
