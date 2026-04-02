from django.http import HttpResponse

def home(request):
    return HttpResponse("Projeto de troca de livros")