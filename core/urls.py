from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("sobre/", views.pagina_institucional, {"template_name": "core/sobre.html"}, name="sobre"),
    path("contato/", views.pagina_institucional, {"template_name": "core/contato.html"}, name="contato"),
    path("politica-de-trocas/", views.pagina_institucional, {"template_name": "core/trocas.html"}, name="trocas"),
    path("privacidade/", views.pagina_institucional, {"template_name": "core/privacidade.html"}, name="privacidade"),
]
