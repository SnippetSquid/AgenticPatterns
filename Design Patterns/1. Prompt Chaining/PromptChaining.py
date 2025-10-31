"""
Simple Prompt Chaining Example using LangChain

This example demonstrates how to chain multiple prompts together,
where the output of one prompt becomes the input to the next.
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

# Define a Pydantic model for the product name output
class ProductName(BaseModel):
    """Structured product name model"""
    name: str = Field(description="A creative product name")
    reasoning: str = Field(description="Brief explanation of why this name was chosen")

# Define the first prompt: Generate a product name
generate_name_prompt = ChatPromptTemplate.from_template(
    "Generate a creative product name for: {product_description}\n"
    "Provide the product name and explain why this name works well."
)

# Define the second prompt: Create a marketing slogan from the product name
generate_slogan_prompt = ChatPromptTemplate.from_template(
    "Create a catchy marketing slogan for a product called: {product_name}\n"
    "The slogan should be memorable and under 10 words."
)

# Define the third prompt: Write a short product description
generate_description_prompt = ChatPromptTemplate.from_template(
    "Write a 2-sentence product description for '{product_name}' with the slogan: '{slogan}'\n"
    "Make it compelling and highlight key benefits."
)

# Create the chain using the pipe operator (|)
# Chain 1: product_description -> ProductName (structured output)
chain1 = generate_name_prompt | llm.with_structured_output(ProductName)

# Chain 2: product_name -> slogan
chain2 = generate_slogan_prompt | llm | StrOutputParser()

# Chain 3: product_name + slogan -> description
chain3 = generate_description_prompt | llm | StrOutputParser()



# ============================================================
# EXAMPLE: Smart Water Bottle
# ============================================================
print("=" * 60)
print("EXAMPLE: Smart Water Bottle")
print("=" * 60)

product_description = "A water bottle that tracks your hydration and reminds you to drink water"
print(f"Starting with: {product_description}\n")

# Step 1: Generate product name (returns structured ProductName object)
print("Step 1: Generating product name...")
product_name_result = chain1.invoke({"product_description": product_description})
print(f"Product Name: {product_name_result.name}")
print(f"Reasoning: {product_name_result.reasoning}\n")

# Step 2: Generate slogan
print("Step 2: Creating marketing slogan...")
slogan = chain2.invoke({"product_name": product_name_result.name})
print(f"Slogan: {slogan}\n")

# Step 3: Generate full description
print("Step 3: Writing product description...")
description = chain3.invoke({
    "product_name": product_name_result.name,
    "slogan": slogan
})
print(f"Description: {description}\n")



