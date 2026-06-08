# Workflow Weaver

Workflow Weaver is a compact Python task runner for dependency-aware automation. Define tasks as Python functions, declare dependencies, and run them in a predictable topological order with retry support.

## Highlights

- No runtime dependencies
- Cycle detection with readable error messages
- Retry support for flaky steps
- Small enough to understand, useful enough to demo

## Quick start

```bash
python -m pip install -e .
python examples/build_pipeline.py
```

## Development

```bash
python -m pytest
```
