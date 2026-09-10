from django.db import models

class Pesagem(models.Model):
    produto = models.CharField(max_length=100)

    massa = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )

    contagem = models.JSONField(
        default=dict
    )

    quantidade_deteccoes = models.PositiveIntegerField()

    data_hora = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.produto} - {self.massa} kg"