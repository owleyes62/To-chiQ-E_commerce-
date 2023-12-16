from django.shortcuts import render
from .models import *
from produto.models import Produto

def Home_banner(request):
    banners = Banner.objects.all().order_by('id')
    data    = Produto.objects.filter(is_feat_caracterico = True).order_by('id')
    return render(request, 'parcias/_banners.html',{'data': data,
                                                    'banners': banners
                                                    })