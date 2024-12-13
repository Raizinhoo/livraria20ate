from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from core.models import Livro
from core.serializers import (
    LivroDetailSerializer,
    LivroListSerializer,
    LivroSerializer,
    LivroAlterarPrecoSerializer,
    LivroAjustarEstoqueSerializer,
)


class LivroPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'  
    max_page_size = 100

class LivroViewSet(ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    pagination_class = LivroPagination  

    def get_serializer_class(self):
        if self.action == "list":
            return LivroListSerializer
        elif self.action == "retrieve":
            return LivroDetailSerializer
        return LivroSerializer

    @action(detail=True, methods=["patch"])
    def alterar_preco(self, request, pk=None):
        livro = self.get_object()
        serializer = LivroAlterarPrecoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        livro.preco = serializer.validated_data["preco"]
        livro.save()
        return Response(
            {"detail": f"Preço do Livro '{livro.titulo}' atualizado para {livro.preco}."},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def alterar_quantidade(self, request, pk=None):
        livro = self.get_object()
        serializer = LivroAjustarEstoqueSerializer(data=request.data, context={"livro": livro})
        serializer.is_valid(raise_exception=True)
        quantidade_ajuste = serializer.validated_data["quantidade"]
        livro.quantidade += quantidade_ajuste
        livro.save()
        return Response(
            {"status": "Quantidade mudada com sucesso", "novo_estoque": livro.quantidade},
            status=status.HTTP_200_OK,
        )


class LivroViewSet(ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return LivroListSerializer
        elif self.action == "retrieve":
            return LivroDetailSerializer
        return LivroSerializer

    @action(detail=True, methods=["patch"])
    def alterar_preco(self, request, pk=None):
        livro = self.get_object()

        serializer = LivroAlterarPrecoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        livro.preco = serializer.validated_data["preco"]
        livro.save()

        return Response(
            {"detail": f"Preco do Livro '{livro.titulo}' atualizado para {livro.preco}."}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def alterar_quantidade(self, request, pk=None):
        livro = self.get_object()

        serializer = LivroAjustarEstoqueSerializer(data=request.data, context={"livro": livro})
        serializer.is_valid(raise_exception=True)

        quantidade_ajuste = serializer.validated_data["quantidade"]

        livro.quantidade += quantidade_ajuste
        livro.save()

        return Response(
            {"status": "Quantidade mudada com sucesso", "novo_estoque": livro.quantidade}, status=status.HTTP_200_OK
        )
