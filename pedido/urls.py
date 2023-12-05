from django.urls import path
from . import views

app_name = 'pedido' # Define o namespace  do aplicativo para envitar conflitos de nomeclatura

urlpatterns = [
# varial que armazena as definições padrão de URL para o endpoint
    path('pagar/<int:pk>', views.Pagar.as_view(), name='pagar'),
    path('salvarpedido/', views.SalvarPedido.as_view(), name='salvarpedido'),
    path('lista/', views.Lista.as_view(), name='lista'),
    path('detalhe/<int:pk>', views.Detalhe.as_view(), name='detalhe'),
]


"""
 "pk" Abreviação de chave primaria(Primary Key) é um valor único associado a cada registro no baco de dados

<int:pk>
    Significa que a URL espera um parâmetro chamdo"pk" que deve ser um número inteiro(int). 
    Parametro geralmente usado para identificar de forma exclusiva um objeto específico do BD
"""