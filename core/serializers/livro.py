from rest_framework.serializers import (
    DecimalField,
    ModelSerializer,
    Serializer,
    SlugRelatedField,
    ValidationError,
    IntegerField,
)

from core.models import Livro

from uploader.models import Image
from uploader.serializers import ImageSerializer


class LivroSerializer(ModelSerializer):
    capa_attachment_key = SlugRelatedField(
        source="capa", queryset=Image.objects.all(), slug_field="attachment_key", required=False, write_only=True
    )
    capa = ImageSerializer(required=False, read_only=True)

    class Meta:
        model = Livro
        fields = "__all__"


class LivroDetailSerializer(ModelSerializer):
    class Meta:
        model = Livro
        fields = "__all__"
        depth = 1
        capa = ImageSerializer(required=False)


class LivroListSerializer(ModelSerializer):
    class Meta:
        model = Livro
        fields = ("id", "titulo", "preco")


class LivroAlterarPrecoSerializer(Serializer):
    preco = DecimalField(max_digits=10, decimal_places=2)

    def validate_preco(self, value):
        if value <= 0:
            raise ValidationError("O Preço Precisa ser Positivo, Cabeção!")
        return value


class LivroAjustarEstoqueSerializer(Serializer):
    quantidade = IntegerField()

    def validate_quantidade(self, value):
        livro = self.context.get("livro")
        if livro:
            nova_quantidade = livro.quantidade + value
            if nova_quantidade < 0:
                raise ValidationError("Quantidade em estoque não pode ser negativa")
        return value
