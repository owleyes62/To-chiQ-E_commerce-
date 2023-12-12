from django.db import models
from django.utils.html import mark_safe

class Banner(models.Model):
    imagem   = models.ImageField(upload_to= "banner_imgs/") 
    alt_text = models.CharField(max_length = 300)

    def image_tag_path(self):
        return mark_safe('<img src= "%s" width="100"/>' % (self.imagem.url))
    
    class Meta: 
        verbose_name_plural = '1. banners'


    def __str__(self):
        return self.alt_text