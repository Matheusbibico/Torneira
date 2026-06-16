from django.db import models


class Cliente(models.Model):
    nome = models.CharField(max_length=160)
    email = models.EmailField()
    telefone = models.CharField(max_length=30)
    cpf = models.CharField(max_length=14, blank=True)
    endereco = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "cliente"
        verbose_name_plural = "clientes"

    def __str__(self):
        return self.nome
