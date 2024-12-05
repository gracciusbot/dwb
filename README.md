# Projeto Blog

## Visão Geral
Este é uma aplicação de blog baseada em Django que inclui recursos como autenticação de usuários, criação de posts e um feed de posts. O projeto está organizado em dois aplicativos principais: `BlogApp` e `api`.

## Dependências
O projeto depende das seguintes bibliotecas, listadas no arquivo `requirements.txt`:
- Django
- djangorestframework
- psycopg2 (para suporte ao banco de dados PostgreSQL)
- Pillow (para manipulação de imagens)

Para instalar as dependências, execute:
```bash
pip install -r requirements.txt
```

## Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/graccius/dwb.git
   cd blog
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure o banco de dados:
   - Certifique-se de que o PostgreSQL está instalado e em execução.
   - Crie um banco de dados para o projeto.
   - Atualize a configuração `DATABASES` em `Blog/settings.py` com suas credenciais de banco de dados.

4. Aplique as migrações:
   ```bash
   python manage.py migrate
   ```

5. Crie um superusuário (opcional):
   ```bash
   python manage.py createsuperuser
   ```

6. Cole os arquivos estáticos:
   ```bash
   python manage.py collectstatic
   ```

## Uso
1. Execute o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```

2. Abra seu navegador e navegue até `http://127.0.0.1:8000/` para acessar a aplicação de blog.

3. Para acessar o painel administrativo, navegue até `http://127.0.0.1:8000/admin/` e faça login com as credenciais do superusuário criado anteriormente.

4. Para usar a API, navegue até `http://127.0.0.1:8000/api/`.

## Estrutura de Diretórios
- `Blog/`: Contém as configurações e configurações principais do projeto Django.
- `BlogApp/`: Contém a lógica principal do aplicativo, incluindo views, models, forms e templates.
- `api/`: Contém os endpoints e serializadores da API REST.
- `static/`: Contém arquivos estáticos como CSS, JavaScript e arquivos de mídia.
- `templates/`: Contém os templates HTML para o aplicativo.

## Contribuição
Sinta-se à vontade para contribuir para este projeto enviando pull requests ou abrindo issues no repositório do GitHub.

