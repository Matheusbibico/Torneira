from django.contrib import admin

from .models import ItemPedido, Pedido


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ("produto", "nome_produto", "preco", "quantidade")


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "status", "subtotal", "frete", "total", "criado_em")
    list_filter = ("status", "criado_em")
    search_fields = ("cliente__nome", "cliente__email", "cliente__telefone")
    inlines = [ItemPedidoInline]


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ("pedido", "produto", "nome_produto", "preco", "quantidade")
