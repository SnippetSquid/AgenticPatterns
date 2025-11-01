# Reflection

## Overview

In complex tasks, an agent's initial output may not be optimal, accurate, or complete. The Reflection pattern addresses this by enabling an agent to evaluate its own work and use that evaluation to improve its performance iteratively. This self-correction mechanism allows agents to refine outputs based on feedback, internal critique, or comparison against desired criteria.

Reflection adds a layer of meta-cognition to agentic systems, transforming them from simple executors into intelligent systems that learn from their outputs and processes. This leads to more reliable, high-quality results, particularly in scenarios where output quality, accuracy, or adherence to complex constraints is critical.

The pattern introduces a feedback loop: the agent doesn't just produce an output—it examines that output (or the process that generated it), identifies potential issues or areas for improvement, and uses those insights to generate a better version or modify future actions.


### Producer-Critic Model

A highly effective implementation separates the reflection process into two distinct logical roles, often called the "Generator-Critic" or "Producer-Reviewer" model:

**Producer Agent**: Focuses entirely on generating content—whether writing, planning, or creating. It takes the initial prompt and produces the first version of the output without concerning itself with critique.

**Critic Agent**: Evaluates the Producer's output with a different persona and distinct instructions (e.g., "You are a senior editor," "You are a meticulous fact-checker"). The Critic analyzes the work against specific criteria such as accuracy, quality, style, or completeness. It finds flaws, suggests improvements, and provides structured feedback.

This separation is powerful because it prevents cognitive bias—the Critic approaches the output with a fresh perspective dedicated entirely to finding errors and improvements. The feedback is then passed back to the Producer, which generates a refined version. This two-agent model creates more robust and unbiased results than single-agent self-reflection.

**Benefits:**
- Prevents cognitive bias through role separation
- Enables specialized evaluation criteria
- Produces more objective and actionable feedback
- Supports iterative improvement cycles
- Scales to handle complex quality requirements

## How It Works

```
Requirements → Producer (Draft 1) → Critic (Feedback) → Producer (Draft 2) → Critic (Feedback) → Final Output
```

The reflection process typically involves these steps:

1. **Execution**: The Producer agent performs a task or generates an initial output
2. **Evaluation/Critique**: The Critic agent analyzes the result, checking for accuracy, coherence, style, completeness, and adherence to requirements
3. **Reflection/Refinement**: Based on the critique, the Producer determines how to improve and generates a refined output
4. **Iteration**: The refined output is evaluated again, and the process repeats until satisfactory quality is achieved or a stopping condition is met

## Example

The example implements a blog post writing system with editorial feedback:
1. **Producer writes initial draft** - Creates blog post based on topic and requirements
2. **Editor provides structured critique** - Evaluates clarity, structure, engagement, and accuracy
3. **Producer refines based on feedback** - Incorporates suggestions to improve the draft
4. **Iteration continues** - Process repeats 2-3 times until quality threshold is met

## Implementation Steps

1. **Define Producer and Critic roles** - Create distinct prompts with different personas and objectives
2. **Implement structured feedback** - Use Pydantic models to ensure consistent, actionable critique
3. **Build refinement loop** - Create iteration logic that passes feedback to Producer for improvement
4. **Set stopping conditions** - Define max iterations or quality thresholds to end the loop
5. **Track improvements** - Display each iteration to visualize quality progression

## When to Use

**Use when:**
- Output quality, accuracy, or polish is critical
- Tasks require adherence to complex constraints or style guides
- Content needs iterative refinement (writing, planning, creative work)
- You can define clear evaluation criteria
- The cost of iteration is justified by quality improvement

**Avoid when:**
- Simple tasks where initial output is sufficient
- Evaluation criteria are unclear or subjective
- Latency is critical (reflection adds multiple LLM calls)
- The domain doesn't benefit from iterative refinement
- Cost of multiple iterations outweighs quality gains

## Advanced Considerations

**Memory and Context**: The effectiveness of reflection is significantly enhanced when the LLM maintains conversational history. This allows the Critic to assess outputs against previous interactions and feedback, enabling cumulative learning where each cycle builds upon the last. Without memory, each reflection is isolated; with memory, it becomes episodic learning that creates context-based wisdom.

**Goal Setting Integration**: Reflection intersects powerfully with goal setting and monitoring. Goals provide the ultimate benchmark for self-evaluation, while monitoring tracks progress. Reflection acts as the corrective engine, using monitored feedback to analyze deviations and adjust strategy. This synergy transforms the agent from a passive executor into a purposeful system that adaptively works toward objectives.

## Tradeoffs

It's important to consider that while the Reflection pattern significantly enhances output quality, it comes with important trade-offs. The iterative process, though powerful, can lead to higher costs and latency, since every refinement loop may require a new LLM call, making it suboptimal for time-sensitive applications. Furthermore, the pattern is memory-intensive; with each iteration, the conversational history expands, including the initial output, critique, and subsequent refinements.