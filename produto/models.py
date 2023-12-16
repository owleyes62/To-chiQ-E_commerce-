from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.html import mark_safe
from utils.f_produto import formata_preco
from PIL import Image
import os


class Produto(models.Model):
# Modelo com objetivo de resgistrar produtos da tabela
    name           = models.CharField(max_length = 255) 
    des_curta      = models.TextField(max_length = 255)
    des_longa      = models.TextField()
    imagem         = models.ImageField(upload_to = 'Produto_image/%y/%m/', 
                                       blank = True, null = True)
    # Variavel de um campo que armazenara imagens, em um  diretorio nomeado(upload_to).
    slug           = models.SlugField(unique = True, 
                                      blank = True, null = True  ) # URL ddo produto
    pre_marke      = models.FloatField()
    pre_marke_prom = models.FloatField(default = 0)
    tipo           = models.CharField(default = 'v',max_length = 1,choices =(
                                        ('V', 'Variavel'),('S', 'Simples' ),))
    # Forneçera duas opções(choice) com uma sendo ja pré definida(Default) e com o quantidade especifica(max_length)
    
    def image_tag_path(self): # Define o tamanho da imagem ná área admin 
        return mark_safe('<img src= "%s" width="100" height="80"/>' % (self.imagem.url))
    
    def get_preco_formatado(self):    
        return formata_preco(self.pre_marke) # Função da pasta utils.f_produtos
    get_preco_formatado.short_description = 'preço'

    def get_preco_formatado_promo(self):    
        return formata_preco(self.pre_marke_prom) # Função da pasta utils.f_produtos
    get_preco_formatado_promo.short_description = 'preço promo'


    @staticmethod
    def resize_image(img, new_width=800):
    # Função que realiza a redimensão da imagem escolhida(img) para o produto, definido uma largura padrão(new_width)
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name) # Caminho da imagem
        img_pil       = Image.open(img_full_path) # abre a imagem      
        original_width, original_height = img_pil.size

        if original_width <= new_width:
            # Se a imagem original for menor ou igual a largura definida(new_width) não ouvera alteração
            img_pil.close()    
            return
        
        new_height = round((new_width * original_height) / original_width)
        # Calcula a nova altura da imagem usando regra de 3 
        new_img    = img_pil.resize((new_width, new_height), Image.LANCZOS)
        # raliza a redimensão da imagem por meio de um calculo matematico(LANCZOS) 
        new_img.save(img_full_path, optimize=True, quality=50)
        # Realizando o salvamento(save) da nova imagem encima da antiga.


    
    def save(self, *args, **kwargs):
    # cria slug para o produto a partir do nome se o slug estiver vazio
    # além de redimencionar a imagem do produto 
        
        # verifica se o campo do slug está vazio
        if not self.slug:
            # Cria um slug(slugify) a partir do nome do produto
            slug      = f'{slugify(self.name)}'
            self.slug = slug

        super().save(*args, **kwargs) # Salva o slug criado na base de dados

        max_image_size = 800 # Define o tamanho máximo da imagem

        # Redimendiona a imagem se existir
        if self.imagem:
            self.resize_image(self.imagem, max_image_size)

    def __str__(self): # mostra o nome do produto na área admin
        return self.name

class Variacao(models.Model):
    # Modelo com o objetivo de registrar varações do mesmo produto, 
    # esta ligada diretamente ao modelo produto.
    produto  = models.ForeignKey(Produto, on_delete=models.CASCADE)
    # Chave estrangeira(ForeignKey) relacionada ao modelo produto(produto).
    nome     = models.CharField(max_length=50, blank=True, null=True)
    preco    = models.FloatField()
    pre_prom = models.FloatField(default=0)
    estoque  = models.PositiveIntegerField(default=1)
    # Sempre tera que aver  pelomenos 1 produto(deafault) 

    def __str__(self):
        return self.nome or self.produto.nome
    
    def get_v_preco_formatado(self):    
        return formata_preco(self.preco) # Função da pasta utils.f_produtos
    get_v_preco_formatado.short_description = 'preço'

    def get_v_preco_formatado_promo(self):    
        return formata_preco(self.pre_prom) # Função da pasta utils.f_produtos
    get_v_preco_formatado_promo.short_description = 'preço promo'

    class Meta:
        # realisa a mundaça do nome da classe dentro da area de admin
        verbose_name        = 'Variação'
        verbose_name_plural = 'Variações'