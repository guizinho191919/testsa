from django import forms
from .models import Item, Movimentacao

class ItemForm(forms.ModelForm):
    class Meta:
        model  = Item
        fields = ["nome", "codigo_referencia", "local_prateleira",
                  "quantidade", "estoque_minimo"]


class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model  = Movimentacao
        fields = ["item", "tipo", "quantidade", "observacoes"]

    def clean(self):
        cleaned = super().clean()
        item = cleaned.get("item")
        tipo = cleaned.get("tipo")
        qtd  = cleaned.get("quantidade")

        if item and tipo == Movimentacao.SAIDA and qtd and qtd > item.quantidade:
            self.add_error("quantidade", "Saída maior que o estoque disponível.")
        return cleaned
