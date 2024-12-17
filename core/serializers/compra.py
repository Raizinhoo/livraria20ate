from rest_framework.serializers import (
    CharField,
    CurrentUserDefault,
    DateTimeField,
    HiddenField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)

from core.models import Compra, ItensCompra, Livro
from core.serializers import LivroSerializer


class LivroSimplificadoSerializer(ModelSerializer):
    class Meta:
        model = Livro
        fields = ("quantidade", "titulo", "capa", "editora", "categoria", "autores")


class ItensCompraSerializer(ModelSerializer):
    livro = LivroSimplificadoSerializer(read_only=True)
    total = SerializerMethodField()

    def get_total(self, instance):
        return instance.preco * instance.quantidade  #####

    class Meta:
        model = ItensCompra
        fields = ("livro", "quantidade", "total")
        depth = 1


class CriarEditarItensCompraSerializer(ModelSerializer):
    class Meta:
        model = ItensCompra
        fields = ("livro", "quantidade")

    def validate_quantidade(self, quantidade):
        if quantidade <= 0:
            raise ValidationError("Precisa ser Maior que zero")
        return quantidade

    def validate(self, item):
        if item["quantidade"] > item["livro"].quantidade:
            raise ValidationError("QUantidade maior que a quantidade em estoque.")
        return item


class CompraSerializer(ModelSerializer):
    usuario = CharField(source="usuario.email", read_only=True)
    status = CharField(source="get_status_display", read_only=True)
    data = DateTimeField(read_only=True)
    tipo_pagamento = CharField(source="get_tipo_pagamento_display", read_only=True)
    itens = ItensCompraSerializer(many=True, read_only=True)


    class Meta:
        model = Compra
        fields = ("id", "usuario", "status", "data", "total", "tipo_pagamento", "itens")


class CriarEditarCompraSerializer(ModelSerializer):

    class Meta:
        model = Compra
        fields = "__all__"


class ListarItensCompraSerializer(ModelSerializer):
    livro = LivroSerializer()

    class Meta:
        model = ItensCompra
        fields = ("livro", "quantidade")
        depth = 1


class ListarCompraSerializer(ModelSerializer):
    usuario = CharField(source="usuario.id", read_only=True)
    itens = ListarItensCompraSerializer(many=True, read_only=True)
    status_display = CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Compra
        fields = ("id", "usuario", "status", "status_display", "itens")
