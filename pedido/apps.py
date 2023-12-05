from django.apps import AppConfig
# Importa uma classe do modelo django(AppConfig), 
# q é usada para configurar uma aplicá	ao django e fornecer metadados sobre ela

class PedidoConfig(AppConfig):
# Subclasse de configuração personalizada para a aplicação 'pedido'
# que herda todas as funcionalidades da classe base(AppConfig)

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pedido'
    # Nomea a aplicação

"""  
->  default_auto_field = 'django.db.models.BigAutoField'   
Variavel de um campo que sera usado como chave primaria(BigAutoField)
automática para os modelos dentro da sua aplicação.
A Chave primaria definida(BigAutoField) 
usa tipos de dado grande que é apropirado quando vocÊ espera ter um grande número de registros
""" 


