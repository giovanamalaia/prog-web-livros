from django.shortcuts import render, redirect
from django.contrib import messages 
from .forms import RegistroForm
from .forms import LoginForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from .models import Livro
from django.contrib.auth.decorators import login_required
from .forms import LivroForm
import json
import urllib.request
from django.core.files.base import ContentFile
 
 
def home(request):
    return render(request, 'core/pages/home.html', {'active_page': 'home'})  # define qual ícone fica "ativo" na sidebar

def registro(request):
    if request.method == 'POST':
        # dados que o usuário digitou no html
        form = RegistroForm(request.POST) 
        
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Conta criada e login realizado com sucesso!')
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
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('home')
    else:
        form = LoginForm(request)

    return render(request, 'core/auth/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    messages.info(request, 'Você saiu da sua conta.')
    return redirect('login_raiz')


def favoritos(request):  
    return render(request, 'core/pages/favoritos.html', {'active_page': 'favoritos'})  


def perfil(request): 
    return render(request, 'core/pages/perfil.html', {'active_page': 'perfil'}) 


def configuracoes(request):  
    return render(request, 'core/pages/configuracoes.html', {'active_page': 'configuracoes'})  


def home(request):
    # pega os 10 últimos livros adicionados 
    latest_books = Livro.objects.filter(disponivel=True).order_by('-data_adicao')[:10]
    
    context = {
        'latest_books': latest_books,
        'active_page': 'home' 
    }
    return render(request, 'core/pages/home.html', context)


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
            
            messages.success(request, 'Livro adicionado com sucesso!')
            return redirect('perfil') 
    else:
        form = LivroForm()

    context = {
        'form': form,
        'active_page': 'adicionar_livro'
    }
    return render(request, 'core/pages/adicionar_livro.html', context)