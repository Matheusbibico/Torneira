# Aureum Metais Ecommerce Django

Projeto Django para transformar o prototipo estatico Aureum Metais em um ecommerce real de torneiras e metais sanitarios, preservando a direcao visual premium descrita no prompt.

## O que foi criado

- Apps Django: `core`, `produtos`, `carrinho`, `pedidos`, `clientes`
- Produtos e categorias dinamicos pelo banco
- Admin para produtos, imagens extras, categorias, clientes e pedidos
- Carrinho persistente por session do Django
- Checkout basico com cadastro de cliente
- Pedido salvo no banco com itens e baixa de estoque
- Busca e filtros por categoria, cor, acabamento e preco
- Templates Django com visual grafite, branco e dourado
- Static files organizados em `static/css` e `static/js`
- Media files em `media/products`
- Estrutura pronta para Mercado Pago, Melhor Envio e WhatsApp

## Como rodar

1. Crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instale as dependencias:

```bash
pip install -r requirements.txt
```

3. Crie o arquivo `.env`:

```bash
cp .env.example .env
```

4. Suba o PostgreSQL:

```bash
docker compose up -d
```

5. Rode as migracoes e crie o usuario admin:

```bash
python manage.py migrate
python manage.py seed_aureum
python manage.py createsuperuser
```

6. Inicie o servidor:

```bash
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/` e cadastre produtos em `http://127.0.0.1:8000/admin/`.

## Deploy

Para subir no Railway, use o guia [RAILWAY.md](RAILWAY.md). O projeto ja inclui `railway.json`, `Procfile`, `runtime.txt`, Gunicorn e WhiteNoise.

## Observacao importante

A pasta inicial nao continha os arquivos estaticos originais do prototipo. Por isso, esta versao recria a experiencia visual com base no prompt e mantem a estrutura preparada para encaixar `index.html`, `produto.html`, `css/style.css`, `js/main.js` e `img/` originais quando eles forem adicionados ao projeto.
