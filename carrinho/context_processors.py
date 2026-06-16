from .cart import Carrinho


def carrinho(request):
    cart = Carrinho(request)
    return {"carrinho": cart, "carrinho_total_itens": len(cart)}
