from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    SerializerMethodField,
    HiddenField,
    CurrentUserDefault,
    ValidationError,
)

from core.models import Compra, ItensCompra, Livro


class LivroSimplificadoSerializer(ModelSerializer):
    class Meta:
        model = Livro
        fields = ("quantidade", "titulo", "capa", "editora", "categoria", "autor")


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
    itens = ItensCompraSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = ("id", "usuario", "status", "total", "itens")


class CriarEditarCompraSerializer(ModelSerializer):
    usuario = HiddenField(default=CurrentUserDefault())  # eu tinha esquecido de comitar o nome
    itens = CriarEditarItensCompraSerializer(many=True)

    class Meta:
        model = Compra
        fields = ("usuario", "itens")

    def create(self, validated_data):
        itens = validated_data.pop("itens")
        compra = Compra.objects.create(**validated_data)
        for item in itens:
            item["preco"] = item["livro"].preco
            ItensCompra.objects.create(compra=compra, **item)
        compra.save()
        return compra

    def update(self, compra, validated_data):
        print("oioioioioiooi")
        itens = validated_data.pop("itens")
        if itens:
            compra.itens.all().delete()
            for item in itens:
                item["preco"] = item["livro"].preco
                ItensCompra.objects.create(compra=compra, **item)
        compra.save()
        return super().update(compra, validated_data)


class ListarItensCompraSerializer(ModelSerializer):
    livro = CharField(source="livro.titulo", read_only=True)

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
