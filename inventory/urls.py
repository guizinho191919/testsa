from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("itens/novo/",        views.ItemCreate.as_view(),  name="item_create"),
    path("itens/<int:pk>/editar/", views.ItemUpdate.as_view(),  name="item_update"),
    path("itens/<int:pk>/excluir/", views.ItemDelete.as_view(), name="item_delete"),  # 👈 novo
    path("movimentos/novo/",   views.MovimentacaoCreate.as_view(), name="mov_create"),
]
