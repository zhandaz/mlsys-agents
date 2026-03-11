# CLAUDE.md

## Project Overview

**mlsys-agents** is a monorepo of agent-native utilities for ML systems research and engineering.

## Setup

```bash
pip install -e .
```

Dependencies: `matplotlib>=3.9`, `numpy>=1.26`.

## Coding Conventions

- Python 3.12+ type hints (`list[str]` not `List[str]`, `X | None` not `Optional[X]`)
- Line length: 120
- Docstring convention: Google style
- Lint: `ruff` with `select = ["ALL"]` (see pyproject.toml for ignores)
- Format: `black` (line-length 120)
- Run `pre-commit run -a` before committing
