from django.urls import path
from .views import use_rag

urlpatterns = [
    path("rag/", use_rag, name="use_rag"),
]
