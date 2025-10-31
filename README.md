# Agentic AI Patterns with LangChain

A learning repository demonstrating practical implementations of Agentic AI design patterns using LangChain and OpenAI. Each pattern is presented with working code examples and conceptual documentation to help you understand when and how to apply these patterns in your own AI systems.

## What are Agentic AI Patterns?

Agentic AI systems are intelligent agents that can make decisions, perform actions, and adapt their behavior based on context. This repository explores fundamental design patterns that enable AI agents to handle complex, real-world tasks through structured workflows, dynamic decision-making, and specialized processing.

## Patterns Implemented

### 1. Prompt Chaining
**Location:** `Design Patterns/1. Prompt Chaining/`

Break complex tasks into sequential steps where each prompt's output feeds into the next. This pattern improves output quality by focusing on specific subtasks and provides better control through intermediate validation points.

**Use cases:**
- Multi-step content generation (e.g., product name → slogan → description)
- Data transformation pipelines
- Tasks requiring validation between steps

**Key files:**
- `PromptChaining.py` - Working implementation with examples
- `PromptChaining.md` - Conceptual overview

### 2. Routing
**Location:** `Design Patterns/2. Routing/`

Use an LLM to analyze input and dynamically route it to specialized handlers. This enables intelligent request classification and context-aware response generation through dedicated processing chains.

**Use cases:**
- Customer service systems (technical support, billing, product info)
- Multi-intent chatbots
- Content categorization and specialized processing

**Key files:**
- `Routing.py` - Customer service routing example
- `Routing.md` - Conceptual overview with routing mechanisms

### 3. Parallelization
**Location:** `Design Patterns/3. Parallelization/`

Execute multiple independent LLM operations concurrently to dramatically reduce total execution time. This pattern uses Python's asyncio to run multiple chains simultaneously, achieving significant speedups (often 2-4×) for independent tasks.

**Use cases:**
- Generating multiple pieces of content simultaneously
- Processing multiple documents or inputs at once
- Parallel data analysis or classification tasks
- Multi-aspect evaluation (sentiment, topics, entities) in parallel

**Key files:**
- `Parallelization.py` - Sequential vs parallel execution comparison
- `Parallelization.md` - Conceptual overview with performance analysis

## Getting Started

### Prerequisites
- Python 3.8+
- OpenAI API key


## Technologies Used

- **[LangChain](https://python.langchain.com/)** - Framework for building LLM applications
- **[OpenAI](https://openai.com/)** - LLM provider (GPT-4o-mini)
- **[Python-dotenv](https://github.com/theskumar/python-dotenv)** - Environment configuration
- **[Pydantic](https://docs.pydantic.dev/)** - Data validation and structured outputs

## Learning Resources

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [OpenAI API Documentation](https://platform.openai.com/docs/introduction)
- [Agentic AI Patterns Guide](https://www.anthropic.com/research/building-effective-agents)

## License

This is a learning repository intended for educational purposes.