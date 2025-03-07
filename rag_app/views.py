"""
Views for the RAG application.
"""

from django.http import JsonResponse
from .services.rag_service import RAGService
from .utils.provider_models import PROVIDER_MODELS
import logging

def use_rag(request, model):
    if request.method == 'GET':
        try:
            query = request.GET.get('query', '')
            result = RAGService.process_query(model, query)
            return JsonResponse(result, status=200)
            
        except ValueError as e:
            error_msg = str(e)
            logging.error(f"Validation error: {error_msg}")
            return JsonResponse({'error': error_msg}, status=400)
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logging.error(error_msg)
            return JsonResponse({'error': error_msg}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
        
