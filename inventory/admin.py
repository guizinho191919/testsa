from django.contrib import admin
from .models import Item, Movimentacao

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display  = ("nome", "codigo_referencia",
                     "quantidade", "estoque_minimo", "em_alerta")
    search_fields = ("nome", "codigo_referencia")
    list_filter   = ("estoque_minimo",)


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display  = ("item", "tipo", "quantidade", "criado_em")
    list_filter   = ("tipo", "criado_em")
    search_fields = ("item__nome",)
