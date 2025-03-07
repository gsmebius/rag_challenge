"""
Configuration of available models in the application.
"""

PROVIDER_MODELS = {
    "deepseek": {
        "model": "deepseek-ai/deepseek-coder-7b-base-v1.5",
        "provider": "huggingface"
    },
    "gpt2": {
        "model": "gpt2",
        "provider": "huggingface"
    },
}

def get_model_config(model_name):
    """
    Gets the configuration of a model by its name.
    
    Args:
        model_name (str): Name of the model to search for
        
    Returns:
        dict: Model configuration or None if it doesn't exist
    """
    return PROVIDER_MODELS.get(model_name.lower())

def get_available_models():
    """
    Gets the list of available models.
    
    Returns:
        list: List of available model names
    """
    return list(PROVIDER_MODELS.keys()) 