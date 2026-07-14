# 🤖 Research Agent

> A full-stack Multi-Agent AI Research Assistant built using **LangGraph, FastAPI, React, and NVIDIA Foundation Models**.

The application accepts a research question, plans the research workflow, executes tools, generates a structured research report, critiques its own output, and presents the final result through a modern React interface.

---

## 🚀 Features

- Multi-Agent AI workflow using LangGraph
- Planner, Writer, Critic, and Rewriter agents
- FastAPI backend
- React + Vite frontend
- Research report generation
- Markdown report rendering
- REST API
- Swagger API documentation
- Modular architecture
- Execution metrics dashboard

---

# 🏗 Architecture

```
                User
                  │
                  ▼
         React Frontend (Vite)
                  │
                  ▼
          FastAPI REST API
                  │
                  ▼
          LangGraph Workflow
                  │
     ┌────────────┴────────────┐
     ▼                         ▼
 Planner Agent          Tool Executor
                              │
             ┌────────────────┼───────────────┐
             ▼                ▼               ▼
        Search Tool      Python Tool   Analysis Tool
                              │
                              ▼
                       Writer Agent
                              │
                              ▼
                       Critic Agent
                              │
                  PASS ───────┴────── FAIL
                     │                │
                     ▼                ▼
               Final Report     Rewriter Agent
                                      │
                                      ▼
                                Final Report
```

---

# ⚙️ Tech Stack

## Backend

- Python
- FastAPI
- LangGraph
- LangChain
- Pydantic

## Frontend

- React
- Vite
- Axios
- React Markdown
- Tailwind CSS

## AI

- NVIDIA Foundation Models
- Prompt Engineering
- Multi-Agent Workflow

---

# 📂 Project Structure

```
research-agent/

├── app/
│   ├── agents/
│   ├── api/
│   ├── graph/
│   ├── prompts/
│   ├── tools/
│   └── utils/
│
├── frontend/
│
├── tests/
│
├── README.md
│
└── requirements.txt
```

---

# ✨ Workflow

1. User submits a research question.
2. Planner Agent creates an execution plan.
3. Tool Executor gathers relevant information.
4. Writer Agent generates a structured report.
5. Critic Agent evaluates report quality.
6. If needed, the Rewriter Agent improves the report.
7. Final report is displayed in the React frontend.

---

# 📦 Installation

## Clone Repository

```bash
git clone git@github.com:rishikesh0012/research-agent-.git
cd research-agent-
```

## Backend Setup

```bash
python -m venv venv

source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

Create a `.env` file and configure:

```env
NVIDIA_API_KEY=your_key
NVIDIA_MODEL=your_model
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
TAVILY_API_KEY=your_key
```

Run the backend

```bash
uvicorn app.main:app --reload
```

Backend

```
http://localhost:8000
```

Swagger

```
http://localhost:8000/docs
```

---

## Frontend Setup

```bash
cd frontend
```

```bash
npm install
```

```bash
npm run dev
```

Frontend

```
http://localhost:5173
```

---

# 📡 API Endpoint

### POST

```
/api/v1/research
```

Example

```json
{
  "question": "Compare RAG, Fine-Tuning and AI Agents",
  "max_retries": 1,
  "timeout_seconds": 300
}
```

---

# 📸 Screenshots

### Home Page

_Add screenshot_

### Research Report

_Add screenshot_

### Swagger API

_Add screenshot_

---

# 🔮 Future Improvements

- Streaming responses
- Citation support
- Multiple search providers
- PDF export
- Authentication
- Docker deployment
- CI/CD pipeline
- Cloud deployment

---

# 🧪 Testing

```bash
pytest
```

---

# 📄 License

MIT License

---

# 👨‍💻 Author

**Rishikesh KG**

AI Engineer | Generative AI | Machine Learning | Full-Stack AI Development

GitHub: https://github.com/rishikesh0012

---

⭐ If you found this project useful, consider giving it a star.
