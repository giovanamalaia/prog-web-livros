from django.contrib import admin
from .models import Perfil, Livro, Interesse

class LivroAdmin(admin.ModelAdmin):
    readonly_fields = ('data_adicao',)
    list_display = ('titulo', 'autor', 'dono', 'status', 'data_adicao')
    # barra de pesquisa por título e autor
    search_fields = ('titulo', 'autor')

admin.site.register(Perfil)
admin.site.register(Livro, LivroAdmin)
admin.site.register(Interesse)