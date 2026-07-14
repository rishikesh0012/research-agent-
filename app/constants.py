"""Constants used throughout the application."""

# Tool types
TOOL_SEARCH = "search"
TOOL_PYTHON = "python"
TOOL_ANALYSIS = "analysis"

# Execution statuses
STATUS_PENDING = "pending"
STATUS_RUNNING = "running"
STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"

# Critic statuses
CRITIC_PASS = "PASS"
CRITIC_FAIL = "FAIL"

# Default timeouts (seconds)
DEFAULT_SEARCH_TIMEOUT = 30
DEFAULT_EXECUTION_TIMEOUT = 300
DEFAULT_LLM_TIMEOUT = 60

# Default limits
DEFAULT_MAX_RETRIES = 2
DEFAULT_MAX_RESEARCH_DEPTH = 5
DEFAULT_MAX_SEARCH_RESULTS = 10

# Quality score thresholds
QUALITY_PASS_THRESHOLD = 0.7  # Minimum average score to PASS
COMPLETENESS_WEIGHT = 0.4
CONSISTENCY_WEIGHT = 0.4
CLARITY_WEIGHT = 0.2
