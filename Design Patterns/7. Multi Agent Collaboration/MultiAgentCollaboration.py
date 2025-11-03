# -*- coding: utf-8 -*-
"""
Multi-Agent Collaboration Pattern Example using LangChain

This example demonstrates how multiple specialized agents can collaborate
to accomplish a complex task. Each agent has a specific role and contributes
their expertise in a sequential workflow.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field

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
# PYDANTIC MODEL FOR RESEARCH OUTPUT
# ============================================================

class ResearchNotes(BaseModel):
    """Structured research notes from the Researcher agent"""
    topic: str = Field(description="The research topic")
    key_points: list[str] = Field(description="Key findings and important points")
    sources: list[str] = Field(description="Types of sources consulted (simulated)")
    summary: str = Field(description="Brief summary of the research")


# ============================================================
# AGENT 1: RESEARCHER
# ============================================================

researcher_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert researcher. Your role is to gather information on a given topic and organize it into structured research notes.

Your research should:
- Identify key concepts and important points
- Note relevant facts and data
- Organize information logically
- Provide a clear summary

You have access to knowledge from your training data. Simulate consulting various sources."""),
    ("human", "Research the following topic and provide structured notes:\n\nTopic: {topic}")
])

researcher_agent = researcher_prompt | llm.with_structured_output(ResearchNotes)


# ============================================================
# AGENT 2: WRITER
# ============================================================

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert content writer. Your role is to transform research notes into engaging, well-written blog posts.

Your writing should:
- Be clear and engaging
- Have a logical flow with introduction, body, and conclusion
- Use the research accurately
- Be accessible to a general technical audience
- Include relevant examples or analogies

Transform dry research into compelling content."""),
    ("human", """Using the following research notes, write an engaging blog post:

Topic: {topic}
Key Points:
{key_points}

Summary: {summary}

Write a complete blog post (400-600 words) based on this research.""")
])

writer_agent = writer_prompt | llm | StrOutputParser()


# ============================================================
# AGENT 3: EDITOR
# ============================================================

editor_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a meticulous editor. Your role is to review and polish written content for publication.

Your editing should focus on:
- Clarity and readability
- Grammar and punctuation
- Flow and coherence
- Removing redundancy
- Ensuring professional tone
- Adding polish and refinement

Provide the final, publication-ready version."""),
    ("human", """Review and edit the following blog post. Provide the final polished version:

{blog_draft}

Return the complete edited version.""")
])

editor_agent = editor_prompt | llm | StrOutputParser()


# ============================================================
# ORCHESTRATION: MULTI-AGENT WORKFLOW
# ============================================================

def content_creation_workflow(topic: str) -> dict:
    """
    Orchestrates the multi-agent collaboration workflow.

    Args:
        topic: The topic to create content about

    Returns:
        Dictionary with outputs from each agent
    """
    print(f"Topic: {topic}\n")
    print("=" * 80)

    # Step 1: Researcher Agent
    print("STEP 1: Research Phase")
    print("=" * 80)
    print("Researcher Agent is gathering information...\n")

    research_notes = researcher_agent.invoke({"topic": topic})

    print(f"Topic: {research_notes.topic}")
    print(f"\nKey Points:")
    for i, point in enumerate(research_notes.key_points, 1):
        print(f"  {i}. {point}")
    print(f"\nSummary: {research_notes.summary}")
    print(f"\nSources Referenced: {', '.join(research_notes.sources)}")
    print("\n")

    # Step 2: Writer Agent
    print("=" * 80)
    print("STEP 2: Writing Phase")
    print("=" * 80)
    print("Writer Agent is creating the blog post...\n")

    key_points_text = "\n".join([f"- {point}" for point in research_notes.key_points])

    blog_draft = writer_agent.invoke({
        "topic": research_notes.topic,
        "key_points": key_points_text,
        "summary": research_notes.summary
    })

    print("Draft Blog Post:")
    print("-" * 80)
    print(blog_draft)
    print("-" * 80)
    print("\n")

    # Step 3: Editor Agent
    print("=" * 80)
    print("STEP 3: Editing Phase")
    print("=" * 80)
    print("Editor Agent is reviewing and polishing...\n")

    final_post = editor_agent.invoke({"blog_draft": blog_draft})

    print("Final Polished Blog Post:")
    print("-" * 80)
    print(final_post)
    print("-" * 80)
    print("\n")

    return {
        "research_notes": research_notes,
        "draft": blog_draft,
        "final": final_post
    }


# ============================================================
# EXAMPLE: Create a Blog Post with Multi-Agent Team
# ============================================================
print("=" * 80)
print("MULTI-AGENT COLLABORATION EXAMPLE")
print("Creating a Blog Post with Researcher, Writer, and Editor")
print("=" * 80)
print()

topic = "The benefits and challenges of using LangChain for building AI agents"

result = content_creation_workflow(topic)

print("=" * 80)
print("WORKFLOW COMPLETE")
print("=" * 80)
print("\nThe three specialized agents successfully collaborated:")
print("1. Researcher: Gathered and organized information")
print("2. Writer: Transformed research into engaging content")
print("3. Editor: Polished and refined for publication")
print("\nEach agent contributed their unique expertise to produce the final result.")
