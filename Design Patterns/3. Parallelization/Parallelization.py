"""
Parallelization Pattern Example using LangChain

This example demonstrates how to execute multiple independent LLM calls
concurrently to significantly reduce total execution time. We'll compare
sequential execution vs. parallel execution using Python's asyncio.
"""

import os
import sys
import time
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Configure UTF-8 encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Add parent directory to path to import common module
sys.path.insert(0, str(Path(__file__).parent.parent))
import common

# Load environment variables from .env file
load_dotenv()

# Get pre-configured HTTP clients for corporate networks (both sync and async)
http_client = common.get_http_client()

# For async operations, we need an async httpx client
import httpx
async_http_client = httpx.AsyncClient(verify=False)

# Initialize the LLM with both sync and async HTTP clients
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    http_client=http_client,
    http_async_client=async_http_client
)


# ============================================================
# STEP 1: Define Multiple Independent Chains
# ============================================================

# Chain 1: Generate a blog post title
title_prompt = ChatPromptTemplate.from_template(
    "Create a catchy, SEO-friendly blog post title about: {topic}\n"
    "The title should be engaging and under 60 characters."
)
title_chain = title_prompt | llm | StrOutputParser()

# Chain 2: Generate a meta description
meta_prompt = ChatPromptTemplate.from_template(
    "Write a compelling meta description for a blog post about: {topic}\n"
    "Keep it under 155 characters and include a call-to-action."
)
meta_chain = meta_prompt | llm | StrOutputParser()

# Chain 3: Generate a social media post
social_prompt = ChatPromptTemplate.from_template(
    "Create an engaging social media post (Twitter/X style) about: {topic}\n"
    "Keep it under 280 characters and make it shareable."
)
social_chain = social_prompt | llm | StrOutputParser()

# Chain 4: Generate relevant hashtags
hashtag_prompt = ChatPromptTemplate.from_template(
    "Generate 5 relevant and trending hashtags for a blog post about: {topic}\n"
    "Format as a comma-separated list."
)
hashtag_chain = hashtag_prompt | llm | StrOutputParser()


# ============================================================
# STEP 2: Sequential Execution (Traditional Approach)
# ============================================================

def execute_sequentially(topic: str) -> dict:
    """
    Execute all chains one after another (sequential).

    Args:
        topic: The blog post topic

    Returns:
        dict with all generated content and execution time
    """
    start_time = time.time()

    # Execute each chain one at a time
    title = title_chain.invoke({"topic": topic})
    meta = meta_chain.invoke({"topic": topic})
    social = social_chain.invoke({"topic": topic})
    hashtags = hashtag_chain.invoke({"topic": topic})

    end_time = time.time()
    execution_time = end_time - start_time

    return {
        "title": title,
        "meta_description": meta,
        "social_post": social,
        "hashtags": hashtags,
        "execution_time": execution_time
    }


# ============================================================
# STEP 3: Parallel Execution (Parallelization Pattern)
# ============================================================

async def execute_in_parallel(topic: str) -> dict:
    """
    Execute all chains concurrently using asyncio.

    Args:
        topic: The blog post topic

    Returns:
        dict with all generated content and execution time
    """
    start_time = time.time()

    # Execute all chains concurrently using asyncio.gather()
    # The ainvoke() method is the async version of invoke()
    results = await asyncio.gather(
        title_chain.ainvoke({"topic": topic}),
        meta_chain.ainvoke({"topic": topic}),
        social_chain.ainvoke({"topic": topic}),
        hashtag_chain.ainvoke({"topic": topic})
    )

    end_time = time.time()
    execution_time = end_time - start_time

    return {
        "title": results[0],
        "meta_description": results[1],
        "social_post": results[2],
        "hashtags": results[3],
        "execution_time": execution_time
    }


# ============================================================
# STEP 4: Helper Function to Run Async Code
# ============================================================

def run_parallel(topic: str) -> dict:
    """
    Wrapper to run async parallel execution.

    Args:
        topic: The blog post topic

    Returns:
        dict with all generated content and execution time
    """
    return asyncio.run(execute_in_parallel(topic))


# ============================================================
# EXAMPLES: Compare Sequential vs. Parallel Execution
# ============================================================

def print_results(results: dict, execution_type: str):
    """Helper function to print results in a formatted way."""
    print(f"\n{execution_type.upper()} RESULTS:")
    print(f"{'=' * 80}")
    print(f"Title: {results['title']}")
    print(f"\nMeta Description: {results['meta_description']}")
    print(f"\nSocial Post: {results['social_post']}")
    print(f"\nHashtags: {results['hashtags']}")
    print(f"\nExecution Time: {results['execution_time']:.2f} seconds")
    print(f"{'=' * 80}")


# Example topic
topic = "The future of AI in healthcare and medical diagnostics"

print("=" * 80)
print("PARALLELIZATION PATTERN DEMONSTRATION")
print("=" * 80)
print(f"\nTopic: {topic}\n")
print("We will generate 4 pieces of content:")
print("  1. Blog post title")
print("  2. Meta description")
print("  3. Social media post")
print("  4. Hashtags")
print("\nComparing sequential vs. parallel execution...\n")


# ============================================================
# RUN SEQUENTIAL EXECUTION
# ============================================================

print("[Sequential] Running Sequential Execution...")
print("   (Each task waits for the previous one to complete)")
sequential_results = execute_sequentially(topic)
print_results(sequential_results, "Sequential")


# ============================================================
# RUN PARALLEL EXECUTION
# ============================================================

print("\n\n[Parallel] Running Parallel Execution...")
print("   (All tasks run concurrently)")
parallel_results = run_parallel(topic)
print_results(parallel_results, "Parallel")


# ============================================================
# PERFORMANCE COMPARISON
# ============================================================

speedup = sequential_results['execution_time'] / parallel_results['execution_time']
time_saved = sequential_results['execution_time'] - parallel_results['execution_time']

print("\n" + "=" * 80)
print("PERFORMANCE COMPARISON")
print("=" * 80)
print(f"Sequential Time:  {sequential_results['execution_time']:.2f} seconds")
print(f"Parallel Time:    {parallel_results['execution_time']:.2f} seconds")
print(f"\nSpeedup:          {speedup:.2f}x faster")
print(f"Time Saved:       {time_saved:.2f} seconds")
print("=" * 80)
