from rest_framework.serializers import ModelSerializer, CharField

from core.models import Compra

class CompraSerializer(ModelSerializer):
    usuario = CharField(source="usuario.email", read_only="True")
    class Meta:
        model = Compra
        fields = "__all__"