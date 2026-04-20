import json
from pathlib import Path
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Livro, Interesse, ESTADO_UF_CHOICES
from django.contrib.auth.forms import AuthenticationForm

DATA_PATH = Path(__file__).resolve().parent / "data" / "ibge_cidades.json"
with DATA_PATH.open(encoding="utf-8") as data_file:
    CIDADES_POR_UF = json.load(data_file)


def choices_cidades(uf):
    cidades = CIDADES_POR_UF.get(uf, {}).get("cidades", [])
    return [('', 'Selecione a cidade')] + [(cidade, cidade) for cidade in cidades]

class RegistroForm(UserCreationForm):
    username = forms.CharField(label='Nome de usuário')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Senha')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirme a senha')
    first_name = forms.CharField(max_length=150, required=False, label='Primeiro nome')
    last_name = forms.CharField(max_length=150, required=False, label='Sobrenome')
    email = forms.EmailField(required=False, label='Email')
    estado = forms.ChoiceField(label='Estado', choices=[('', 'Selecione o estado')] + list(ESTADO_UF_CHOICES))
    cidade = forms.ChoiceField(label='Cidade', choices=[('', 'Selecione o estado primeiro')])

    def __init__(self, *args, estado_selecionado=None, **kwargs):
        super().__init__(*args, **kwargs)
        if estado_selecionado:
            self.fields['cidade'].choices = choices_cidades(estado_selecionado)
            self.fields['cidade'].widget.attrs.pop('disabled', None)
        else:
            self.fields['cidade'].choices = [('', 'Selecione o estado primeiro')]
            self.fields['cidade'].widget.attrs['disabled'] = True


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
        fields = ['titulo', 'autor', 'genero', 'estado', 'capa'] 
        labels = {
            'titulo': 'Título',
            'autor': 'Autor',
            'genero': 'Gênero', 
            'estado': 'Estado',
            'capa': 'Capa',
        }
        widgets = {
            'capa': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    #dono vem do usuário logado e status começa como disponível inicialmente, então não precisa do formulário para isso

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Nome de usuário')
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')
