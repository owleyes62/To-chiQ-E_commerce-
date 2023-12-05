from django.template import Library
from utils.f_produto import formata_preco , f_cart_total_qtd, f_cart_totals

register = Library()

@register.filter
def preco_formatado(val):
    return formata_preco(val)

@register.filter
def cart_total_qtd(carrinho):
    return f_cart_total_qtd(carrinho)


@register.filter
def cart_totals(carrinho):
    return f_cart_totals(carrinho)
    
