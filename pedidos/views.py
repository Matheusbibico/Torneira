from decimal import Decimal

from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from carrinho.cart import Carrinho
from .forms import CheckoutForm
from .models import ItemPedido, Pedido


def checkout(request):
    cart = Carrinho(request)
    itens = list(cart.itens())
    if not itens:
        messages.info(request, "Seu carrinho está vazio.")
        return redirect("carrinho:detalhe")

    subtotal = cart.subtotal()
    frete = Decimal("0.00")
    total = subtotal + frete

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                cliente = form.save()
                pedido = Pedido.objects.create(cliente=cliente, subtotal=subtotal, frete=frete, total=total)
                for item in itens:
                    produto = item["produto"]
                    ItemPedido.objects.create(
                        pedido=pedido,
                        produto=produto,
                        nome_produto=produto.nome,
                        preco=item["preco"],
                        quantidade=item["quantidade"],
                    )
                    produto.estoque = max(0, produto.estoque - item["quantidade"])
                    produto.save(update_fields=["estoque"])
                cart.limpar()
            return redirect("pedidos:obrigado", pedido_id=pedido.id)
    else:
        form = CheckoutForm()

    return render(
        request,
        "pedidos/checkout.html",
        {
            "form": form,
            "itens": itens,
            "subtotal": subtotal,
            "frete": frete,
            "total": total,
            "seo_title": "Checkout | Aureum Metais",
        },
    )


def obrigado(request, pedido_id):
    pedido = get_object_or_404(Pedido.objects.select_related("cliente"), id=pedido_id)
    return render(request, "pedidos/obrigado.html", {"pedido": pedido, "seo_title": "Pedido recebido"})
