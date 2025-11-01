"""
Reflection Pattern Example using LangGraph

This example demonstrates the Producer-Critic model using LangGraph's StateGraph.
LangGraph is ideal for reflection because it supports stateful, cyclic workflows
with conditional routing - perfect for iterative refinement.
"""

import os
import sys
from pathlib import Path
from typing import List, TypedDict, Annotated
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig
import operator
import uuid

# Configure UTF-8 encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Add parent directory to path to import common module
sys.path.insert(0, str(Path(__file__).parent.parent))
import common

# Load environment variables from .env file
load_dotenv()

# Get pre-configured HTTP client for corporate networks
http_client = common.get_http_client()

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    http_client=http_client
)


# ============================================================
# STEP 1: Define Structured Models
# ============================================================

class Critique(BaseModel):
    """Structured feedback from the Critic agent"""
    overall_assessment: str = Field(description="Brief overall assessment of the draft")
    strengths: List[str] = Field(description="List of strengths in the current draft")
    issues: List[str] = Field(description="List of specific issues that need improvement")
    quality_score: int = Field(description="Quality score from 1-100, where 80+ means ready to publish. Be specific and use the full range to show incremental improvements.")


# ============================================================
# STEP 2: Define Graph State
# ============================================================

class ReflectionState(TypedDict):
    """State that flows through the reflection graph"""
    topic: str
    draft: str
    feedback_history: Annotated[List[str], operator.add]
    iteration: int
    quality_score: int
    max_iterations: int
    target_score: int


# ============================================================
# STEP 3: Define Producer Node (Blog Writer)
# ============================================================

def producer_node(state: ReflectionState) -> ReflectionState:
    """
    Producer node that creates or refines a blog post based on feedback.
    """
    iteration = state["iteration"]

    print(f"\n[Producer] Creating draft {iteration}...")

    if iteration == 1:
        context = "This is your first draft."
        feedback_instruction = "Write a compelling first draft."
    else:
        context = f"This is iteration {iteration}. You are revising your previous draft based on editorial feedback."
        latest_feedback = state["feedback_history"][-1]
        previous_draft = state["draft"]
        feedback_instruction = f"""Previous draft:
---
{previous_draft}
---

Editorial feedback on this draft:
{latest_feedback}

Please revise the draft above to address all the issues mentioned in the feedback while preserving the strengths."""

    prompt = f"""You are a skilled blog writer creating engaging content.

    {context}

    Topic: {state["topic"]}

    Requirements:
    - Write a blog post of approximately 300-400 words
    - Include a compelling hook in the opening
    - Use clear structure with logical flow
    - Make it engaging and readable
    - Include a call-to-action at the end

    {feedback_instruction}

    Write the blog post:"""

    response = llm.invoke(prompt)
    draft = response.content

    print(f"\n--- DRAFT {iteration} ---")
    print(draft)
    print()

    return {
        "draft": draft
    }


# ============================================================
# STEP 4: Define Critic Node (Editor)
# ============================================================

def critic_node(state: ReflectionState) -> ReflectionState:
    """
    Critic node that evaluates the blog post and provides structured feedback.
    """
    iteration = state["iteration"]

    print(f"[Critic] Evaluating draft {iteration}...")

    prompt = f"""You are an experienced blog editor providing constructive feedback.

Evaluate the following blog post on the topic: "{state["topic"]}"

Blog Post:
{state["draft"]}

Evaluate the post based on these criteria:
    1. **Clarity**: Is the writing clear and easy to understand?
    2. **Structure**: Does it have good flow and logical organization?
    3. **Engagement**: Is it interesting and does it hook the reader?
    4. **Accuracy**: Is the content accurate and well-reasoned?
    5. **Completeness**: Does it adequately cover the topic?
    6. **Call-to-action**: Is there a clear and compelling CTA?

    Provide structured feedback with:
    - Overall assessment (brief summary)
    - List of strengths (what's working well)
    - List of specific issues to address (be specific and actionable)
    - Quality score (1-100, where 80+ means ready to publish)

    IMPORTANT: Use the full 1-100 range. Scores: 60-69 = significant issues, 70-79 = good but needs work, 80+ = publication-ready.
    """

    structured_llm = llm.with_structured_output(Critique)
    critique = structured_llm.invoke(prompt)

    print(f"\n--- EDITORIAL FEEDBACK ---")
    print(f"Overall Assessment: {critique.overall_assessment}")
    print(f"\nQuality Score: {critique.quality_score}/100")

    print(f"\nStrengths:")
    for strength in critique.strengths:
        print(f"  + {strength}")

    if critique.issues:
        print(f"\nIssues to Address:")
        for issue in critique.issues:
            print(f"  - {issue}")
    print()

    # Prepare feedback for next iteration
    feedback_parts = [f"Overall: {critique.overall_assessment}"]
    feedback_parts.append(f"Current score: {critique.quality_score}/100")

    for issue in critique.issues:
        feedback_parts.append(f"- {issue}")

    new_feedback = "\n".join(feedback_parts)

    return {
        "feedback_history": [new_feedback],
        "quality_score": critique.quality_score,
        "iteration": state["iteration"] + 1
    }


