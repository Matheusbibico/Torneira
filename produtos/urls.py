from django.urls import path

from . import views

app_name = "produtos"

urlpatterns = [
    path("", views.lista_produtos, name="lista"),
    path("categoria/<slug:slug>/", views.categoria, name="categoria"),
    path("<slug:slug>/", views.detalhe_produto, name="detalhe"),
]
