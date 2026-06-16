from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cliente",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=160)),
                ("email", models.EmailField(max_length=254)),
                ("telefone", models.CharField(max_length=30)),
                ("cpf", models.CharField(blank=True, max_length=14)),
                ("endereco", models.TextField()),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
            ],
            options={"verbose_name": "cliente", "verbose_name_plural": "clientes", "ordering": ["-criado_em"]},
        ),
    ]
