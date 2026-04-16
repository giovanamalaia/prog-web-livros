from django.shortcuts import render, redirect
from django.contrib import messages 
from .forms import RegistroForm
from .forms import LoginForm
from django.contrib.auth import login as auth_login, logout as auth_logout
 
 
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
