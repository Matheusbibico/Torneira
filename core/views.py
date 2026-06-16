from django.shortcuts import render

from produtos.models import Categoria, Produto


def home(request):
    produtos = Produto.objects.filter(ativo=True).select_related("categoria")
    destaques = produtos.filter(destaque=True)[:8]
    categorias = Categoria.objects.filter(ativa=True)[:6]
    return render(
        request,
        "core/index.html",
        {
            "produtos": produtos[:12],
            "destaques": destaques,
            "categorias": categorias,
            "seo_title": "Aureum Metais | Torneiras e metais sanitários premium",
            "seo_description": "Ecommerce premium de torneiras e metais sanitários com design elegante, acabamentos nobres e garantia.",
        },
    )


def pagina_institucional(request, template_name):
    return render(request, template_name)
