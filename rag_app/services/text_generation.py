import json
from transformers import pipeline
from ..utils.logging_config import setup_logging
from ..utils.decorators import timeout_decorator
import logging

logger = logging.getLogger(__name__)
setup_logging()

class HuggingFaceGenerator:
    def __init__(self, model_name="gpt2"):
        self.model_name = model_name
        try:
            self.pipeline = pipeline(
                "text-generation",
                model=model_name,
                device=-1  # Use CPU
            )
            logger.info(f"Model {model_name} loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model {model_name}: {str(e)}")
            raise

    # prevent blocking     
    @timeout_decorator(30)  # 30 seconds timeout
    def generate(self, prompt: str, max_new_tokens: int = 100) -> str:
        try:
            # Generate response
            response = self.pipeline(
                prompt,
                max_new_tokens=max_new_tokens,
                num_return_sequences=1,
                pad_token_id=self.pipeline.tokenizer.eos_token_id,
                do_sample=True,
                temperature=0.7
            )
            
            # Extract and clean the generated text
            generated_text = response[0]['generated_text']
            
            # Remove prompt from the beginning if present
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):].strip()
            
            logger.info(f"Text generated successfully using {self.model_name}")
            return generated_text

        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            raise

def create_text_generator(provider="huggingface", model_name="gpt2"):
    try:
        return HuggingFaceGenerator(model_name)
    except Exception as e:
        error_msg = f"Error creating generator: {str(e)}"
        logger.error(error_msg)
        raise ValueError(error_msg)

def retrieve_information(query):
    try:
        with open("knowledge_base.json", "r") as f:
            knowledge_base = json.load(f)
    except FileNotFoundError:
        logger.warning("knowledge_base.json not found")
        return ["Not found relevant information."]

    relevant_info = []
    query_words = set(query.lower().split())
    
    for item in knowledge_base:
        content_words = set(item["content"].lower().split())
        overlap = len(query_words.intersection(content_words))
        if overlap > 0:
            relevant_info.append(item["content"])
    
    return relevant_info if relevant_info else ["Not found relevant information."]