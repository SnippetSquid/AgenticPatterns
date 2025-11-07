# Reflexion

**Paper:** [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/pdf/2303.11366)

## Overview

Reflexion is an advanced agentic pattern that enables language models to learn from their mistakes through **self-reflection combined with persistent memory**. Unlike simple iterative refinement, Reflexion implements trial-and-error learning that persists across multiple episodes, allowing agents to accumulate knowledge and improve performance on future tasks based on past failures.

The key innovation of Reflexion is that it uses the model's own reasoning capabilities to evaluate performance, generate self-critiques, and store these insights in memory for future reference. This creates a feedback loop where the agent becomes progressively better at similar tasks over time, mimicking human-like learning from experience.

## Core Components

### 1. Self-Reflection Mechanism

The agent analyzes its own outputs against task requirements and generates specific, actionable critiques. Rather than generic feedback like "this could be better," Reflexion produces diagnostic reflections that identify specific failure modes:

- What went wrong?
- Why did the approach fail?
- What should be done differently next time?

### 2. Memory Systems (The Key Differentiator)

Reflexion employs two complementary memory systems:

**Episodic Memory:**
- Stores recent trial outcomes with their associated reflections
- Uses a sliding window to keep the N most recent attempts
- Enables short-term tactical adjustments based on immediate past experiences
- Resets or gets pruned as new episodes accumulate

**Long-term Memory:**
- Accumulates distilled insights across multiple episodes
- Creates generalizable principles that persist indefinitely
- Contains high-level strategies and patterns learned from many failures
- Carries forward to completely new task instances

### 3. Trial-and-Error Learning Loop

```
Episode 1: Attempt → Fail → Reflect on failure → Store in memory
Episode 2: Retrieve past reflections → Attempt (informed by memory) → Improve → Store new learnings
Episode 3: Use accumulated knowledge → Attempt → Success
```

This loop continues across different task instances, with the agent building a knowledge base of what works and what doesn't.

## How It Works

1. **Initial Attempt:** The agent attempts to solve a task using its base knowledge and any available context.

2. **Evaluation:** The agent (or an evaluator component) assesses whether the attempt succeeded or failed. This can use:
   - Self-evaluation (model judges its own output)
   - External signals (test cases, user feedback, validation rules)
   - Heuristic checks (format validation, constraint satisfaction)

3. **Reflection Generation:** If the attempt failed, the agent generates a detailed reflection:
   - Analyzes what specific aspects failed
   - Identifies the root cause of the failure
   - Proposes specific improvements for future attempts

4. **Memory Update:**
   - Add the attempt and reflection to episodic memory
   - Extract generalizable insights for long-term memory
   - Prune old episodic memories if the window is full

5. **Next Episode:** When facing a new (or the same) task:
   - Retrieve relevant reflections from both memory systems
   - Incorporate learned insights into the prompt
   - Attempt the task with improved strategy
   - Repeat the cycle

## Key Differences from Other Patterns

### Reflexion vs. Reflection (Pattern #4)

| Aspect | Reflection | Reflexion |
|--------|-----------|-----------|
| **Scope** | Single task improvement | Multi-episode learning |
| **Memory** | Resets each task | Persists across tasks |
| **Goal** | Polish one output | Learn from failures |
| **Use case** | "Make this better" | "Learn to do better" |

### Reflexion vs. Chain-of-Thought

- **Chain-of-Thought:** Single-shot reasoning with step-by-step verbalization
- **Reflexion:** Multiple attempts with explicit failure analysis and memory accumulation

### Reflexion vs. ReAct

- **ReAct:** Action-observation cycles within a single episode (reasoning + acting)
- **Reflexion:** Adds explicit reflection on failures + persistent memory across episodes

## When to Use Reflexion

**Use Reflexion when:**
- Tasks involve repeated similar challenges where learning from failures is valuable
- You want the agent to improve performance across multiple task instances
- Failures provide learning opportunities that can generalize to future tasks
- The cost of multiple attempts is acceptable for improved long-term performance
- Examples: coding challenges, puzzle solving, strategy games, question answering

**Use Simple Reflection (Pattern #4) when:**
- You need to improve a single output through iteration
- No need for learning that persists to other tasks
- Immediate quality improvement is the goal
- Examples: drafting documents, generating creative content, refining analyses

**Avoid Reflexion when:**
- Tasks are completely unique with no pattern reuse
- Immediate results are required (no time for trial-and-error)
- The task has no clear success/failure signals for self-evaluation
- Memory overhead is not justified by performance gains

## Implementation Considerations

### Memory Management

- **Episodic Memory Size:** Typically 3-10 recent episodes (balance between context and noise)
- **Long-term Memory:** Distill key insights to avoid unbounded growth
- **Retrieval Strategy:** Simple recency-based or similarity-based retrieval

### Evaluation Mechanisms

- **Self-evaluation:** Model judges its own output (flexible but potentially unreliable)
- **External validation:** Test cases, rules, or ground truth (reliable but requires setup)
- **Hybrid approach:** Combine self-assessment with objective checks

### Performance Trade-offs

- **Benefits:** Improved performance over time, accumulated expertise, adaptability
- **Costs:** Multiple LLM calls per episode, memory storage, increased latency
- **Sweet spot:** Tasks where learning amortizes across many instances

## Example Scenarios

### Coding Challenges
An agent attempts to solve programming problems. When tests fail, it reflects on the error messages and logic flaws, storing insights about common pitfalls. Over multiple problems, it builds a knowledge base of debugging strategies and edge cases to watch for.

### Question Answering
An agent answers questions and verifies correctness. When wrong, it reflects on why its reasoning failed and what knowledge was missing. Future questions benefit from this accumulated understanding.

### Strategic Planning
An agent plans multi-step solutions to problems. When plans fail execution, it reflects on which assumptions were wrong or which dependencies were missed. Future plans incorporate these learned constraints.

## Advanced Considerations

### Scaling Memory

As episodes accumulate, memory can become unwieldy. Consider:
- Periodic memory consolidation (merge similar insights)
- Relevance-based pruning (remove outdated or rarely-used memories)
- Hierarchical memory (organize insights by topic or task type)

### Multi-Agent Reflexion

Reflexion can be combined with multi-agent patterns:
- Different agents contribute to shared memory
- Specialized reflectors analyze different failure modes
- Collective learning across agent pool

### Hybrid Learning

Combine Reflexion with:
- **Planning patterns:** Reflect on which plans succeeded/failed
- **Tool use:** Learn which tools work best for which tasks
- **RAG systems:** Store reflections in vector databases for semantic retrieval

## Summary

Reflexion transforms language models from one-shot problem solvers into learning agents that improve through experience. By adding self-reflection and persistent memory to the trial-and-error learning loop, agents can accumulate expertise and apply lessons learned from past failures to future challenges. This pattern is particularly powerful for repeated similar tasks where the investment in multiple attempts pays off through improved long-term performance.
