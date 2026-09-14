from django.db import models

class Pesagem(models.Model):

    massa = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )

    frames_analisados = models.PositiveIntegerField(
        default=0
    )

    objetos_rastreados = models.PositiveIntegerField(
        default=0
    )

    data_hora = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"Pesagem #{self.id} - "
            f"{self.massa} kg"
        )


class ItemPesagem(models.Model):

    pesagem = models.ForeignKey(
        Pesagem,
        on_delete=models.CASCADE,
        related_name="itens"
    )

    classe = models.CharField(
        max_length=100
    )

    quantidade = models.PositiveIntegerField()

    confianca_media = models.FloatField(
        null=True,
        blank=True
    )

    razao_votacao = models.FloatField(
        null=True,
        blank=True
    )

    def __str__(self):

        return (
            f"{self.classe} - "
            f"{self.quantidade}"
        )