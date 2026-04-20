from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import RegistroForm
from .forms import LoginForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from .models import Livro, Interesse, Perfil
from django.contrib.auth.decorators import login_required
from .forms import LivroForm
from django.urls import reverse
from urllib.parse import urlparse
import json
import urllib.request
from django.core.files.base import ContentFile
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import translation
from django.utils.translation import gettext as _

@login_required(login_url='login_raiz')
def home(request):
    livros_disponiveis = Livro.objects.filter(disponivel=True)

    if request.user.is_authenticated:
        livros_disponiveis = livros_disponiveis.exclude(dono=request.user)

    # pesquisa
    q = request.GET.get('q', '').strip()
    if q:
        termos = [termo for termo in q.split() if termo]
        for termo in termos:
            livros_disponiveis = livros_disponiveis.filter(
                Q(titulo__istartswith=termo)
                | Q(titulo__icontains=f" {termo}")
                | Q(autor__istartswith=termo)
                | Q(autor__icontains=f" {termo}")
            )
        latest_books = livros_disponiveis.order_by('-data_adicao')  # sem limitar quando pesquisa
    else:
        latest_books = livros_disponiveis.order_by('-data_adicao')[:20]

    # generos
    livros_por_genero = []
    
    for slug_genero, nome_bonito in Livro.GENERO_CHOICES:
        livros_do_genero = livros_disponiveis.filter(genero=slug_genero).order_by('-data_adicao')
        
        # so entra se tiver livros no genero
        if livros_do_genero.exists():
            livros_por_genero.append({
                'titulo_secao': nome_bonito.upper(),
                'livros': livros_do_genero[:10]
            })

    context = {
        'latest_books': latest_books,
        'livros_por_genero': livros_por_genero, 
        'active_page': 'home',
    }
    return render(request, 'core/pages/home.html', context)

def registro(request):
    if request.method == 'POST':
        estado_selecionado = request.POST.get('estado') or None
        # dados que o usuário digitou no html
        form = RegistroForm(request.POST, estado_selecionado=estado_selecionado) 
        action = request.POST.get('action', 'submit')

        if action == 'refresh_cities':
            return render(request, 'core/auth/cadastro.html', {'form': form})
        
        if form.is_valid():
            user = form.save()
            Perfil.objects.create(
                user=user,
                estado=form.cleaned_data['estado'],
                cidade=form.cleaned_data['cidade'],
            )
            auth_login(request, user)
            messages.success(request, _('Conta criada e login realizado com sucesso!'))
            #redireciona para home
            return redirect('home')
    else:
        form = RegistroForm()
    
    return render(request, 'core/auth/cadastro.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            auth_login(request, form.get_user())
            messages.success(request, _('Login realizado com sucesso!'))
            return redirect('home')
    else:
        form = LoginForm(request)

    return render(request, 'core/auth/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    messages.info(request, _('Você saiu da sua conta.'))
    return redirect('login_raiz')


@require_POST
def trocar_idioma(request):
    idioma = request.POST.get('language')
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'

    idiomas_disponiveis = {codigo for codigo, _ in settings.LANGUAGES}
    if idioma not in idiomas_disponiveis:
        return redirect(next_url)

    translation.activate(idioma)
    response = redirect(next_url)
    if hasattr(request, 'session'):
        request.session['django_language'] = idioma
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, idioma)
    return response


def favoritos(request):  
    return render(request, 'core/pages/favoritos.html', {'active_page': 'favoritos'})  


@login_required(login_url='login_raiz')
def configuracoes(request):
    if request.method == 'POST':
        user = request.user
        
        # oq foi digitado
        novo_username = request.POST.get('username')
        novo_email = request.POST.get('email')
        
        # verifica se o username escolhido ja existe
        if User.objects.filter(username=novo_username).exclude(id=user.id).exists():
            messages.error(request, _('Esse username já está em uso por outra conta.'))
            return redirect('configuracoes')
            
        # verifica se email ja existe
        if User.objects.filter(email=novo_email).exclude(id=user.id).exists():
            messages.error(request, _('Esse e-mail já está cadastrado em outra conta.'))
            return redirect('configuracoes')

        # atualiza 
        user.username = novo_username
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = novo_email
        user.save()

        perfil, criado = Perfil.objects.get_or_create(user=user)
        
        # input da foto
        if 'foto_perfil' in request.FILES:
            perfil.foto_perfil = request.FILES.get('foto_perfil')
            perfil.save()
            
        messages.success(request, _('Configurações salvas com sucesso!'))
        return redirect('configuracoes')

    # acessar a pagina
    return render(request, 'core/pages/configuracoes.html', {'active_page': 'configuracoes'})


@login_required(login_url='login_raiz')
def perfil(request): 
    # filtro os livros onde o dono é o usuário que está logado atualmente
    meus_livros = Livro.objects.filter(dono=request.user).order_by('-data_adicao')
    
    context = {
        'active_page': 'perfil',
        'meus_livros': meus_livros 
    }
    return render(request, 'core/pages/perfil.html', context)


@login_required(login_url='login_raiz')
def adicionar_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST, request.FILES) 
        
        if form.is_valid():
            livro = form.save(commit=False) # salva "em pausa"
            livro.dono = request.user       # define o dono do livro
            livro.save()                    # salva no banco de dados
            
            messages.success(request, _('Livro adicionado com sucesso!'))
            return redirect('perfil') 
    else:
        form = LivroForm()

    context = {
        'form': form,
        'active_page': 'adicionar_livro'
    }
    return render(request, 'core/pages/adicionar_livro.html', context)
    

