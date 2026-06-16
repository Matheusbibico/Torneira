from decimal import Decimal

from produtos.models import Produto


class Carrinho:
    session_key = "carrinho"

    def __init__(self, request):
        self.session = request.session
        self.data = self.session.get(self.session_key, {})

    def adicionar(self, produto, quantidade=1):
        produto_id = str(produto.id)
        quantidade = max(1, int(quantidade))
        atual = self.data.get(produto_id, {"quantidade": 0})
        nova_quantidade = min(produto.estoque, atual["quantidade"] + quantidade)
        self.data[produto_id] = {"quantidade": nova_quantidade}
        self.salvar()

    def atualizar(self, produto, quantidade):
        produto_id = str(produto.id)
        quantidade = int(quantidade)
        if quantidade <= 0:
            self.remover(produto)
            return
        self.data[produto_id] = {"quantidade": min(produto.estoque, quantidade)}
        self.salvar()

    def remover(self, produto):
        self.data.pop(str(produto.id), None)
        self.salvar()

    def limpar(self):
        self.session[self.session_key] = {}
        self.session.modified = True

    def salvar(self):
        self.session[self.session_key] = self.data
        self.session.modified = True

    def itens(self):
        ids = self.data.keys()
        produtos = Produto.objects.filter(id__in=ids, ativo=True)
        produtos_map = {str(produto.id): produto for produto in produtos}

        for produto_id, item in self.data.items():
            produto = produtos_map.get(produto_id)
            if not produto:
                continue
            quantidade = item["quantidade"]
            preco = produto.preco_atual
            yield {
                "produto": produto,
                "quantidade": quantidade,
                "preco": preco,
                "subtotal": preco * quantidade,
            }

    def subtotal(self):
        return sum((item["subtotal"] for item in self.itens()), Decimal("0.00"))

    def total_itens(self):
        return sum(item["quantidade"] for item in self.data.values())

    def __len__(self):
        return self.total_itens()
