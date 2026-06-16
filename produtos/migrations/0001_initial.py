from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Categoria",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=120)),
                ("slug", models.SlugField(unique=True)),
                ("imagem", models.ImageField(blank=True, null=True, upload_to="categories/")),
                ("ativa", models.BooleanField(default=True)),
            ],
            options={"verbose_name": "categoria", "verbose_name_plural": "categorias", "ordering": ["nome"]},
        ),
        migrations.CreateModel(
            name="Produto",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=180)),
                ("slug", models.SlugField(unique=True)),
                ("descricao_curta", models.CharField(max_length=240)),
                ("descricao_completa", models.TextField()),
                ("preco", models.DecimalField(decimal_places=2, max_digits=10)),
                ("preco_promocional", models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ("acabamento", models.CharField(blank=True, max_length=100)),
                ("material", models.CharField(blank=True, max_length=100)),
                ("cor", models.CharField(blank=True, max_length=80)),
                ("garantia", models.CharField(blank=True, max_length=80)),
                ("estoque", models.PositiveIntegerField(default=0)),
                ("imagem_principal", models.ImageField(blank=True, null=True, upload_to="products/")),
                ("ativo", models.BooleanField(default=True)),
                ("destaque", models.BooleanField(default=False)),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                ("categoria", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="produtos", to="produtos.categoria")),
            ],
            options={"verbose_name": "produto", "verbose_name_plural": "produtos", "ordering": ["-destaque", "-criado_em"]},
        ),
        migrations.CreateModel(
            name="ProdutoImagem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("imagem", models.ImageField(upload_to="products/gallery/")),
                ("alt", models.CharField(blank=True, max_length=160)),
                ("ordem", models.PositiveIntegerField(default=0)),
                ("produto", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="imagens", to="produtos.produto")),
            ],
            options={"verbose_name": "imagem extra", "verbose_name_plural": "imagens extras", "ordering": ["ordem", "id"]},
        ),
    ]
