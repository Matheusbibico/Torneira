from decimal import Decimal

from django.core.management.base import BaseCommand

from produtos.models import Categoria, Produto


class Command(BaseCommand):
    help = "Cria categorias e produtos iniciais para visualizar a loja Aureum."

    def handle(self, *args, **options):
        categorias = {
            "torneiras": "Torneiras",
            "misturadores": "Misturadores",
            "acessorios": "Acessórios",
        }
        categoria_objs = {}
        for slug, nome in categorias.items():
            categoria_objs[slug], _ = Categoria.objects.get_or_create(slug=slug, defaults={"nome": nome})

        produtos = [
            {
                "nome": "Torneira Aurea Monocomando",
                "slug": "torneira-aurea-monocomando",
                "categoria": categoria_objs["torneiras"],
                "descricao_curta": "Design minimalista com bica alta e acabamento dourado escovado.",
                "descricao_completa": "Torneira monocomando premium para lavabos sofisticados, com acionamento suave e construção robusta.",
                "preco": Decimal("1290.00"),
                "preco_promocional": Decimal("1090.00"),
                "acabamento": "Escovado",
                "material": "Latão",
                "cor": "Dourado",
                "garantia": "10 anos",
                "estoque": 12,
                "destaque": True,
            },
            {
                "nome": "Misturador Grafite Duo",
                "slug": "misturador-grafite-duo",
                "categoria": categoria_objs["misturadores"],
                "descricao_curta": "Misturador de mesa em grafite fosco para banheiros contemporâneos.",
                "descricao_completa": "Peça com duas alavancas, acabamento resistente e proporções equilibradas para cubas de apoio.",
                "preco": Decimal("1590.00"),
                "acabamento": "Fosco",
                "material": "Latão",
                "cor": "Grafite",
                "garantia": "10 anos",
                "estoque": 8,
                "destaque": True,
            },
            {
                "nome": "Ducha Higiênica Linea",
                "slug": "ducha-higienica-linea",
                "categoria": categoria_objs["acessorios"],
                "descricao_curta": "Acessório discreto com acabamento branco e metais internos reforçados.",
                "descricao_completa": "Ducha higiênica para compor projetos completos com a mesma linguagem visual da linha Aureum.",
                "preco": Decimal("490.00"),
                "acabamento": "Polido",
                "material": "Aço e latão",
                "cor": "Branco",
                "garantia": "5 anos",
                "estoque": 20,
                "destaque": True,
            },
        ]

        criados = 0
        for dados in produtos:
            _, created = Produto.objects.get_or_create(slug=dados["slug"], defaults=dados)
            criados += int(created)

        self.stdout.write(self.style.SUCCESS(f"Seed concluido. Produtos criados: {criados}"))
