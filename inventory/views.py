from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Item, Movimentacao
from .forms import ItemForm, MovimentacaoForm
from django.utils.text import capfirst
from django.db.models import Sum, F

class DashboardView(ListView):
    model = Item
    template_name = "inventory/dashboard.html"
    context_object_name = "itens"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calculate analytics data
        itens = Item.objects.all()
        context['itens_ok_count'] = itens.filter(quantidade__gt=F('estoque_minimo')).count()
        context['itens_alerta_count'] = itens.filter(quantidade__lte=F('estoque_minimo')).count()
        
        # Calculate total stock value (assuming you have a price field, otherwise set to 0)
        # If you don't have a price field in your Item model, this will be 0
        context['valor_total_estoque'] = 0  # You can implement this when you add price field
        
        return context

class ItemDelete(DeleteView):
    model         = Item
    template_name = "inventory/confirm_delete.html"
    success_url   = reverse_lazy("inventory:dashboard")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Item removido com sucesso.")
        return super().delete(request, *args, **kwargs)


class ItemCreate(CreateView):
    model         = Item
    form_class    = ItemForm
    template_name = "inventory/form.html"
    success_url   = reverse_lazy("inventory:dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Item cadastrado com sucesso.")
        return super().form_valid(form)
    

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = f"Cadastrar {capfirst(self.model._meta.verbose_name)}"
        return ctx


class ItemUpdate(UpdateView):
    model         = Item
    form_class    = ItemForm
    template_name = "inventory/form.html"
    success_url   = reverse_lazy("inventory:dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Item atualizado com sucesso.")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = f"Editar {capfirst(self.model._meta.verbose_name)}"
        return ctx


class MovimentacaoCreate(CreateView):
    model         = Movimentacao
    form_class    = MovimentacaoForm
    template_name = "inventory/form.html"
    success_url   = reverse_lazy("inventory:dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Movimentação registrada.")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = "Registrar Movimentação"
        return ctx
