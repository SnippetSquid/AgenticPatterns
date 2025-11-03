# Tool Use

## Overview

The Tool Use pattern, often implemented through a mechanism called Function Calling, enables an agent to interact with external APIs, databases, services, or even execute code. It allows the LLM at the core of the agent to decide when and how to use a specific external function based on the user's request or the current state of the task.

This pattern is fundamental because it breaks the limitations of the LLM's training data and allows it to access up-to-date information, perform calculations it can't do internally, interact with user-specific data, or trigger real-world actions. Without Tool Use, LLMs are constrained by their knowledge cutoff date and internal reasoning capabilities alone. With tools, they become dynamic agents capable of real-world interactions.

While "function calling" aptly describes invoking specific, predefined code functions, it's useful to consider the more expansive concept of "tool calling." This broader term acknowledges that an agent's capabilities can extend far beyond simple function execution. A "tool" can be a traditional function, but it can also be a complex API endpoint, a request to a database, or even an instruction directed to another specialized agent. This perspective allows us to envision more sophisticated systems where, for instance, a primary agent might delegate a complex data analysis task to a dedicated "analyst agent" or query an external knowledge base through its API. Thinking in terms of "tool calling" better captures the full potential of agents to act as orchestrators across a diverse ecosystem of digital resources and other intelligent entities.

**Benefits:**
- Extends LLM capabilities beyond training data
- Enables access to real-time information
- Performs precise calculations and data operations
- Interacts with external systems and databases
- Delegates specialized tasks to other agents or services

## How It Works

```
User Query → LLM (with tools) → Tool Call Decision → Execute Tool → Tool Result → LLM → Final Response
```

The Tool Use process typically involves:

1. **Tool Definition**: External functions or capabilities are defined and described to the LLM. This description includes the function's purpose, its name, and the parameters it accepts, along with their types and descriptions.

2. **LLM Decision**: The LLM receives the user's request and the available tool definitions. Based on its understanding of the request and the tools, the LLM decides if calling one or more tools is necessary to fulfill the request.

3. **Function Call Generation**: If the LLM decides to use a tool, it generates a structured output (often a JSON object) that specifies the name of the tool to call and the arguments (parameters) to pass to it, extracted from the user's request.

4. **Tool Execution**: The agentic framework or orchestration layer intercepts this structured output. It identifies the requested tool and executes the actual external function with the provided arguments.

5. **Observation/Result**: The output or result from the tool execution is returned to the agent.

6. **LLM Processing**: The LLM receives the tool's output as context and uses it to formulate a final response to the user or decide on the next step in the workflow (which might involve calling another tool, reflecting, or providing a final answer).

## Example

The example demonstrates a simple agent with two tools:
1. **Calculator Tool** - Performs basic arithmetic operations (add, subtract, multiply, divide)
2. **Weather Tool** - Retrieves mock weather information for various cities

The agent intelligently decides:
- **When to use tools** - "What is 1,234 multiplied by 56?" → Uses calculator
- **Which tool to use** - "What's the weather in Tokyo?" → Uses weather lookup
- **When tools aren't needed** - "What is the capital of France?" → Answers directly
- **Multiple tool usage** - "Temperature difference between Tokyo and London?" → Uses calculator after understanding the question

## Implementation Steps

1. **Define tools with schemas** - Create tool functions decorated with `@tool` and define input schemas using Pydantic models
2. **Bind tools to LLM** - Use `llm.bind_tools()` to make the LLM aware of available tools
3. **Implement agent loop** - Create a loop that invokes the LLM, checks for tool calls, executes tools, and feeds results back
4. **Handle tool execution** - Map tool names to functions and execute with provided arguments
5. **Feed results back to LLM** - Add tool results as ToolMessages to the conversation history
6. **Extract final answer** - When no more tool calls are needed, return the LLM's response

## When to Use

**Use when:**
- Tasks require real-time or up-to-date information
- You need precise calculations beyond LLM reasoning
- Accessing databases, APIs, or external services
- Interacting with user-specific data
- Triggering real-world actions (sending emails, creating tickets, etc.)
- Delegating specialized tasks to other agents or services

**Avoid when:**
- Task can be solved with LLM knowledge alone
- Tool execution is expensive or slow
- Security concerns with automated function execution
- Tools would add unnecessary complexity
- Response latency is critical and tools would slow it down

## Advanced Considerations

**Tool Selection Strategy**: When multiple tools are available, the LLM must intelligently choose which tool to use. This decision-making can be enhanced through clear, descriptive tool definitions and examples in the tool docstrings. Consider providing context about when each tool should be used to improve selection accuracy.

**Error Handling**: Tools can fail—APIs may be down, calculations may encounter errors, or data may be unavailable. Robust implementations should handle tool failures gracefully, potentially allowing the LLM to try alternative approaches or inform the user about limitations.

**Tool Chaining**: Complex tasks may require using multiple tools in sequence. The agent loop should support iterative tool calls, where the result of one tool informs the selection and parameters of the next tool.

**Security and Permissions**: When tools interact with external systems, consider implementing authorization checks, rate limiting, and validation to prevent misuse. Not every tool should be accessible for every request—context-aware permission systems can add crucial safety layers.

## References
- OpenAI function calling guide: https://platform.openai.com/docs/guides/function-calling
- Anthropic Writing effective tools for agents: https://www.anthropic.com/engineering/writing-tools-for-agents