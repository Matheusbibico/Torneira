from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from produtos.models import Produto

from .cart import Carrinho


def detalhe(request):
    cart = Carrinho(request)
    return render(
        request,
        "carrinho/detalhe.html",
        {
            "itens": list(cart.itens()),
            "subtotal": cart.subtotal(),
            "seo_title": "Carrinho | Aureum Metais",
        },
    )


@require_POST
def adicionar(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id, ativo=True)
    quantidade = request.POST.get("quantidade", 1)
    Carrinho(request).adicionar(produto, quantidade)
    messages.success(request, f"{produto.nome} foi adicionado ao carrinho.")
    return redirect(request.POST.get("next") or produto.get_absolute_url())


@require_POST
def atualizar(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id, ativo=True)
    quantidade = request.POST.get("quantidade", 1)
    Carrinho(request).atualizar(produto, quantidade)
    return redirect("carrinho:detalhe")


@require_POST
def remover(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id, ativo=True)
    Carrinho(request).remover(produto)
    return redirect("carrinho:detalhe")
