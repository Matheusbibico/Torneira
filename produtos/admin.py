from django.contrib import admin

from .models import Categoria, Produto, ProdutoImagem


class ProdutoImagemInline(admin.TabularInline):
    model = ProdutoImagem
    extra = 1


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "slug", "ativa")
    list_filter = ("ativa",)
    prepopulated_fields = {"slug": ("nome",)}
    search_fields = ("nome",)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria", "preco_atual", "estoque", "ativo", "destaque")
    list_filter = ("ativo", "destaque", "categoria", "cor", "acabamento")
    prepopulated_fields = {"slug": ("nome",)}
    search_fields = ("nome", "descricao_curta", "descricao_completa", "cor", "acabamento")
    inlines = [ProdutoImagemInline]
