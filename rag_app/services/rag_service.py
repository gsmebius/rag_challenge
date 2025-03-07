"""
Main service for handling RAG (Retrieval Augmented Generation).
"""

from .rag_handdler import RAGHandler
from ..utils.provider_models import get_model_config, get_available_models
import logging

class RAGService:
    @staticmethod
    def process_query(model_name, query):
        if not query:
            raise ValueError("Query parameter is required")

        logging.info(f"Processing request for model: {model_name}")
        
        # Get model configuration
        model_config = get_model_config(model_name)
        if not model_config:
            available_models = get_available_models()
            raise ValueError(f"Model not supported. Valid options: {available_models}")

        logging.info(f"Model configuration: {model_config}")

        # Create RAG handler with correct provider and model
        rag_handler = RAGHandler(
            model_name=model_config["model"],
            provider=model_config["provider"]
        )
        
        # Process the query
        result = rag_handler.evaluate_rag(query)
        
        # Add used model to the response
        result['model'] = model_name
        
        return result 