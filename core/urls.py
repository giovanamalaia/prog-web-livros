from django.urls import path
from .views import home, registro, login, logout, favoritos, perfil, configuracoes, adicionar_livro

urlpatterns = [
    # INICIAL (localhost:8000/)
    path('', login, name='login_raiz'),
    
    # HOME / FEED (localhost:8000/home/)
    path('home/', home, name='home'),
    
    # cadastro (localhost:8000/cadastro/)
    path('cadastro/', registro, name='registro'),

    # login alternativo 
    path('login/', login, name='login'),

    # logout (localhost:8000/logout/)
    path('logout/', logout, name='logout'),

    # favoritos (localhost:8000/favoritos/)
    path('favoritos/', favoritos, name='favoritos'), 

    # perfil (localhost:8000/perfil/)
    path('perfil/', perfil, name='perfil'), 

    # configurações (localhost:8000/configuracoes/)
    path('configuracoes/', configuracoes, name='configuracoes'), 

    # 👇 E aqui tiramos o "views." da frente
    path('adicionar-livro/', adicionar_livro, name='adicionar_livro'),
]