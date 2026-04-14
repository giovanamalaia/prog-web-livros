from django.urls import path
from .views import home, registro

urlpatterns = [
    # inicial (localhost:8000/)
    path('', home, name='home'),
    
    # cadastro (localhost:8000/cadastro/)
    path('cadastro/', registro, name='registro'),
]