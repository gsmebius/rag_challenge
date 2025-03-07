from .text_generation import create_text_generator, retrieve_information
from .evaluation import evaluate_response_quality
from ..utils.logging_config import setup_logging

setup_logging()

class RAGHandler:

    def __init__(self, model_name, provider="huggingface"):
        self.text_generator = create_text_generator(provider=provider, model_name=model_name)

    def evaluate_rag(self, query):

        # Retrieve relevant context
        context = retrieve_information(query)
        
        # Create prompt with context
        prompt = f"Context: {' '.join(context)}\nQuestion: {query}\nAnswer:"
        
        # Generate response
        response = self.text_generator.generate(prompt)
        
        # Clean up response by removing prompt and extra text
        response = response.replace(prompt, "").strip()
        response = response.split("Question:")[0].split("Answer:")[-1].strip()
        
        # Evaluate response quality
        evaluation = evaluate_response_quality(query, response, context)
        
        # Return complete results
        return {
            "query": query,
            "context": context,
            "response": response,
            "model": self.text_generator.model_name,
            "evaluation": evaluation,
        }