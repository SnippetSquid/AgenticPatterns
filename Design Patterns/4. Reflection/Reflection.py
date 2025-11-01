"""
Reflection Pattern Example using LangGraph

This example demonstrates the Producer-Critic model using LangGraph's StateGraph.
LangGraph is ideal for reflection because it supports stateful, cyclic workflows
with conditional routing - perfect for iterative refinement.
"""

import os
import sys
from pathlib import Path
from typing import List, TypedDict, Annotated, Dict, Any
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
    """Structured feedback from the Critic agent with multi-dimensional scoring"""
    overall_assessment: str = Field(description="Brief overall assessment of the draft")
    strengths: List[str] = Field(description="List of strengths in the current draft")
    issues: List[str] = Field(description="List of specific issues that need improvement")

    # Multi-dimensional scores (1-100 each)
    clarity_score: int = Field(description="Clarity: Is the writing clear and easy to understand? (1-100)")
    structure_score: int = Field(description="Structure: Does it have good flow and logical organization? (1-100)")
    engagement_score: int = Field(description="Engagement: Is it interesting and does it hook the reader? (1-100)")
    accuracy_score: int = Field(description="Accuracy: Is the content accurate and well-reasoned? (1-100)")
    completeness_score: int = Field(description="Completeness: Does it adequately cover the topic? (1-100)")
    cta_score: int = Field(description="Call-to-action: Is there a clear and compelling CTA? (1-100)")

    @property
    def overall_score(self) -> int:
        """Calculate overall score as average of all dimensions"""
        return (self.clarity_score + self.structure_score + self.engagement_score +
                self.accuracy_score + self.completeness_score + self.cta_score) // 6


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
    score_history: Annotated[List[Dict[str, Any]], operator.add]  # List of score snapshots
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

Evaluate the post on SIX specific dimensions (each scored 1-100):

1. **Clarity** (1-100): Is the writing clear and easy to understand? Are sentences concise? Is jargon explained?
   - 60-69: Confusing sections, unclear wording
   - 70-79: Mostly clear with minor issues
   - 80-89: Clear and well-written
   - 90-100: Exceptionally clear and crisp

2. **Structure** (1-100): Does it have good flow and logical organization? Are transitions smooth?
   - 60-69: Poor organization, lacks flow
   - 70-79: Decent structure with some issues
   - 80-89: Well-organized and logical
   - 90-100: Perfect structure and flow

3. **Engagement** (1-100): Does it hook the reader? Is it interesting throughout?
   - 60-69: Boring, lacks hook
   - 70-79: Somewhat engaging
   - 80-89: Engaging and interesting
   - 90-100: Highly compelling

4. **Accuracy** (1-100): Is the content accurate, well-reasoned, and credible?
   - 60-69: Questionable claims or logic
   - 70-79: Mostly accurate with minor issues
   - 80-89: Accurate and well-reasoned
   - 90-100: Exceptionally credible

5. **Completeness** (1-100): Does it adequately cover the topic? Are examples sufficient?
   - 60-69: Missing key information
   - 70-79: Covers basics but lacks depth
   - 80-89: Thorough coverage
   - 90-100: Comprehensive and complete

6. **Call-to-action** (1-100): Is there a clear, specific, and compelling CTA?
   - 60-69: Weak or missing CTA
   - 70-79: Generic CTA
   - 80-89: Clear and actionable CTA
   - 90-100: Highly compelling CTA

