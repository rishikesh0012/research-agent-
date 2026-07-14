# Architecture Decisions

## 1. LangGraph for Orchestration

**Decision**: Use LangGraph instead of custom orchestration

**Rationale**:
- Industry-standard workflow management
- Built-in state management
- Conditional routing support
- Better debugging and tracing
- Active community support

## 2. Pydantic for Data Validation

**Decision**: Use Pydantic models for all data structures

**Rationale**:
- Strong type checking
- Built-in validation
- Automatic serialization
- JSON schema generation
- Industry standard

## 3. Async/Await Throughout

**Decision**: Use async/await for all I/O operations

**Rationale**:
- Better performance for I/O-bound tasks
- Improved scalability
- Natural concurrency model
- Better error handling

## 4. Single Retry for Critique

**Decision**: Allow only one rewrite pass after critique failure

**Rationale**:
- Prevents infinite loops
- Controls latency
- Balances quality with performance
- Configurable via settings

## 5. Rich Logging

**Decision**: Use Rich library for terminal output

**Rationale**:
- Beautiful formatted logs
- Better readability
- Built-in table/panel support
- Professional appearance

## 6. Tool Safety Restrictions

**Decision**: Whitelist approach for Python execution

**Rationale**:
- Prevent malicious code execution
- Control resource usage
- Audit trail of operations
- Production-safe

## 7. Evaluation File Storage

**Decision**: Store metrics in evaluation.json

**Rationale**:
- Simple, no database required
- Human-readable format
- Easy to analyze
- Git-friendly (can be ignored)
- Can be extended to database later

## 8. FastAPI for API

**Decision**: Use FastAPI for REST API

**Rationale**:
- Fast and modern
- Automatic OpenAPI/Swagger docs
- Built-in async support
- Type hint integration
- Excellent for production

## 9. Environment-Based Configuration

**Decision**: Load all config from environment variables

**Rationale**:
- 12-factor app compliance
- Security (no secrets in code)
- Easy deployment
- CI/CD friendly

## 10. Modular Package Structure

**Decision**: Organize into functional packages (agents, tools, graph, etc.)

**Rationale**:
- Clear separation of concerns
- Easy to test
- Easy to extend
- Maintainable
- Scalable
