"""
Prompt templates for different use cases.
"""

class PromptTemplates:
    @staticmethod
    def get_rag_prompt(query: str, context: list) -> str:
        # Format the context
        formatted_context = "\n\n".join([
            f"Fragment {i+1}:\n{ctx.strip()}"
            for i, ctx in enumerate(context)
        ])
        
        return f"""Please provide a precise and direct answer to the following question.
Use ONLY the information provided in the context. If the information is not available in the context,
respond: "I'm sorry, I don't have enough information to answer that question."

Relevant Context:
{formatted_context}

Question: {query}

Specific Instructions:
1. Use ONLY the information from the provided context
2. DO NOT generate information that is not in the context
3. DO NOT invent URLs or external references
4. If there is not enough information, clearly admit it
5. Keep the answer concise but informative

Answer:""" 