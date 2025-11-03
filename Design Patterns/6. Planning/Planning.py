# -*- coding: utf-8 -*-
"""
Planning Pattern Example using LangChain

This example demonstrates how an agent can break down complex goals into
structured, sequential plans. The focus is on plan generation - transforming
high-level objectives into concrete, actionable steps.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List, Optional

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
    temperature=0.7,
    http_client=http_client
)


# ============================================================
# PYDANTIC MODELS FOR STRUCTURED PLAN OUTPUT
# ============================================================

class PlanStep(BaseModel):
    """A single step in a plan"""
    step_number: int = Field(description="The sequential number of this step")
    description: str = Field(description="Clear description of what needs to be done")
    dependencies: Optional[List[int]] = Field(
        default=None,
        description="Step numbers that must be completed before this step (if any)"
    )
    estimated_effort: str = Field(
        description="Estimated time or effort (e.g., '2 hours', '1 day', '1 week')"
    )
    rationale: str = Field(
        description="Brief explanation of why this step is necessary"
    )


class Plan(BaseModel):
    """A complete plan for achieving a goal"""
    goal: str = Field(description="The original goal to be achieved")
    summary: str = Field(description="One-sentence overview of the approach")
    steps: List[PlanStep] = Field(description="Sequential list of steps to complete")
    total_estimated_effort: str = Field(
        description="Total estimated time to complete all steps"
    )


# ============================================================
# PLANNING PROMPT
# ============================================================

planning_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert strategic planner. Your role is to break down complex goals into clear, actionable plans.

When given a goal, you should:
1. Analyze what needs to be accomplished
2. Identify the logical sequence of steps
3. Note any dependencies between steps
4. Estimate the effort required for each step
5. Provide rationale for why each step is necessary

Create plans that are:
- Concrete and actionable (not vague)
- Logically sequenced (with clear dependencies)
- Realistic in scope and effort estimates
- Complete (covering all aspects of the goal)

Remember: A good plan transforms a complex goal into a clear roadmap."""),
    ("human", """Create a detailed plan to achieve the following goal:

Goal: {goal}

{context}""")
])

# Bind structured output to the LLM
planner = planning_prompt | llm.with_structured_output(Plan)


# ============================================================
# HELPER FUNCTION: Display Plan
# ============================================================

def display_plan(plan: Plan):
    """Format and display a plan in a readable way"""
    print(f"Goal: {plan.goal}")
    print(f"Strategy: {plan.summary}")
    print(f"Total Estimated Effort: {plan.total_estimated_effort}")
    print("\nPlan Steps:")
    print("=" * 80)

    for step in plan.steps:
        print(f"\nStep {step.step_number}: {step.description}")
        print(f"  Effort: {step.estimated_effort}")

        if step.dependencies:
            deps = ", ".join([f"Step {d}" for d in step.dependencies])
            print(f"  Dependencies: {deps}")

        print(f"  Rationale: {step.rationale}")

    print("\n" + "=" * 80 + "\n")


# ============================================================
# EXAMPLE 1: Software Feature Development
# ============================================================
print("=" * 80)
print("EXAMPLE 1: Software Feature Development")
print("=" * 80)
print()

goal1 = "Build a user authentication system with email/password login"
context1 = "Context: This is for a web application. We need secure authentication with password hashing."

plan1 = planner.invoke({
    "goal": goal1,
    "context": context1
})

display_plan(plan1)


# ============================================================
# EXAMPLE 2: Content Creation
# ============================================================
print("=" * 80)
print("EXAMPLE 2: Content Creation Plan")
print("=" * 80)
print()

goal2 = "Write a comprehensive blog series about AI agentic patterns"
context2 = "Context: Target audience is software developers. Series should be 5 posts covering different patterns with code examples."

plan2 = planner.invoke({
    "goal": goal2,
    "context": context2
})

display_plan(plan2)


# ============================================================
# EXAMPLE 3: Learning Plan
# ============================================================
print("=" * 80)
print("EXAMPLE 3: Learning Plan")
print("=" * 80)
print()

goal3 = "Learn React.js well enough to build production applications"
context3 = "Context: I have 2 weeks available, 2-3 hours per day. I already know JavaScript and HTML/CSS."

plan3 = planner.invoke({
    "goal": goal3,
    "context": context3
})

display_plan(plan3)
