from django.apps import AppConfig

class PedidoConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pedido'
    # Nomea a aplicação

"""  
->  default_auto_field = 'django.db.models.BigAutoField'   
sera usado como chave primaria(BigAutoField)
automática para os modelos dentro da sua aplicação.
A Chave primaria definida(BigAutoField) 
usa tipos de dado grande que é apropirado quando você espera ter um grande número de registros
""" 


