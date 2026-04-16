from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Livro, Interesse
from django.contrib.auth.forms import AuthenticationForm

class RegistroForm(UserCreationForm):
    username = forms.CharField(label='Nome de usuário')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Senha')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirme a senha')
    first_name = forms.CharField(max_length=150, required=False, label='Primeiro nome')
    last_name = forms.CharField(max_length=150, required=False, label='Sobrenome')
    email = forms.EmailField(required=False, label='Email')


    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1', 
            'password2',
        ]


class LivroForm(ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'estado', 'capa', 'isbn'] 
        labels = {
            'titulo': 'Título',
            'autor': 'Autor',
            'estado': 'Estado',
            'capa': 'Capa',
            'isbn': 'ISBN', 
        }

    #dono vem do usuário logado e status começa como disponível inicialmente, então não precisa do formulário para isso

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Nome de usuário')
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')