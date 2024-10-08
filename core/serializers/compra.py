from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField

from core.models import Compra, ItensCompra, Livro

class LivroSimplificadoSerializer(ModelSerializer):
    class Meta:
        model = Livro
        fields = ("quantidade", "titulo", "capa", "editora", "categoria", "autor") 

class ItensCompraSerializer(ModelSerializer):
    
    livro = LivroSimplificadoSerializer(read_only=True)
    
    total = SerializerMethodField()
    
    def get_total(self, instance):
        return instance.livro.preco * instance.quantidade #####
    
    class Meta:
        model = ItensCompra
        fields = ("livro", "quantidade", "total") 
        depth = 1
        

class CompraSerializer(ModelSerializer):
    usuario = CharField(source="usuario.email", read_only=True)
    status = CharField(source="get_status_display", read_only=True)
    itens = ItensCompraSerializer(many=True, read_only=True)
    class Meta:
        model = Compra
        fields = ("id", "usuario", "status", "total", "itens") 
        
