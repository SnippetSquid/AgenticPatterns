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


### 2. Routing
**Location:** `Design Patterns/2. Routing/`

Use an LLM to analyze input and dynamically route it to specialized handlers. This enables intelligent request classification and context-aware response generation through dedicated processing chains.

**Use cases:**
- Customer service systems (technical support, billing, product info)
- Multi-intent chatbots
- Content categorization and specialized processing


### 3. Parallelization
**Location:** `Design Patterns/3. Parallelization/`

Execute multiple independent LLM operations concurrently to dramatically reduce total execution time. This pattern uses Python's asyncio to run multiple chains simultaneously, achieving significant speedups (often 2-4×) for independent tasks.

**Use cases:**
- Generating multiple pieces of content simultaneously
- Processing multiple documents or inputs at once
- Parallel data analysis or classification tasks
- Multi-aspect evaluation (sentiment, topics, entities) in parallel


### 4. Reflection
**Location:** `Design Patterns/4. Reflection/`

Enable agents to evaluate and iteratively improve their own outputs through a Producer-Critic model. This pattern uses LangGraph's stateful workflows to implement cyclic refinement, where a Critic agent provides structured feedback and a Producer agent incorporates improvements across multiple iterations.

**Use cases:**
- High-quality content creation requiring polish and refinement
- Tasks with complex quality criteria or style requirements
- Scenarios where iterative improvement adds significant value
- Self-improving systems that learn from feedback


### 5. Tool Use
**Location:** `Design Patterns/5. Tool Use/`

Enable agents to extend their capabilities by deciding when and how to use external tools, APIs, or functions. The LLM intelligently chooses which tools to invoke based on the user's request, executes them with appropriate parameters, and incorporates the results into its response.

**Use cases:**
- Accessing real-time or up-to-date information beyond training data
- Performing precise calculations (math, data operations)
- Interacting with external APIs, databases, or services
- Triggering real-world actions (sending emails, creating tickets)
- Delegating specialized tasks to other agents or tools


### 6. Planning
**Location:** `Design Patterns/6. Planning/`

Break down complex goals into structured, sequential plans with clear steps, dependencies, and effort estimates. This pattern transforms high-level objectives into actionable roadmaps, enabling goal-oriented behavior rather than reactive responses.

**Use cases:**
- Complex goals requiring multiple coordinated steps
- Project planning and task decomposition
- Scenarios where the "how" needs to be discovered, not prescribed
- Breaking ambiguous objectives into concrete actions
- Dynamic environments where plans may need adjustment


### 7. Multi-Agent Collaboration
**Location:** `Design Patterns/7. Multi Agent Collaboration/`

Structure systems as cooperative ensembles of specialized agents, each with distinct roles and expertise. Agents collaborate through sequential handoffs, parallel processing, or hierarchical coordination to accomplish tasks that exceed single-agent capabilities.

**Use cases:**
- Complex, multi-domain tasks requiring diverse expertise
- Content creation pipelines (research → writing → editing)
- Tasks that naturally decompose into specialized sub-tasks
- Systems requiring resilience through distributed processing
- Scenarios where agent specialization improves quality
- Modular architectures with clear separation of concerns


## Getting Started

### Prerequisites
- See requirements.txt


## Technologies Used

- **[LangChain](https://python.langchain.com/)** - Framework for building LLM applications
- **[LangGraph](https://langchain-ai.github.io/langgraph/)** - Framework for building stateful, multi-agent workflows with cycles
- **[OpenAI](https://openai.com/)** - LLM provider
- **[Python-dotenv](https://github.com/theskumar/python-dotenv)** - Environment configuration
- **[Pydantic](https://docs.pydantic.dev/)** - Data validation and structured outputs

## Learning Resources

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [OpenAI API Documentation](https://platform.openai.com/docs/introduction)
- [Anthropic - Agentic AI Patterns Guide](https://www.anthropic.com/research/building-effective-agents)
- [Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems, Antonio Gulli](https://docs.google.com/document/d/1rsaK53T3Lg5KoGwvf8ukOUvbELRtH-V0LnOIFDxBryE/)

