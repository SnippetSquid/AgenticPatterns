# -*- coding: utf-8 -*-
"""
Tool Use Pattern Example using LangChain

This example demonstrates how to create tools that an LLM agent can use
to extend its capabilities beyond its training data. The agent learns to
decide when and how to use these tools based on the user's request.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from pydantic import BaseModel, Field
from typing import Literal

# Add parent directory to path to import common module
sys.path.insert(0, str(Path(__file__).parent.parent))
import common

# Configure UTF-8 encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables from .env file
load_dotenv()

# Get pre-configured HTTP client for corporate networks
http_client = common.get_http_client()

# Initialize the LLM with the custom HTTP client
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    http_client=http_client
)


# ============================================================
# TOOL DEFINITIONS
# ============================================================

class CalculatorInput(BaseModel):
    """Input schema for the calculator tool"""
    operation: Literal["add", "subtract", "multiply", "divide"] = Field(
        description="The mathematical operation to perform"
    )
    a: float = Field(description="The first number")
    b: float = Field(description="The second number")


@tool(args_schema=CalculatorInput)
def calculator(operation: str, a: float, b: float) -> str:
    """
    Performs basic mathematical calculations.
    Use this tool when you need to perform arithmetic operations.
    """
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else "Error: Division by zero"
    }

    if operation in operations:
        result = operations[operation](a, b)
        return f"The result of {a} {operation} {b} is: {result}"
    else:
        return f"Error: Unknown operation '{operation}'"


class WeatherInput(BaseModel):
    """Input schema for the weather tool"""
    city: str = Field(description="The name of the city to get weather for")


@tool(args_schema=WeatherInput)
def get_weather(city: str) -> str:
    """
    Retrieves current weather information for a given city.
    Use this tool when you need to check the weather in a specific location.
    """
    # Mock weather data (in a real application, this would call a weather API)
    weather_data = {
        "london": "Cloudy with occasional rain, 15�C (59�F)",
        "paris": "Partly sunny, 18�C (64�F)",
        "tokyo": "Clear skies, 22�C (72�F)",
        "new york": "Sunny, 20�C (68�F)",
        "san francisco": "Foggy morning clearing to sun, 16�C (61�F)",
        "sydney": "Warm and sunny, 25�C (77�F)",
    }

    city_lower = city.lower()
    if city_lower in weather_data:
        return f"Weather in {city.title()}: {weather_data[city_lower]}"
    else:
        return f"Weather data for {city} is not available. Available cities: {', '.join([c.title() for c in weather_data.keys()])}"


# ============================================================
# BIND TOOLS TO LLM
# ============================================================

# Create a list of tools
tools = [calculator, get_weather]

# Create a mapping of tool names to tool functions for easy execution
tools_map = {t.name: t for t in tools}

# Bind the tools to the LLM - this tells the LLM what tools are available
llm_with_tools = llm.bind_tools(tools)


# ============================================================
# HELPER FUNCTION: Execute Agent Loop
# ============================================================

def run_agent(user_input: str, max_iterations: int = 5) -> str:
    """
    Runs the agent loop: LLM -> Tool Call -> Tool Execution -> LLM -> Response

    Args:
        user_input: The user's question or request
        max_iterations: Maximum number of tool calls to prevent infinite loops

    Returns:
        The final response from the LLM
    """
    messages = [HumanMessage(content=user_input)]
    iterations = 0

    print(f"User Input: {user_input}\n")

    while iterations < max_iterations:
        # Invoke the LLM
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        # Check if the LLM wants to call any tools
        if not response.tool_calls:
            # No tool calls - the LLM has provided a final answer
            print(f"Final Response: {response.content}\n")
            return response.content

        # The LLM wants to use tools
        iterations += 1
        print(f"--- Tool Call Iteration {iterations} ---")

        # Execute each tool call
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id = tool_call["id"]

            print(f"Tool: {tool_name}")
            print(f"Arguments: {tool_args}")

            # Execute the tool
            selected_tool = tools_map[tool_name]
            tool_output = selected_tool.invoke(tool_args)

            print(f"Tool Output: {tool_output}\n")

            # Add the tool result to messages
            messages.append(ToolMessage(
                content=tool_output,
                tool_call_id=tool_id
            ))

    return "Maximum iterations reached"


# ============================================================
# EXAMPLE 1: Using the Calculator Tool
# ============================================================
print("=" * 60)
print("EXAMPLE 1: Mathematical Calculation")
print("=" * 60)

run_agent("What is 1,234 multiplied by 56?")


# ============================================================
# EXAMPLE 2: Using the Weather Tool
# ============================================================
print("=" * 60)
print("EXAMPLE 2: Weather Lookup")
print("=" * 60)

run_agent("What's the weather like in Tokyo?")


# ============================================================
# EXAMPLE 3: Agent Decides No Tool Needed
# ============================================================
print("=" * 60)
print("EXAMPLE 3: No Tool Required")
print("=" * 60)

run_agent("What is the capital of France?")


# ============================================================
# EXAMPLE 4: Complex Query (Multiple Tool Usage)
# ============================================================
print("=" * 60)
print("EXAMPLE 4: Multiple Tool Usage")
print("=" * 60)

run_agent("If it's 22°C in Tokyo and 15°C in London, what's the temperature difference in Celsius?")
