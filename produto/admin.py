from django.contrib import admin
from . import models

#Todo os models criados deveram vim para o admin para q ele possam aparecer na URL admin
# Aqui sera personalizado a aparencia  de todos os models na área de admin
class VariacaoInline(admin.TabularInline):
    # Uma subclasse(VariacaoInline) de TabularInline que exibi registros de modelos relacionados em um formato tabular
    model = models.Variacao
    extra = 1

class ProdutoAdmin(admin.ModelAdmin):
    # Uma subclasse(ProdutoAdmin) de ModelAdmin que fornece a personalização da aparênciae e o comportamento da interface admin
    list_display = ['name', 'get_preco_formatado', 'get_preco_formatado_promo',  'image_tag_path']
    inlines = [ 
        VariacaoInline
        # Permite que um modelo(Variacao) seja gerenciado diretamente por outros modelos dentro do admin(Produto)
    ]

admin.site.register(models.Produto, ProdutoAdmin)
# registra(register) os modelos(Produto, Variação) para que possam ser gerenciado no adminS
admin.site.register(models.Variacao)