from django.urls import path
from .views import home, registro, login, logout, favoritos, perfil, configuracoes, adicionar_livro, detalhe_livro, editar_livro, excluir_livro, criar_interesse, excluir_interesse, aceitar_interesse, recusar_interesse

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

    path('adicionar-livro/', adicionar_livro, name='adicionar_livro'),

    # Detalhe do Livro
    path('livro/<int:livro_id>/', detalhe_livro, name='detalhe_livro'),

    path('editar-livro/<int:livro_id>/', editar_livro, name='editar_livro'),

    path('excluir-livro/<int:livro_id>/', excluir_livro, name='excluir_livro'),

    path('livro/<int:livro_id>/interesse/', criar_interesse, name='criar_interesse'),

    path('livro/<int:livro_id>/interesse/excluir/', excluir_interesse, name='excluir_interesse'),

    path('interesse/<int:interesse_id>/aceitar/', aceitar_interesse, name='aceitar_interesse'),

    path('interesse/<int:interesse_id>/recusar/', recusar_interesse, name='recusar_interesse'),

]