from django.db import models

from django.db import models
from django.contrib.auth.models import User


class Pedido(models.Model):
    # Modelo com o objetivo de registrar pedidos feitos por um usuario
    usuario   = models.ForeignKey(User, on_delete=models.CASCADE)
    preco_t   = models.FloatField() # preco
    qtd_total = models.PositiveIntegerField()
    status    = models.CharField(
        default    = "C",
        max_length = 1,
        choices    =(
            ('A', 'Aprovado'),
            ('C', 'Criado'),
            ('R', 'Reprovado'),
            ('P', 'Pendente'),
            ('E', 'Enviado'),
            ('F', 'Finalizado'),
        )
    )

    def __str__(self):
        return f'Pedido N. {self.pk}'


class ItemPedido(models.Model):
    # Modelo com o objetivo de registrar os itens do pedido, esta ligado diretamente ao modelo Pedido
    pedido      = models.ForeignKey(Pedido, on_delete = models.CASCADE)
    produto     = models.CharField(max_length = 255)
    produto_id  = models.PositiveIntegerField()
    variacao    = models.CharField(max_length = 255)
    variacao_id = models.PositiveIntegerField()
    preco       = models.FloatField()
    prec_promo  = models.FloatField(default = 0)
    quantidade  = models.PositiveIntegerField()
    imagem      = models.CharField(max_length = 2000)

    def __str__(self):
        return f'Item do {self.pedido}'

    class Meta:
        verbose_name        = 'Item do pedido'
        verbose_name_plural = 'Itens do pedido'
