# Guia de Docker

Este documento descreve como preparar, buildar e rodar o projeto utilizando contêineres Docker.

# Pré-requisitos
- Docker Desktop instalado e rodando.
- Conta ativa no [Docker Hub](https://hub.docker.com/).

# Comandos de Desenvolvimento (Local)

# 1. Criar a imagem localmente
Sempre que fizer alterações no `models.py` ou instalar novas bibliotecas no `requirements.txt`, você deve reconstruir a imagem:
`bash
docker build -t giovanamalaia/livro:v1 .
`

# 2. Rodar o contêiner localmente
Para testar se a imagem está funcionando no seu computador antes de enviar, use o comando:
`bash
docker run -p 8000:8000 giovanamalaia/livro:v1
`
Após inicializar, acesse o site no seu navegador pelo endereço: **http://localhost:8000**

# Publicação (Docker Hub)

Para atualizar a versão final, siga estes passos no terminal:

1. **Login:** `docker login`
2. **Push (Enviar):** `docker push giovanamalaia/livro:v1`
