from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.html import mark_safe
from utils.f_produto import formata_preco
from PIL import Image
import os


class Produto(models.Model):
# classe referente aos modelos de Django(models.Model), que cria uma tabela no banco de dados.
# Modelo com objetivo de resgistrar produtos da tabela
    name           = models.CharField(max_length = 255) 
    # Variavel de um campo que armazenara Strings(CharField) com quantidade predefinida
    des_curta      = models.TextField(max_length = 255)
    # Variavel de um campo que armazenara Stings de quantidade variaveda(TextField)
    des_longa      = models.TextField()
    imagem         = models.ImageField(upload_to = 'Produto_image/%y/%m/', blank = True, null = True)
    # Variavel de um campo que armazenara imagens, em um  diretorio nomeado(upload_to). OBS:se n existir sera criado.
    # onde o campo é opçonal(blank) e nulo(Null)
    slug           = models.SlugField(unique = True, blank = True, null = True  )
    # Variavel de um campo que armazenara um identificador unico para a URL do produto
    pre_marke      = models.FloatField()
    # Variavel de um campo que aceitara somente numeros e os transformara em decimais
    pre_marke_prom = models.FloatField() # (default = 0)
    tipo           = models.CharField(default = 'v',max_length = 1,choices =(
                                        ('V', 'Variavel'),('S', 'Simples' ),))
    # Variavel de um campo que armazenara Strings(CharField) com um quantidade predefinida, 
    # que forneçera duas opções(choice) com uma sendo ja pré definida(Default) e com o quantidade especifica(max_length)
    
    def image_tag_path(self):
        return mark_safe('<img src= "%s" width="100" height="80"/>' % (self.imagem.url))
    
    def get_preco_formatado(self):    
        return formata_preco(self.pre_marke) # Função da pasta utils.f_produtos
    get_preco_formatado.short_description = 'preço'

    def get_preco_formatado_promo(self):    
        return formata_preco(self.pre_marke_prom) # Função da pasta utils.f_produtos
    get_preco_formatado_promo.short_description = 'preço promo'


    @staticmethod
    def resize_image(img, new_width=800):
    # função que realiza a redimensão da imagem escolhida(img) para o produto, definido uma largura padrão(new_width)
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        # Variavel com o Caminho da imagem(MEDIA_ROOT) escolhida(img)
        img_pil       = Image.open(img_full_path)
        # Variavel abriando a imagem(open)        
        original_width, original_height = img_pil.size

        if original_width <= new_width:
            # Se a imagem original for menor ou igual que a largura definida(new_width) não ouvera redimensionamento
            img_pil.close()    
            return
        
        new_height = round((new_width * original_height) / original_width)
        # Variavel com calculo envolvendo regra de 3 para achar a nova altura da imagem
        new_img    = img_pil.resize((new_width, new_height), Image.LANCZOS)
        # Variavel realizando a redimensão da imagem por meio de um calculo matematico(LANCZOS) 
        # para diminuir a iamgem em termo de pixie
        new_img.save(img_full_path, optimize=True, quality=50)
        # Realizando o salvamento(save) da nova imagem encima da antiga, habilitando a otimização(optimize) e definindo um gualidade de 50%


    
    def save(self, *args, **kwargs):
    # Função de salvamento
        
        if not self.slug:
            slug      = f'{slugify(self.name)}'
            self.slug = slug

        super().save(*args, **kwargs)

        max_image_size = 800

        if self.imagem:
            self.resize_image(self.imagem, max_image_size)

    def __str__(self): # mostra o nome do produto na lista de produtos no admin
        return self.name

class Variacao(models.Model):
    # Modelo com o objetivo de registrar varações do mesmo produto, esta ligada diretamente ao modelo produto.
    produto  = models.ForeignKey(Produto, on_delete=models.CASCADE)
    # Variavel definida como uma chave estrangeira(ForeignKey) relacionada ao modelo produto(produto),
    #e se o produto relaconado for deletedo todas as suas variações dessa classe(Variacao) serão excluidas(On_delete)
    nome     = models.CharField(max_length=50, blank=True, null=True)
    preco    = models.FloatField()
    pre_prom = models.FloatField(default=0)
    estoque  = models.PositiveIntegerField(default=1) 
    # Variavel de um campo que armazenara numeros positivos(PositiveIntegerField) representados por produtos,
    # e sempre tera que aver  pelomenos 1 produto(deafault) 

    def __str__(self):
        return self.nome or self.produto.nome

    class Meta:
        # realisa a mundaça do nome da classe dentro da area de admin
        verbose_name        = 'Variação'
        verbose_name_plural = 'Variações'