Provide structured feedback with:
- Overall assessment (brief summary)
- List of strengths (what's working well)
- List of specific issues to address (be specific and actionable)
- Individual score for EACH of the 6 dimensions

IMPORTANT: Use the full 1-100 range. Be specific and show meaningful differences between iterations.
    """

    structured_llm = llm.with_structured_output(Critique)
    critique = structured_llm.invoke(prompt)

    print(f"\n--- EDITORIAL FEEDBACK ---")
    print(f"Overall Assessment: {critique.overall_assessment}")

    print(f"\n📊 Dimensional Scores:")
    print(f"  Clarity:       {critique.clarity_score}/100")
    print(f"  Structure:     {critique.structure_score}/100")
    print(f"  Engagement:    {critique.engagement_score}/100")
    print(f"  Accuracy:      {critique.accuracy_score}/100")
    print(f"  Completeness:  {critique.completeness_score}/100")
    print(f"  CTA:           {critique.cta_score}/100")
    print(f"  ─────────────────────────")
    print(f"  Overall:       {critique.overall_score}/100")

    print(f"\nStrengths:")
    for strength in critique.strengths:
        print(f"  + {strength}")

    if critique.issues:
        print(f"\nIssues to Address:")
        for issue in critique.issues:
            print(f"  - {issue}")
    print()

    # Create score snapshot for history tracking (use dict instead of TypedDict)
    score_snapshot = {
        "iteration": iteration,
        "clarity": critique.clarity_score,
        "structure": critique.structure_score,
        "engagement": critique.engagement_score,
        "accuracy": critique.accuracy_score,
        "completeness": critique.completeness_score,
        "cta": critique.cta_score,
        "overall": critique.overall_score
    }


    # Prepare feedback for next iteration
    feedback_parts = [f"Overall: {critique.overall_assessment}"]
    feedback_parts.append(f"Current overall score: {critique.overall_score}/100")
    feedback_parts.append(f"Dimension scores - Clarity:{critique.clarity_score} Structure:{critique.structure_score} Engagement:{critique.engagement_score} Accuracy:{critique.accuracy_score} Completeness:{critique.completeness_score} CTA:{critique.cta_score}")

    for issue in critique.issues:
        feedback_parts.append(f"- {issue}")

    new_feedback = "\n".join(feedback_parts)

    return {
        "feedback_history": [new_feedback],
        "quality_score": critique.overall_score,
        "score_history": [score_snapshot],
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
    # Create the graph with explicit configuration for list accumulation
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
    # Note: The Annotated[List[...], operator.add] in TypedDict should handle accumulation
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
    "score_history": [],
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

# Run the graph with streaming (mode="values" gives full state, not just updates)
final_state = None
iteration_count = 0
for state_snapshot in app.stream(initial_state, config, stream_mode="values"):
    # Track the complete state at each step
    final_state = state_snapshot

    # Check if we just completed a critic evaluation (iteration increased)
    if state_snapshot.get("iteration", 1) > iteration_count + 1:
        iteration_count = state_snapshot["iteration"] - 1
        print("=" * 80)
        print(f"ITERATION {iteration_count}")
        print("=" * 80)

print(f"\n{'=' * 80}")
print("REFLECTION PROCESS COMPLETE")
print(f"{'=' * 80}")
print(f"Total Iterations: {final_state['iteration'] - 1}")
print(f"Final Quality Score: {final_state['quality_score']}/100 (Target: {target_score}+)")

# Display score evolution
print(f"\n{'=' * 80}")
print("SCORE EVOLUTION ACROSS ITERATIONS")
print(f"{'=' * 80}\n")

score_history = final_state['score_history']

# Print header
print(f"{'Iter':<6} {'Clarity':<9} {'Structure':<11} {'Engage':<9} {'Accuracy':<10} {'Complete':<10} {'CTA':<6} {'Overall':<8}")
print("─" * 80)

# Print each iteration's scores
for snapshot in score_history:
    print(f"{snapshot['iteration']:<6} "
          f"{snapshot['clarity']:<9} "
          f"{snapshot['structure']:<11} "
          f"{snapshot['engagement']:<9} "
          f"{snapshot['accuracy']:<10} "
          f"{snapshot['completeness']:<10} "
          f"{snapshot['cta']:<6} "
          f"{snapshot['overall']:<8}")

# Calculate improvements
if len(score_history) > 1:
    first = score_history[0]
    last = score_history[-1]

    print("\n" + "─" * 80)
    print("IMPROVEMENTS FROM FIRST TO FINAL DRAFT:")
    print("─" * 80)

    improvements = {
        "Clarity": last['clarity'] - first['clarity'],
        "Structure": last['structure'] - first['structure'],
        "Engagement": last['engagement'] - first['engagement'],
        "Accuracy": last['accuracy'] - first['accuracy'],
        "Completeness": last['completeness'] - first['completeness'],
        "CTA": last['cta'] - first['cta'],
        "Overall": last['overall'] - first['overall']
    }

    for dimension, improvement in improvements.items():
        sign = "+" if improvement >= 0 else ""
        print(f"  {dimension:<14} {sign}{improvement:>3} points")

print("\n" + "=" * 80)

