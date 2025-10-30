# Prompt Chaining

## Overview

Prompt chaining breaks complex tasks into sequential steps, where each prompt's output feeds into the next.

**Benefits:**
- Better quality (focused subtasks)
- Easier debugging (inspect intermediate outputs)
- More control (validate/modify between steps)

## How It Works

```
Input → Prompt 1 → LLM → Output 1 → Prompt 2 → LLM → Output 2 → ...
```

## Example

The example chains three prompts:
1. Product description → Product name
2. Product name → Marketing slogan
3. Name + slogan → Full description

## Implementation Steps

1. **Create individual prompts** - Define each step as a separate prompt template
2. **Build chains** - Combine prompt → LLM → output parser using the pipe operator (`|`)
3. **Execute sequentially** - Run each chain, passing outputs to the next chain's inputs

## When to Use

**Use when:**
- Tasks can be broken into logical steps
- You need to validate outputs between steps
- Different steps need different prompting strategies

**Avoid when:**
- Task is simple and single-step
- Latency is critical (chains = multiple API calls)
