from django.contrib import admin
from . import models

# Aqui sera personalizado a aparencia  de todos os models na área de admin
class VariacaoInline(admin.TabularInline):
    # mostrara o models Variacao dentro da area de produtos no admin
    model = models.Variacao
    extra = 1

class VariacaoAdmin(admin.ModelAdmin):
    # exibira o models Produto na interface princial do admin
    list_display = ['nome',
                    'produto',
                    'get_v_preco_formatado',
                    'get_v_preco_formatado_promo',
                    'estoque'
                    ]

class ProdutoAdmin(admin.ModelAdmin):
    # exibira o models Produto na interface princial do admin
    list_display = ['name', 
                    'get_preco_formatado', 
                    'get_preco_formatado_promo',  
                    'image_tag_path'
                    ]
    inlines = [ 
        VariacaoInline
        # Permite que um modelo(Variacao) seja gerenciado diretamente por outros modelos dentro do admin(Produto)
    ]

# registra os modens no admin
admin.site.register(models.Produto, ProdutoAdmin)
admin.site.register(models.Variacao, VariacaoAdmin)