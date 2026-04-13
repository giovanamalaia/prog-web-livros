from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Perfil(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    cidade = models.CharField(max_length=100) 

    def __str__(self):
        return f"{self.user.username} - {self.cidade}"
    

class Livro(models.Model):
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('reservado', 'Reservado'),
        ('trocado', 'Trocado'),
    ]
    ESTADO_CHOICES = [
        ('N', 'Novo'),
        ('SN', 'Semi-novo'),
        ('U', 'Usado'),
    ]

    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES)

    capa = models.ImageField(upload_to='capas/', blank=True, null=True)
    disponivel = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel')
    ISBN = models.CharField(max_length=13, blank=True, null=True)
    dono = models.ForeignKey(User, on_delete=models.CASCADE, related_name='livros')



    def __str__(self):
        return f"{self.titulo} por {self.autor}"
