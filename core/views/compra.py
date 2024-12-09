from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from core.models import Compra
from core.serializers import CompraSerializer, CriarEditarCompraSerializer, ListarCompraSerializer


class CompraViewSet(ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem acessar

    def get_queryset(self):
        usuario = self.request.user
        if usuario.is_anonymous:  # Para garantir que usuários anônimos não causem erros
            return Compra.objects.none()
        if usuario.is_superuser:
            return Compra.objects.all()
        if usuario.groups.filter(name="Administradores"):
            return Compra.objects.all()
        return Compra.objects.filter(usuario=usuario)

    def get_serializer_class(self):
        if self.action == "list":
            return ListarCompraSerializer
        if self.action in ("create", "update", "partial_update"):
            return CriarEditarCompraSerializer
        return CompraSerializer

    # def get_serializer_class(self):
    #     if self.action in ("create", "update"):
    #         return CriarEditarCompraSerializer
    #     return CompraSerializer
