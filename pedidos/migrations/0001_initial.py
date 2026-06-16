from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("clientes", "0001_initial"),
        ("produtos", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Pedido",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("subtotal", models.DecimalField(decimal_places=2, max_digits=10)),
                ("frete", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("total", models.DecimalField(decimal_places=2, max_digits=10)),
                ("status", models.CharField(choices=[("novo", "Novo"), ("pago", "Pago"), ("separacao", "Em separação"), ("enviado", "Enviado"), ("concluido", "Concluído"), ("cancelado", "Cancelado")], default="novo", max_length=20)),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                ("cliente", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="pedidos", to="clientes.cliente")),
            ],
            options={"verbose_name": "pedido", "verbose_name_plural": "pedidos", "ordering": ["-criado_em"]},
        ),
        migrations.CreateModel(
            name="ItemPedido",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome_produto", models.CharField(max_length=180)),
                ("preco", models.DecimalField(decimal_places=2, max_digits=10)),
                ("quantidade", models.PositiveIntegerField()),
                ("pedido", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="itens", to="pedidos.pedido")),
                ("produto", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="produtos.produto")),
            ],
            options={"verbose_name": "item do pedido", "verbose_name_plural": "itens do pedido"},
        ),
        migrations.AddField(
            model_name="pedido",
            name="produtos",
            field=models.ManyToManyField(related_name="pedidos", through="pedidos.ItemPedido", to="produtos.produto"),
        ),
    ]
