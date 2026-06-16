from django.urls import path

from . import views

app_name = "pedidos"

urlpatterns = [
    path("", views.checkout, name="checkout"),
    path("obrigado/<int:pedido_id>/", views.obrigado, name="obrigado"),
]
