# Livrô — Plataforma de Troca de Livros

Projeto Web em **Python + Django**, **HTML** e **CSS** para troca de livros entre usuários.

## Integrantes
- Giovana Malaia Pinheiro - 2312080
- Luana Pinho Bueno Pena - 2312082 

## Links da entrega
- **Site publicado:** [link site]
- **Repositório público:** https://github.com/giovanamalaia/prog-web-livros

## Resumo do pré-projeto 
O site “Livrô” é uma plataforma de troca de livros entre usuários. Cada pessoa cria uma conta, cadastra os
livros que possui e navega pelo catálogo para demonstrar interesse em livros de outras pessoas. O dono do
livro recebe a solicitação e pode aceitar ou recusar, notificando o interessado. O sistema organiza os livros
por gênero e destaca itens próximos ao usuário (mesma cidade/estado), além de permitir edição do perfil,
troca de idioma e gestão completa dos livros e interesses.

## Escopo e funcionalidades
- **Cadastro, login e logout** com autenticação do Django.
- **Perfil do usuário** com foto e localização (estado/cidade).
- **Catálogo de livros** com filtro de pesquisa e seções por gênero.
- **Interesses de troca**: solicitar, cancelar, aceitar e recusar.
- **Notificações** para o dono do livro com ações rápidas.
- **E-mails automáticos** de interesse, aceite e recusa.
- **Internacionalização** (PT‑BR e EN) com alternância de idioma.

## CRUD implementado

**Livro**
- **Create:** cadastrar livro em “Adicionar livro”.
- **Read:** listar no feed e visualizar detalhes.
- **Update:** editar dados e status do livro.
- **Delete:** excluir livro do próprio perfil.

**Interesse**
- **Create:** demonstrar interesse em um livro.
- **Read:** visualizar interesses na área “Favoritos”.
- **Update:** aceitar/recusar (altera status).
- **Delete:** excluir interesse criado pelo usuário.

## Perfis e permissões (gerência de usuário)
- Usuários **não autenticados** só acessam login/cadastro.
- Usuários **autenticados** veem o feed, detalhes e favoritos.
- Apenas o **dono do livro** pode editar/excluir e aceitar/recusar interesses.
- Apenas o **interessado** pode cancelar o próprio interesse.

## Manual do usuário (passo a passo)
1. **Criar conta:** acesse `/cadastro/`, preencha dados e escolha estado/cidade.
2. **Entrar no sistema:** use `/login/` com usuário e senha cadastrados.
3. **Adicionar livros:** em “Perfil” clique em **Adicionar livro** e complete o formulário.
4. **Explorar catálogo:** na **Home**, pesquise por título/autor e veja seções por gênero.
5. **Ver detalhes:** clique em um livro para ver informações completas.
6. **Demonstrar interesse:** no detalhe do livro, clique em **Tenho interesse**.
7. **Gerenciar interesses recebidos:** clique no sino de notificações e aceite/recuse.
8. **Favoritos:** veja seus interesses em `/favoritos/` e cancele se quiser.
9. **Editar perfil:** em `/configuracoes/`, altere dados e foto.
10. **Sair:** use `/logout/`.

## Como rodar localmente

### 1. Criar e ativar o ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Aplicar migrações
```bash
python manage.py migrate
```

### 4. Criar superusuário (opcional, para admin)
```bash
python manage.py createsuperuser
```

### 5. Rodar o servidor
```bash
python manage.py runserver
```

Abra em: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Configuração de e‑mail (recuperação de senha e avisos)
Crie um arquivo `.env` na raiz com:
```
EMAIL_USER=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_de_app
```

> **Observação:** o envio de e‑mails usa SMTP do Gmail. Para funcionar em ambiente local, utilize senha de aplicativo e libere o uso no provedor. Sem essas variáveis, o envio pode falhar.


## O que foi testado e funcionou
- Cadastro e login
- CRUD de livros
- CRUD de interesses
- Troca de idioma
- Recuperação de senha (com e‑mail configurado)

## O que foi testado e não funcionou
- Nada a relatar
