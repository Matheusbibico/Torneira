from django.db import models

from clientes.models import Cliente
from produtos.models import Produto


class Pedido(models.Model):
    STATUS_CHOICES = [
        ("novo", "Novo"),
        ("pago", "Pago"),
        ("separacao", "Em separação"),
        ("enviado", "Enviado"),
        ("concluido", "Concluído"),
        ("cancelado", "Cancelado"),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="pedidos")
    produtos = models.ManyToManyField(Produto, through="ItemPedido", related_name="pedidos")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    frete = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="novo")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "pedido"
        verbose_name_plural = "pedidos"

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nome}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    nome_produto = models.CharField(max_length=180)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField()

    class Meta:
        verbose_name = "item do pedido"
        verbose_name_plural = "itens do pedido"

    @property
    def subtotal(self):
        return self.preco * self.quantidade

    def __str__(self):
        return f"{self.quantidade}x {self.nome_produto}"
