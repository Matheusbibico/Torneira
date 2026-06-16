# Deploy no Railway

O projeto ja esta preparado para Railway com:

- `railway.json`: roda `collectstatic`, aplica migracoes e inicia Gunicorn
- `Procfile`: comando de start alternativo
- `runtime.txt`: Python 3.11.9 no Railway
- `whitenoise`: entrega arquivos estaticos em producao
- `DATABASE_URL` ou variaveis `PG*`: conexao com PostgreSQL

## Jeito recomendado: GitHub + Railway

1. Crie um repositorio no GitHub e suba esta pasta:

```bash
cd ~/Documents/projetos/torneira
git init
git add .
git commit -m "Projeto Aureum Django"
git branch -M main
git remote add origin URL_DO_SEU_REPOSITORIO
git push -u origin main
```

2. No Railway:

- Crie um novo projeto
- Escolha "Deploy from GitHub repo"
- Selecione o repositorio da Aureum
- Adicione um banco em "Create" > "Database" > "Add PostgreSQL"

3. No servico da aplicacao, abra "Variables" e adicione:

```text
SECRET_KEY=coloque-uma-chave-grande-e-segura
DEBUG=False
ALLOWED_HOSTS=.railway.app
CSRF_TRUSTED_ORIGINS=https://*.railway.app
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

Se o Railway nao mostrar `DATABASE_URL` no Postgres, use estas variaveis:

```text
PGDATABASE=${{Postgres.PGDATABASE}}
PGUSER=${{Postgres.PGUSER}}
PGPASSWORD=${{Postgres.PGPASSWORD}}
PGHOST=${{Postgres.PGHOST}}
PGPORT=${{Postgres.PGPORT}}
```

4. Clique em Deploy.

5. Depois que subir, no servico da aplicacao:

- Abra "Settings"
- Va em "Networking"
- Clique em "Generate Domain"

## Criar usuario admin no Railway

Depois do deploy, abra um shell do Railway ou use a CLI e rode:

```bash
python manage.py createsuperuser
python manage.py seed_aureum
```

## Observacao sobre imagens enviadas pelo admin

Arquivos de `static/` ficam corretos no deploy. Imagens enviadas pelo admin em `media/` precisam de armazenamento persistente para producao, como Railway Volume ou bucket/S3. Para um ecommerce real, essa sera a proxima melhoria importante.
