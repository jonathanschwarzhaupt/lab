# AI Tools Experiments

Exploring modern AI development tools and frameworks, particularly focusing on [PydanticAI](https://ai.pydantic.dev/) with Anthropic's Claude models.

## What's Here

**Transaction Categorization** (`simple_categorization.py`)
- Marimo notebook experimenting with financial transaction classification
- Uses PydanticAI agents for structured output and categorization
- Includes Logfire observability for monitoring AI interactions

**Dependencies**
- PydanticAI with Anthropic integration
- Marimo for interactive notebooks
- Logfire for observability and tracing

## Getting Started

This project uses uv for dependency management:

```bash
# Sync dependencies
uv sync

# Run the categorization notebook
uv run marimo edit simple_categorization.py
```

You'll need an Anthropic API key in your environment or `.env` file.