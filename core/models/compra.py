from django.db import models

from .user import User
from .livro import Livro

class StatusCompra(models.IntegerChoices):
        CARRINHO = 1, "Carrinho"
        REALIZADO = 2, "Realizado"
        PAGO = 3, "Pago"
        ENTREGUE = 4, "Entregue"
        
class Compra(models.Model):        
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name="compras")
    status = models.IntegerField(choices=StatusCompra.choices, default=StatusCompra.CARRINHO)        
    @property
    def total(self):
            return sum(item.livro.preco * item.quantidade for item in self.itens.all())
    
class ItensCompra(models.Model):
    compra = models.ForeignKey(Compra ,on_delete=models.CASCADE, related_name="itens")
    livro = models.ForeignKey(Livro, on_delete=models.PROTECT, related_name="+")
    quantidade = models.IntegerField(default=1)
    
    def __str__(self):
        return f"({self.id}) {self.livro.titulo}({self.livro.quantidade}) R${self.livro.preco}"
       

