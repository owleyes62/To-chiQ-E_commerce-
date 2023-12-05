
def formata_preco(val): # Formanta a aparencia do valor da variavel(pre_marke)
    return f'R$ {val:.2f}'.replace('.', ',')
    # Define a aperencia do valor crescendo 2 decimais(:.2f) a direita e trocando '.' por ','(('.', ','))

def f_cart_total_qtd(carrinho): # retorna a quatidade total de produtos no carrinho
    return sum([item['quantidade'] for item in carrinho.values()])
    # Compreensão de lista: Itera sobre os valores do dicionário e extrai a chave 'quantidade' de cada item


def f_cart_totals(carrinho): # retorna o valor total de todos os produtos no carrinho
    return sum(                                                       
        [
            item.get('preco_quantitativo_promocional')
            if item.get('preco_quantitativo_promocional')
            else item.get('preco_quantitativo')
            for item
            in carrinho.values()
        ]
    )