# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a learning repository for **Agentic AI Patterns** using LangChain. Each pattern is organized in its own numbered directory (e.g., `1. Prompt Chaining/`) containing:
- A Python implementation file (`.py`)
- A markdown explanation file (`.md`)

## Project Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment configuration:**
   - Copy `.env.example` to `.env`
   - Add your `OPENAI_API_KEY` to `.env`

3. **Run examples:**
   ```bash
   python "1. Prompt Chaining/PromptChaining.py"
   ```

## Architecture

Each pattern directory follows this structure:
- **Python file**: Runnable example with inline comments
- **Markdown file**: Conceptual explanation (no code, just logical steps)

### Key Implementation Details

- All examples use **LangChain** with **OpenAI** models
- Examples use `httpx.Client(verify=False)` for corporate network compatibility
- Environment variables loaded via `python-dotenv`
- LangChain chains use the pipe operator (`|`) pattern: `prompt | llm | StrOutputParser()`

## Adding New Patterns

When adding a new pattern:
1. Create a numbered directory: `N. Pattern Name/`
2. Add `PatternName.py` - implementation with docstrings and examples
3. Add `PatternName.md` - conceptual overview without code examples
4. Keep markdown concise (focus on when/why, not how)
5. Update top-level README if exists
