# Cadastro de Usuário

Este documento explica como a funcionalidade de registro foi estruturada no Django, servindo de base para as próximas etapas (Login e CRUD de Livros).

# Estrutura do Fluxo

O Django segue um ciclo de vida específico para processar o cadastro:
1. **URL**: Recebe a requisição (ex: `/cadastro/`).
2. **View**: Decide o que fazer (mostrar o formulário ou salvar os dados).
3. **Form**: Valida se as senhas coincidem e se o usuário já existe.
4. **Template**: Renderiza o HTML para o usuário.

# Detalhamento dos Arquivos

# 1. O Formulário (`core/forms.py`)
Utilizamos o `UserCreationForm`, que é uma ferramenta nativa do Django.
- **Vantagem**: Ele já vem com validação de senha forte e verificação de nomes de usuário duplicados.
- **Customização**: Extendemos a classe para incluir campos como `email` e `first_name`.

# 2. A Lógica (`core/views.py`)
A função `registro(request)` trabalha com dois cenários:
- **GET**: O usuário apenas entrou na página. Criamos uma instância vazia do formulário: `form = RegistroForm()`.
- **POST**: O usuário clicou em "Finalizar". Pegamos os dados (`request.POST`), validamos com `is_valid()` e salvamos no banco com `form.save()`.

# 3. A Rota (`core/urls.py`)
Definimos o caminho `path('cadastro/', ...)` e atribuímos um `name='registro'`. 
- **Importante**: O `name` permite que usemos a tag `{% url 'registro' %}` nos templates, evitando caminhos "hardcoded" (fixos) que quebram facilmente.

# 4. O Template (`core/templates/core/auth/cadastro.html`)
- **Herança**: Usa `{% extends 'core/layouts/base.html' %}` para manter o header/footer padrão.
- **Segurança**: O uso da tag `{% csrf_token %}` é obrigatório para evitar ataques em formulários POST.
- **Filtro**: `{{ form.as_p }}` renderiza cada campo do formulário dentro de um parágrafo.
