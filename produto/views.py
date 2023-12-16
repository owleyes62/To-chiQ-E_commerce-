from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . import models
from perfil.models import Perfil

class ListaProdutos(ListView):
    #classe de visualização baseada em django para exibir uma lista de produtos.
    model = models.Produto 
    template_name = 'produto/lista.html' 
    context_object_name = 'produtos' 
    paginate_by = 3 
    
class DetalheProduto(DetailView):
    #classe de visualização baseada em django para exibir os detalhes de um produto especifico.
    model = models.Produto  
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug' # Especifica o nome do argumento da URL que será usado para recuperar o objeto do modelo

class AdicionarAoCarrinho(View):
    # Classe de visualização no Django baseada em função para adicionar produtos ao carrinho

    def get(self, *args, **kwargs):
        # Método GET para processar a adição de produtos ao carrinho

        # Obtém a URL de referência da solicitação
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
        
        # Obtém o ID da variação do produto da solicitação GET
        variacao_id = self.request.GET.get('vid')

        # Verifica se o ID da variação existe
        if not variacao_id:
            messages.error(
                self.request,
                'Não há esse produto no estoque'
            )
            return redirect(http_referer)

        # Obtém a variação do produto com base no ID
        variacao = get_object_or_404(models.Variacao, id=variacao_id)
        variacao_estoque = variacao.estoque
        produto = variacao.produto

        # Atribui valores às variáveis para facilitar o acesso
        produto_id = produto.id
        produto_nome = produto.name
        variacao_nome = variacao.nome or ''
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.pre_prom
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem

        # Verifica se há imagem e atribui o nome da imagem
        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        # Verifica se o estoque da variação é suficiente
        if variacao.estoque < 1:
            messages.error(
                self.request,
                'Estoque insuficiente'
            )
            return redirect(http_referer)

        # Verifica se a sessão do carrinho existe
        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        # Obtém o carrinho da sessão
        carrinho = self.request.session['carrinho']

        # Verifica se a variação já está no carrinho
        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1

            # Verifica se o estoque é suficiente para a quantidade desejada
            if variacao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x no '
                    f'produto "{produto_nome}". Adicionamos {variacao_estoque}x '
                    f'no seu carrinho.'
                )
                quantidade_carrinho = variacao_estoque

            # Atualiza as informações no carrinho
            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * quantidade_carrinho
        else:
            # Adiciona uma nova entrada ao carrinho
            carrinho[variacao_id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quantitativo': preco_unitario,
                'preco_quantitativo_promocional': preco_unitario_promocional,
                'quantidade': 1,
                'slug': slug,
                'imagem': imagem,
            }

        # Salva a sessão do carrinho
        self.request.session.save()

        # Exibe mensagem de sucesso
        messages.success(
            self.request,
            f'Produto {variacao_nome} adicionado ao seu '
            f'carrinho {carrinho[variacao_id]["quantidade"]}x.'
        )

        # Redireciona de volta à página de referência
        return redirect(http_referer)


class RemoverDoCarrinho(View):
     def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            return redirect(http_referer)

        if variacao_id not in self.request.session['carrinho']:
            return redirect(http_referer)

        carrinho = self.request.session['carrinho'][variacao_id]

        messages.success(
            self.request,
            f'Produto {carrinho["variacao_nome"]} '
            f'removido do seu carrinho.'
        )

        del self.request.session['carrinho'][variacao_id]
        self.request.session.save()
        return redirect(http_referer)

class Carrinho(View):
    def get(self, *args, **kwargs):
        contexto = {
            'carrinho':self.request.session.get('carrinho', {})
        }
        return render(self.request, 'produto/carrinho.html' ,contexto)

class ResumoDaCompra(View):
    def get(self, *args, **kwargs):

        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')


        contexto = {
            'usuario' : self.request.user,
            'carrinho' : self.request.session['carrinho'],
        }
        
        perfil = Perfil.objects.filter(usuario = self.request.user).exists()

        if not perfil:
            messages.error(
                self.request,
                'Usuario sem perfil.'
            )

        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Carrinho vazio.'
            )

        return render(self.request, 'produto/resumodacompra.html', contexto)

class Busca(View):
    pass