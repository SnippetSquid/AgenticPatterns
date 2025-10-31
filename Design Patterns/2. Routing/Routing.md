# Routing

## Overview

Routing enables agentic systems to dynamically choose between different actions or handlers based on input characteristics. Instead of following a fixed execution path, a routing system analyzes each input and directs it to the most appropriate specialized handler.

**Example:** A customer service agent receives an inquiry. The routing mechanism first classifies the query (e.g., technical issue, billing question, product information). Based on this classification, it directs the query to a specialized handler: a technical support chain, a billing database lookup, or a product information agent. This is more effective than using a single, one-size-fits-all response system.

This pattern transforms agents from static executors into adaptive systems that can select the optimal processing path for each unique input, improving response quality through specialization.

### Implementation Approaches

The routing mechanism can be implemented in several ways:
- **LLM-based Routing**: The language model itself can be prompted to analyze the input and output a specific identifier or instruction that indicates the next step or destination. For example, a prompt might ask the LLM to "Analyze the following user query and output only the category: 'Order Status', 'Product Info', 'Technical Support', or 'Other'." The agentic system then reads this output and directs the workflow accordingly.
- **Embedding-based Routing**: The input query can be converted into a vector embedding (see RAG, Chapter 14). This embedding is then compared to embeddings representing different routes or capabilities. The query is routed to the route whose embedding is most similar. This is useful for semantic routing, where the decision is based on the meaning of the input rather than just keywords.
- **Rule-based Routing**: This involves using predefined rules or logic (e.g., if-else statements, switch cases) based on keywords, patterns, or structured data extracted from the input. This can be faster and more deterministic than LLM-based routing, but is less flexible for handling nuanced or novel inputs. 
- **Machine Learning Model-Based Routing**: Employs a discriminative model, such as a classifier, that has been specifically trained on labeled data to perform a routing task. While it shares conceptual similarities with embedding-based methods, its key characteristic is the supervised fine-tuning process, which adjusts the model's parameters to create a specialized routing function. This technique is distinct from LLM-based routing because the decision-making component is not a generative model executing a prompt at inference time. Instead, the routing logic is encoded within the fine-tuned model's learned weights. While LLMs may be used in a pre-processing step to generate synthetic data for augmenting the training set, they are not involved in the real-time routing decision itself.


**Benefits:**
- Specialized handling for different request types
- Scalable architecture (easy to add new routes)
- Improved response quality through specialization
- Clear separation of concerns

## How It Works

```
Input � Router LLM (classify) � Route Decision � Specialized Handler � Output
```

## Example

The example implements a customer service routing system:
1. Customer inquiry � Router classifies category
2. Router decision � Routes to specialized handler (technical, billing, product, general)
3. Specialized handler � Generates appropriate response

## Implementation Steps

1. **Define routing categories** - Establish clear, distinct categories for classification
2. **Create router chain** - Build LLM chain that classifies inputs with structured output
3. **Build specialized handlers** - Create separate chains optimized for each category
4. **Implement routing logic** - Map classifications to appropriate handlers and execute

## When to Use

**Use when:**
- Different inputs require different handling strategies
- You need specialized responses for different domains
- System needs to scale to handle diverse request types
- You want to optimize prompts for specific scenarios

**Avoid when:**
- All inputs can be handled uniformly
- Routing categories are unclear or overlapping
- Latency is critical (routing adds one extra LLM call)
- Simple conditional logic would suffice