@login_required(login_url='login_raiz')
def detalhe_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)

    meu_interesse = None
    if request.user != livro.dono:
        meu_interesse = Interesse.objects.filter(usuario=request.user, livro=livro).first()

    back_url = request.META.get('HTTP_REFERER')
    if back_url:
        parsed = urlparse(back_url)
        if (parsed.scheme and parsed.scheme not in ('http', 'https')) or (parsed.netloc and parsed.netloc != request.get_host()):
            back_url = None

    context = {
        'livro': livro,
        'active_page': 'home',
        'meu_interesse': meu_interesse,
        'back_url': back_url or reverse('home'),
    }
    return render(request, 'core/pages/detalhe_livro.html', context)


@login_required(login_url='login_raiz')
@require_POST
def excluir_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id, dono=request.user)
    livro.delete()
    messages.success(request, _('Livro excluído com sucesso!'))
    return redirect('perfil')


@login_required(login_url='login_raiz')
def editar_livro(request, livro_id):
    # busca o livro, mas exige que o dono seja o usuário logado
    livro = get_object_or_404(Livro, id=livro_id, dono=request.user)

    if request.method == 'POST':
        # atualizar o existente
        form = LivroForm(request.POST, request.FILES, instance=livro) 
        if form.is_valid():
            form.save()
            messages.success(request, _('Livro atualizado com sucesso!'))
            return redirect('detalhe_livro', livro_id=livro.id) 
    else:
        # carregar o formulário com os dados do livro existente
        form = LivroForm(instance=livro)

    context = {
        'form': form,
        'active_page': 'perfil',
        'editando': True 
    }
    return render(request, 'core/pages/adicionar_livro.html', context)

@login_required(login_url='login_raiz')
@require_POST
def criar_interesse(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)

    if livro.dono == request.user:
        messages.error(request, _('Você não pode demonstrar interesse no seu próprio livro.'))
        return redirect('detalhe_livro', livro_id=livro.id)

    interesse, criado = Interesse.objects.get_or_create(
        usuario=request.user,
        livro=livro,
        defaults={'status': 'pendente'}
    )

    if criado:
        messages.success(request, _('Interesse registrado!'))
        if livro.dono.email: 
            assunto = _("Boas notícias! Alguém quer seu livro: %(titulo)s") % {'titulo': livro.titulo}
            
            nome_dono = livro.dono.first_name or livro.dono.username
            nome_interessado = request.user.username or request.user.first_name
            
            mensagem = _(
                "Olá %(nome_dono)s,\n\n"
                "O usuário %(nome_interessado)s acabou de demonstrar interesse em trocar o seu livro '%(titulo)s'.\n\n"
                "Acesse a plataforma para aceitar ou recusar a solicitação!\n\n"
                "Abraços,\n"
                "Equipe do Livrô"
            ) % {
                'nome_dono': nome_dono.title(),
                'nome_interessado': nome_interessado,
                'titulo': livro.titulo,
            }
            
            try:
                # dispara email
                send_mail(
                    assunto, 
                    mensagem, 
                    settings.DEFAULT_FROM_EMAIL, 
                    [livro.dono.email],        
                    fail_silently=False         
                )
            except Exception as e:
                print(f"Erro ao tentar enviar email: {e}")

    else:
        messages.info(request, _('Você já demonstrou interesse nesse livro.'))

    return redirect('detalhe_livro', livro_id=livro.id)

