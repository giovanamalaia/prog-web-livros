from django.shortcuts import render, redirect
from django.contrib import messages 
from .forms import RegistroForm

def home(request):
    return render(request, 'core/home.html')

def registro(request):
    if request.method == 'POST':
        # dados que o usuário digitou no html
        form = RegistroForm(request.POST) 
        
        if form.is_valid():
            # salva o usuário no bd
            form.save() 
            messages.success(request, 'Sua conta foi criada com sucesso! Faça o login para continuar.')
            # redireciona para login
            return redirect('login')
    else:
        form = RegistroForm()
    
    return render(request, 'core/cadastro.html', {'form': form})