# ============================================================
# STEP 5: Define Conditional Edge
# ============================================================

def should_continue(state: ReflectionState) -> str:
    """
    Determines whether to continue iterating or end the process.
    """
    # Check if we've reached quality target
    if state["quality_score"] >= state["target_score"]:
        print("=" * 80)
        print("SUCCESS: Blog post meets quality standards!")
        print("=" * 80)
        return "end"

    # Check if we've hit max iterations
    if state["iteration"] > state["max_iterations"]:
        print("=" * 80)
        print("Maximum iterations reached.")
        print("=" * 80)
        return "end"

    # Continue iterating
    return "continue"


# ============================================================
# STEP 6: Build the Reflection Graph
# ============================================================

def create_reflection_graph():
    """
    Creates the reflection graph with Producer and Critic nodes.
    """
    # Create the graph
    workflow = StateGraph(ReflectionState)

    # Add nodes
    workflow.add_node("producer", producer_node)
    workflow.add_node("critic", critic_node)

    # Set entry point
    workflow.set_entry_point("producer")

    # Add edges
    workflow.add_edge("producer", "critic")

    # Add conditional edge from critic
    workflow.add_conditional_edges(
        "critic",
        should_continue,
        {
            "continue": "producer",
            "end": END
        }
    )

    # Compile the graph
    return workflow.compile()


# ============================================================
# EXAMPLE: Blog Post on AI in Education
# ============================================================

topic = "How AI is transforming personalized learning in education"
max_iterations = 10
target_score = 80

print("=" * 80)
print("REFLECTION PATTERN DEMONSTRATION (LangGraph)")
print("=" * 80)
print(f"\nTopic: {topic}")
print(f"Target Quality Score: {target_score}/100")
print(f"Maximum Iterations: {max_iterations}\n")

# Create and compile the graph
app = create_reflection_graph()

# Initialize state
initial_state = {
    "topic": topic,
    "draft": "",
    "feedback_history": [],
    "iteration": 1,
    "quality_score": 0,
    "max_iterations": max_iterations,
    "target_score": target_score
}

# Configure tracing for LangSmith
thread_id = str(uuid.uuid4())
config = RunnableConfig(
    configurable={"thread_id": thread_id},
    run_name="Reflection Pattern - Blog Post Refinement",
    tags=["reflection", "blog-writing", "iterative-improvement"],
    metadata={
        "topic": topic,
        "target_score": target_score,
        "max_iterations": max_iterations
    }
)

print(f"Thread ID: {thread_id}\n")

# Run the graph
for output in app.stream(initial_state, config):
    # Print iteration separator when critic completes
    if "critic" in output:
        print("=" * 80)
        print(f"ITERATION {output['critic']['iteration'] - 1}")
        print("=" * 80)

# Get final state
final_state = output[list(output.keys())[0]]

print(f"\n{'=' * 80}")
print("REFLECTION PROCESS COMPLETE")
print(f"{'=' * 80}")
print(f"Total Iterations: {final_state['iteration'] - 1}")
print(f"Final Quality Score: {final_state['quality_score']}/100 (Target: {target_score}+)")

print("\n" + "=" * 80)

