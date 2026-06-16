from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Categoria, Produto


def _produtos_filtrados(request):
    produtos = Produto.objects.filter(ativo=True).select_related("categoria")
    busca = request.GET.get("q", "").strip()
    categoria_slug = request.GET.get("categoria", "").strip()
    cor = request.GET.get("cor", "").strip()
    acabamento = request.GET.get("acabamento", "").strip()
    preco_max = request.GET.get("preco_max", "").strip()

    if busca:
        produtos = produtos.filter(
            Q(nome__icontains=busca)
            | Q(descricao_curta__icontains=busca)
            | Q(descricao_completa__icontains=busca)
        )
    if categoria_slug:
        produtos = produtos.filter(categoria__slug=categoria_slug)
    if cor:
        produtos = produtos.filter(cor__iexact=cor)
    if acabamento:
        produtos = produtos.filter(acabamento__iexact=acabamento)
    if preco_max:
        produtos = produtos.filter(preco__lte=preco_max)

    return produtos


def lista_produtos(request):
    produtos = _produtos_filtrados(request)
    categorias = Categoria.objects.filter(ativa=True)
    return render(
        request,
        "produtos/lista.html",
        {
            "produtos": produtos,
            "categorias": categorias,
            "seo_title": "Produtos | Aureum Metais",
            "seo_description": "Torneiras e metais sanitários premium com filtros por categoria, cor, acabamento e preço.",
        },
    )


def categoria(request, slug):
    categoria_obj = get_object_or_404(Categoria, slug=slug, ativa=True)
    produtos = _produtos_filtrados(request).filter(categoria=categoria_obj)
    return render(
        request,
        "produtos/categoria.html",
        {
            "categoria": categoria_obj,
            "produtos": produtos,
            "categorias": Categoria.objects.filter(ativa=True),
            "seo_title": f"{categoria_obj.nome} | Aureum Metais",
            "seo_description": f"Produtos premium da categoria {categoria_obj.nome}.",
        },
    )


def detalhe_produto(request, slug):
    produto = get_object_or_404(
        Produto.objects.select_related("categoria").prefetch_related("imagens"),
        slug=slug,
        ativo=True,
    )
    relacionados = (
        Produto.objects.filter(ativo=True, categoria=produto.categoria)
        .exclude(id=produto.id)
        .select_related("categoria")[:4]
    )
    return render(
        request,
        "produtos/detalhe.html",
        {
            "produto": produto,
            "relacionados": relacionados,
            "seo_title": f"{produto.nome} | Aureum Metais",
            "seo_description": produto.descricao_curta,
        },
    )
