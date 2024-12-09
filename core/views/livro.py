from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.models import Livro
from core.serializers import (
    LivroDetailSerializer, 
    LivroListSerializer, 
    LivroSerializer,
    LivroAlterarPrecoSerializer)######################

@action(detail=True, methods=["patch"])
def alterar_preco(self, request, pk=None):
    livro = self.get_object()
    
    
    #################
class LivroViewSet(ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    
    def get_serializer_class(self):
        if self.action == "list":
            return LivroListSerializer
        elif self.action == "retrieve":
            return LivroDetailSerializer
        return LivroSerializer