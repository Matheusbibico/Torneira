from django.db import models
from django.urls import reverse


class Categoria(models.Model):
    nome = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    imagem = models.ImageField(upload_to="categories/", blank=True, null=True)
    ativa = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse("produtos:categoria", kwargs={"slug": self.slug})


class Produto(models.Model):
    nome = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="produtos")
    descricao_curta = models.CharField(max_length=240)
    descricao_completa = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    preco_promocional = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    acabamento = models.CharField(max_length=100, blank=True)
    material = models.CharField(max_length=100, blank=True)
    cor = models.CharField(max_length=80, blank=True)
    garantia = models.CharField(max_length=80, blank=True)
    estoque = models.PositiveIntegerField(default=0)
    imagem_principal = models.ImageField(upload_to="products/", blank=True, null=True)
    ativo = models.BooleanField(default=True)
    destaque = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-destaque", "-criado_em"]
        verbose_name = "produto"
        verbose_name_plural = "produtos"

    def __str__(self):
        return self.nome

    @property
    def preco_atual(self):
        return self.preco_promocional or self.preco

    @property
    def disponivel(self):
        return self.ativo and self.estoque > 0

    def get_absolute_url(self):
        return reverse("produtos:detalhe", kwargs={"slug": self.slug})


class ProdutoImagem(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="imagens")
    imagem = models.ImageField(upload_to="products/gallery/")
    alt = models.CharField(max_length=160, blank=True)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordem", "id"]
        verbose_name = "imagem extra"
        verbose_name_plural = "imagens extras"

    def __str__(self):
        return f"Imagem de {self.produto.nome}"
