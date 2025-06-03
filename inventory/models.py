from django.db import models
from django.core.validators import MinValueValidator

class Item(models.Model):
    nome              = models.CharField(max_length=100)
    codigo_referencia = models.CharField(max_length=30, unique=True)
    local_prateleira  = models.CharField(max_length=30, blank=True)
    quantidade        = models.PositiveIntegerField(default=0)
    estoque_minimo    = models.PositiveIntegerField(default=1,
                                                    validators=[MinValueValidator(1)])
    criado_em         = models.DateTimeField(auto_now_add=True)
    atualizado_em     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} ({self.quantidade})"

    def em_alerta(self):
        return self.quantidade < self.estoque_minimo


class Movimentacao(models.Model):
    ENTRADA = "E"
    SAIDA   = "S"
    TIPOS   = [(ENTRADA, "Entrada"), (SAIDA, "Saída")]

    item          = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="movimentos")
    tipo          = models.CharField(max_length=1, choices=TIPOS)
    quantidade    = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    observacoes   = models.CharField(max_length=200, blank=True)
    criado_em     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]

    def save(self, *args, **kwargs):
        if not self.pk:
            delta = self.quantidade if self.tipo == self.ENTRADA else -self.quantidade
            novo_total = self.item.quantidade + delta
            if novo_total < 0:
                raise ValueError("Saída excede a quantidade em estoque.")
            self.item.quantidade = novo_total
            self.item.save()
        super().save(*args, **kwargs)
