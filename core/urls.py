from django.urls import path
from .views import home, registro, login, logout

urlpatterns = [
    # inicial (localhost:8000/)
    path('', home, name='home'),
    
    # cadastro (localhost:8000/cadastro/)
    path('cadastro/', registro, name='registro'),

    # login (localhost:8000/login/)
    path('login/', login, name='login'),

    # logout (localhost:8000/logout/)
    path('logout/', logout, name='logout'),
]