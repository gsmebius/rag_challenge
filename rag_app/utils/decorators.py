"""
Useful decorators for the RAG project.
"""

import threading
from functools import wraps
import logging

logger = logging.getLogger(__name__)

def timeout_decorator(seconds):

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = []
            error = []
            
            def target():
                try:
                    result.append(func(*args, **kwargs))
                except Exception as e:
                    error.append(e)
                    logger.error(f"Error in function {func.__name__}: {str(e)}")
            
            thread = threading.Thread(target=target)
            thread.daemon = True
            
            logger.debug(f"Starting execution of {func.__name__} with timeout of {seconds}s")
            thread.start()
            thread.join(seconds)
            
            if thread.is_alive():
                error_msg = f"Function {func.__name__} exceeded time limit of {seconds}s"
                logger.warning(error_msg)
                raise TimeoutError(error_msg)
            
            if error:
                raise error[0]
                
            return result[0]
        return wrapper
    return decorator 