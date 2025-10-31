"""
Routing Pattern Example using LangChain

This example demonstrates how to use an LLM to analyze input and route it
to the appropriate specialized chain. This is useful for building intelligent
systems that handle different types of requests differently.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from typing import Literal

# Add parent directory to path to import common module
sys.path.insert(0, str(Path(__file__).parent.parent))
import common

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
# STEP 1: Define the Routing Classification Model
# ============================================================

class RouteDecision(BaseModel):
    """Structured model for routing decisions"""
    category: Literal["technical_support", "billing", "product_info", "general"] = Field(
        description="The category of the customer inquiry"
    )
    confidence: str = Field(
        description="Confidence level: high, medium, or low"
    )
    reasoning: str = Field(
        description="Brief explanation of why this category was chosen"
    )


# ============================================================
# STEP 2: Create the Router Chain
# ============================================================

router_prompt = ChatPromptTemplate.from_template(
    """You are a customer service routing assistant. Analyze the customer inquiry and classify it into one of these categories:

Categories:
- technical_support: Issues with product functionality, bugs, errors, troubleshooting
- billing: Payment issues, invoices, refunds, pricing questions
- product_info: Questions about features, specifications, compatibility, availability
- general: General questions, feedback, or inquiries that don't fit other categories

Customer Inquiry: {inquiry}

Classify this inquiry and provide your confidence level and reasoning."""
)

# Router chain: inquiry -> classification
router_chain = router_prompt | llm.with_structured_output(RouteDecision)


# ============================================================
# STEP 3: Create Specialized Handler Chains
# ============================================================

# Technical Support Handler
technical_support_prompt = ChatPromptTemplate.from_template(
    """You are a technical support specialist. Help the customer with their technical issue.

Customer Issue: {inquiry}

Provide a helpful technical response with:
1. Acknowledgment of the issue
2. Possible causes
3. Step-by-step troubleshooting steps
4. When to escalate to engineering

Keep your response concise (3-4 sentences)."""
)
technical_support_chain = technical_support_prompt | llm | StrOutputParser()


# Billing Handler
billing_prompt = ChatPromptTemplate.from_template(
    """You are a billing specialist. Help the customer with their billing question or issue.

Customer Question: {inquiry}

Provide a helpful billing response with:
1. Acknowledgment of their concern
2. Clear explanation of billing details
3. Next steps or resolution
4. Contact information for complex billing issues

Keep your response concise (3-4 sentences)."""
)
billing_chain = billing_prompt | llm | StrOutputParser()


# Product Information Handler
product_info_prompt = ChatPromptTemplate.from_template(
    """You are a product specialist. Answer the customer's question about product features and specifications.

Customer Question: {inquiry}

Provide a helpful product response with:
1. Direct answer to their question
2. Relevant product details
3. Related features they might find useful
4. Where to find more detailed documentation

Keep your response concise (3-4 sentences)."""
)
product_info_chain = product_info_prompt | llm | StrOutputParser()


# General Handler
general_prompt = ChatPromptTemplate.from_template(
    """You are a friendly customer service representative. Help the customer with their general inquiry.

Customer Inquiry: {inquiry}

Provide a helpful, friendly response that:
1. Addresses their question or feedback
2. Provides relevant information
3. Directs them to appropriate resources if needed

Keep your response concise (3-4 sentences)."""
)
general_chain = general_prompt | llm | StrOutputParser()


# ============================================================
# STEP 4: Route and Execute Function
# ============================================================

def route_and_respond(inquiry: str) -> dict:
    """
    Routes the inquiry to the appropriate handler and returns the response.

    Args:
        inquiry: The customer inquiry text

    Returns:
        dict with routing decision and response
    """
    # Step 1: Classify the inquiry
    route_decision = router_chain.invoke({"inquiry": inquiry})

    # Step 2: Route to the appropriate handler
    handlers = {
        "technical_support": technical_support_chain,
        "billing": billing_chain,
        "product_info": product_info_chain,
        "general": general_chain
    }

    handler = handlers[route_decision.category]
    response = handler.invoke({"inquiry": inquiry})

    return {
        "category": route_decision.category,
        "confidence": route_decision.confidence,
        "reasoning": route_decision.reasoning,
        "response": response
    }


# ============================================================
# EXAMPLES: Different Types of Customer Inquiries
# ============================================================

examples = [
    "My app keeps crashing when I try to export data. I'm using version 2.3 on Windows.",
    "I was charged twice for my subscription this month. Can you help me get a refund?",
    "Does your product support integration with Slack and Microsoft Teams?",
    "I just wanted to say thank you for the excellent customer service last week!"
]

print("=" * 80)
print("ROUTING PATTERN DEMONSTRATION")
print("=" * 80)
print()

for i, inquiry in enumerate(examples, 1):
    print(f"{'=' * 80}")
    print(f"EXAMPLE {i}")
    print(f"{'=' * 80}")
    print(f"Customer Inquiry:\n{inquiry}\n")

    result = route_and_respond(inquiry)

    print(f"Routing Decision:")
    print(f"  Category: {result['category']}")
    print(f"  Confidence: {result['confidence']}")
    print(f"  Reasoning: {result['reasoning']}\n")

    print(f"Response:\n{result['response']}\n")
    print()