@login_required(login_url='login_raiz')
@require_POST
def excluir_interesse(request, livro_id):
    Interesse.objects.filter(usuario=request.user, livro_id=livro_id).delete()
    return redirect('favoritos')


@login_required(login_url='login_raiz')
def favoritos(request):
    interesses = (
        Interesse.objects.filter(usuario=request.user)
        .select_related('livro')
        .order_by('-data')
    )
    interesses_books = [i.livro for i in interesses]

    return render(request, 'core/pages/favoritos.html', {
        'active_page': 'favoritos',
        'interesses_books': interesses_books,
    })

@login_required(login_url='login_raiz')
@require_POST
def aceitar_interesse(request, interesse_id):
    interesse = get_object_or_404(
        Interesse,
        id=interesse_id,
        livro__dono=request.user
    )
    interesse.status = 'aceito'
    interesse.save()

    # disparo email do match
    dono = interesse.livro.dono
    interessado = interesse.usuario
    livro = interesse.livro

    nome_dono = dono.first_name or dono.username
    nome_interessado = interessado.first_name or interessado.username

    # email para o dono
    if dono.email:
        assunto_dono = _("Match! Você aceitou trocar: %(titulo)s") % {'titulo': livro.titulo}
        msg_dono = _(
            "Olá %(nome_dono)s,\n\n"
            "Você acabou de aceitar a solicitação de %(nome_interessado)s para o livro '%(titulo)s'.\n\n"
            "Para combinar a troca (local, horário ou envio), entre em contato diretamente pelo e-mail:\n"
            "📧 %(email)s\n\n"
            "Boas trocas!\n"
            "Equipe do Livrô"
        ) % {
            'nome_dono': nome_dono.title(),
            'nome_interessado': nome_interessado.title(),
            'titulo': livro.titulo,
            'email': interessado.email,
        }

        try:
            send_mail(assunto_dono, msg_dono, settings.DEFAULT_FROM_EMAIL, [dono.email], fail_silently=True)
        except Exception as e:
            print(f"Erro ao enviar e-mail para o dono: {e}")

    # email para o interessado
    if interessado.email:
        assunto_interessado = _("Deu Match! Seu interesse em %(titulo)s foi aceito!") % {'titulo': livro.titulo}
        msg_interessado = _(
            "Olá %(nome_interessado)s,\n\n"
            "Ótimas notícias! O usuário %(nome_dono)s aceitou o seu interesse pelo livro '%(titulo)s'.\n\n"
            "Para combinar os detalhes da troca, mande um e-mail para:\n"
            "📧 %(email)s\n\n"
            "Boas trocas!\n"
            "Equipe do Livrô"
        ) % {
            'nome_interessado': nome_interessado.title(),
            'nome_dono': nome_dono.title(),
            'titulo': livro.titulo,
            'email': dono.email,
        }

        try:
            send_mail(assunto_interessado, msg_interessado, settings.DEFAULT_FROM_EMAIL, [interessado.email], fail_silently=True)
        except Exception as e:
            print(f"Erro ao enviar e-mail para o interessado: {e}")

    messages.success(request, _('Interesse aceito! Os e-mails de contato foram enviados para os dois.'))
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required(login_url='login_raiz')
@require_POST
def recusar_interesse(request, interesse_id):
    interesse = get_object_or_404(
        Interesse,
        id=interesse_id,
        livro__dono=request.user
    )
    interesse.status = 'recusado'
    interesse.save()

    # interesse recusado
    interessado = interesse.usuario
    livro = interesse.livro
    nome_interessado = interessado.first_name or interessado.username

    if interessado.email:
        assunto_interessado = _("Atualização sobre o livro: %(titulo)s") % {'titulo': livro.titulo}
        msg_interessado = _(
            "Olá %(nome_interessado)s,\n\n"
            "Infelizmente, o dono do livro '%(titulo)s' não pôde aceitar a sua solicitação de troca neste momento. "
            "O livro pode já ter sido prometido a outra pessoa.\n\n"
            "Não desanime! Continue explorando a plataforma para encontrar outras opções incríveis.\n\n"
            "Abraços,\n"
            "Equipe do Livrô"
        ) % {
            'nome_interessado': nome_interessado.title(),
            'titulo': livro.titulo,
        }

        try:
            send_mail(assunto_interessado, msg_interessado, settings.DEFAULT_FROM_EMAIL, [interessado.email], fail_silently=True)
        except Exception as e:
            print(f"Erro ao enviar e-mail de recusa: {e}")

    messages.info(request, _('O interesse foi recusado e o usuário foi notificado.'))
    return redirect(request.META.get('HTTP_REFERER', 'home'))
