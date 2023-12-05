from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
import re
from utils.f_perfil import valida_cpf, valida_idade, valida_cep


class Perfil(models.Model):
    # Modelo com o objetivo de registrar usuarios em uma Tabela.
    usuario     = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário') 
    # variavel de um campo de relacionemto(OneToOneField) que define que cada registro /
    # no modelo pode ter no maximo um relacionamento com outro registro em outro modelo.
    idade       = models.PositiveIntegerField()
    data_nasc   = models.DateField()
    # VAriavel de um campo que armazena informações de data.
    cpf         = models.CharField(max_length=11)
    endereco    = models.CharField(max_length=50)
    numero      = models.CharField(max_length=5)
    complemento = models.CharField(max_length=30)
    bairro      = models.CharField(max_length=30)
    cep         = models.CharField(max_length=8)
    cidade      = models.CharField(max_length=30)
    estado      = models.CharField(
        max_length=2,
        default='SP',
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )

    def __str__(self):
        return f'{self.usuario}'

    def clean(self):  # Funçào usada para realixar a validação personalizada nos dados do formulario antes de irem ao banco de dados

        """
        raise ValidationError({
            "":"" # informa msgs especificas se os dados estiverem errados
        })
        """
        error_messages = {} 
        #  Este dicionário é usado para armazenar mensagens de erro que podem ocorrer durante a validação dos dados no método clean

        cpf_enviado = self.cpf or None
        cpf_salvo   = None
        perfil      = Perfil.objects.filter(cpf=cpf_enviado).first()
        
        if self.idade is not None and self.idade <= 17:
            error_messages['idade'] = 'precisa ser maior de idade'

        if self.data_nasc is not None and valida_idade(self.idade) != self.data_nasc.year:
            error_messages['data_nasc'] = 'ano de nascimento não bate com sua idade'
            
        if perfil:
            cpf_salvo = perfil.cpf

            if cpf_salvo is not None and self.pk != perfil.pk:
                error_messages['cpf'] = 'CPF já existe.'

        if not valida_cpf(self.cpf): # Função da pasta utils.f_perfil
            error_messages['cpf'] = 'Digite um CPF válido'

        if valida_cep(self.cep): # Função da pasta utils.f_perfil
            error_messages['cep'] = 'CEP inválido, digite os 8 digitos do CEP.(somente numeros)'

        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
