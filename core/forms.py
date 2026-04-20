import json
from pathlib import Path
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _, pgettext_lazy as p_
from .models import Livro, Interesse, ESTADO_UF_CHOICES
from django.contrib.auth.forms import AuthenticationForm

DATA_PATH = Path(__file__).resolve().parent / "data" / "ibge_cidades.json"
with DATA_PATH.open(encoding="utf-8") as data_file:
    CIDADES_POR_UF = json.load(data_file)


def choices_cidades(uf):
    cidades = CIDADES_POR_UF.get(uf, {}).get("cidades", [])
    return [('', _('Selecione a cidade'))] + [(cidade, cidade) for cidade in cidades]

class RegistroForm(UserCreationForm):
    username = forms.CharField(label=_('Nome de usuário'))
    password1 = forms.CharField(widget=forms.PasswordInput, label=_('Senha'))
    password2 = forms.CharField(widget=forms.PasswordInput, label=_('Confirme a senha'))
    first_name = forms.CharField(max_length=150, required=False, label=_('Primeiro nome'))
    last_name = forms.CharField(max_length=150, required=False, label=_('Sobrenome'))
    email = forms.EmailField(required=False, label=_('Email'))
    estado = forms.ChoiceField(label=p_('state', 'Estado'), choices=[('', _('Selecione o estado'))] + list(ESTADO_UF_CHOICES))
    cidade = forms.ChoiceField(label=_('Cidade'), choices=[('', _('Selecione o estado primeiro'))])

    def __init__(self, *args, estado_selecionado=None, **kwargs):
        super().__init__(*args, **kwargs)
        if estado_selecionado:
            self.fields['cidade'].choices = choices_cidades(estado_selecionado)
            self.fields['cidade'].widget.attrs.pop('disabled', None)
        else:
            self.fields['cidade'].choices = [('', _('Selecione o estado primeiro'))]
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
    def __init__(self, *args, include_status=False, **kwargs):
        super().__init__(*args, **kwargs)

        if not include_status:
            self.fields.pop('status', None)

    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'genero', 'estado', 'status', 'capa']
        labels = {
            'titulo': _('Título'),
            'autor': _('Autor'),
            'genero': _('Gênero'), 
            'estado': p_('book_condition', 'Estado'),
            'status': _('Status'),
            'capa': _('Capa'),
        }
        widgets = {
            'capa': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Se o status foi editado, mantemos o boolean "disponivel" coerente.
        if 'status' in self.cleaned_data:
            instance.disponivel = self.cleaned_data['status'] == 'disponivel'

        if commit:
            instance.save()
            self.save_m2m()
        return instance

class LoginForm(AuthenticationForm):
    username = forms.CharField(label=_('Nome de usuário'))
    password = forms.CharField(widget=forms.PasswordInput, label=_('Senha'))
