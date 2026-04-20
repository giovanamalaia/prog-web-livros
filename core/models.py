from django.db import models
from django.contrib.auth.models import User

# model perfil 
class Perfil(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil') 
    
    cidade = models.CharField(max_length=100, blank=True, null=True) 
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"
    

# model livro
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
    GENERO_CHOICES = [
        ('ficcao_geral', 'Ficção Geral'),
        ('nao_ficcao_geral', 'Não Ficção Geral'),
        ('fantasia', 'Fantasia'),
        ('ficcao_cientifica', 'Ficção Científica'),
        ('romance', 'Romance'),
        ('misterio_suspense', 'Mistério & Suspense'),
        ('terror', 'Terror'),
        ('aventura', 'Aventura'),
        ('jovem_adulto', 'Jovem Adulto'),
        ('infantil', 'Infantil & Infanto-juvenil'),
        ('hq_manga', 'HQs, Mangás & Graphic Novels'),
        ('biografia', 'Biografia'),
        ('autoajuda', 'Autoajuda'),
        ('academico', 'Acadêmicos'),
        ('historia_politica', 'História & Política'),
        ('religiao', 'Religião & Espiritualidade'),
        ('classica', 'Literatura Clássica'),
        ('contemporanea', 'Literatura Contemporânea'),
        ('drama', 'Drama'),
        ('poesia', 'Poesia'),
        ('teatro', 'Teatro (Peças)'),
        ('outros', 'Outros'),
    ]

    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES)

    genero = models.CharField(max_length=30, choices=GENERO_CHOICES, default='outros')

    capa = models.ImageField(upload_to='capas/', blank=True, null=True)
    disponivel = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel')
    dono = models.ForeignKey(User, on_delete=models.CASCADE, related_name='livros')
    data_adicao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} por {self.autor}"

# model interesse
class Interesse(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aceito', 'Aceito'),
        ('recusado', 'Recusado'),
    ]
    # quem quer o livro, qual livro e quando demonstrou interesse
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interesses')
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='interessados')
    data = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    def __str__(self):
        return f"{self.usuario.username} tem interesse em {self.livro.titulo}"
    

