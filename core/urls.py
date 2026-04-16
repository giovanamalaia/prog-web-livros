from django.urls import path
from .views import home, registro, login, logout, favoritos, perfil, configuracoes  # importa as páginas da sidebar
 
urlpatterns = [
    # inicial (localhost:8000/)
    path('', home, name='home'),
    
    # cadastro (localhost:8000/cadastro/)
    path('cadastro/', registro, name='registro'),

    # login (localhost:8000/login/)
    path('login/', login, name='login'),

    # logout (localhost:8000/logout/)
    path('logout/', logout, name='logout'),

    # favoritos (localhost:8000/favoritos/)
    path('favoritos/', favoritos, name='favoritos'), 

    # perfil (localhost:8000/perfil/)
    path('perfil/', perfil, name='perfil'), 

    # configurações (localhost:8000/configuracoes/)
    path('configuracoes/', configuracoes, name='configuracoes'), 
]
