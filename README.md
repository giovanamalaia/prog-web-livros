# prog-web-livros

Projeto inicial em Django para um sistema de troca de livros.

## O que foi feito ate agora

Este projeto ja esta com:

- ambiente virtual criado
- Django instalado
- migracoes iniciais aplicadas
- banco SQLite criado
- acesso ao painel `/admin`
- superusuario criado

## Passo a passo para configurar o projeto

### 1. Entrar na pasta do projeto

### 2. Criar o ambiente virtual
python3 -m venv venv

### 3. Ativar o ambiente virtual
source venv/bin/activate

### 4. Instalar o Django
pip install django

### 5. Aplicar as migracoes iniciais
python manage.py migrate

### 6. Criar o superuser
python manage.py createsuperuser

### 7. Rodar o servidor
python manage.py runserver

Por padrao, o projeto vai abrir em:
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### 8. Acessar o admin
Com o servidor rodando, abrir no navegador:

[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
(Fazer login com o superusuario criado no passo anterior)>

