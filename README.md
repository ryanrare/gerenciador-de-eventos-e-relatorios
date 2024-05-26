# gerenciador-de-eventos-e-relatorios
Tratae-se de uma API REST criada em DRF (django rest framework) que gerencia eventos atraves de CRUD nas apis.
- CRUD de eventos
- CRUD de usuarios
- Cadastro de usuarios nos eventos, como tambem remove lo dos eventos.
- No metodo PUT em eventos, é feita uma notificação para todos os usuarios conectados no socket receber uma notificação de modificação.
- Alem de poder autentificar o usuario.

  ### Como rodar o projeto?
  Irei separar em passo a passo:
   - 1* passo: Clone o projeto.
   - 2* passo: Criei um virtual env com python para evitar alguns problemas (python -m venv venv).
   - 3* passo: Na raiz do projeto, rode o comando pip install -r requirements.txt.
   - 4* passo: Crie um banco com postgres, valide sua conexão em setup.setttings.
   - 5* passo: Rode a migracao com python manage.py migrate.
   - 6* passo: Rode a projeto com python manage.py runserver.
 
  Após isso seu projeto ja deve estar rodando, a documentação foi feita com swagger e voce pode acessar em localhost:8000/swagger.
