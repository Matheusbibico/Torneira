from django.urls import path

from . import views

app_name = "carrinho"

urlpatterns = [
    path("", views.detalhe, name="detalhe"),
    path("adicionar/<int:produto_id>/", views.adicionar, name="adicionar"),
    path("atualizar/<int:produto_id>/", views.atualizar, name="atualizar"),
    path("remover/<int:produto_id>/", views.remover, name="remover"),
]
