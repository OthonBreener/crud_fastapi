## Sobre o projeto

Este projeto consiste em uma REST API (ou crud) feita com o python
utilizando o FastAPI como framework e o postgresql como banco de dados.
Os dados do crud são compostos por um cadastro de usuários com os atributos
nome, cpf, email, pis, senha e o endereço possui País, Estado, cidade, cep,
rua, número e complemento.

O endpoints podem ser consultados na documentação gerada automaticamente
pelo swagger, para isso basta adicionar '/docs' no final da url.
Exemplo:
    http://localhost:8000/docs

Além disso, foi utilizado o jinja2 para renderizar os templates básicos
para um cadastro de usuários.

## Rodando a aplicação com o Docker

* Subir aplicação pelo docker:
```sh
make docker
```

* Criando a imagem da aplicação apartir do Dockerfile:
```sh
docker build --tag crud-fastapi .
```

## Rodando a aplicação sem o docker

Se você quiser rodar o código localmente, sem usar o docker,
siga os passos abaixo:

1. Crie um ambiente virtual, para isso você pode utilizar o virtualenv:

```sh
virtualenv -p python3 venv
```

2. Com o ambiente virtual ativo, instale as dependências:

```sh
pip install -r requirements.txt
```
ou pip3 dependendo das suas configurações.

3. Por fim você pode subir a aplicação com:

```sh
uvicorn app.main:app --reload
```
ou simplismente digitar no terminal:

```sh
make run
```
4. Não se esqueça de subir a imagem docker do banco de dados.

```sh
docker run --name database_postgre -e POSTGRES_PASSWORD=senha -p 5432:5432 -d postgres:14
```

## Observações:

1. Se você estiver rodando o projeto localmente sem o docker use a variável de ambiente para o banco de dados
como:

```sh
postgresql://postgres:senha@localhost:5432/postgres
```

Agora se estiver usando o docker, lembre-se de alterar o localhost por postgres, que é o
nome do banco de dados definido no arquivo docker-compose.yml. Assim, você teria:

```sh
postgresql://postgres:senha@postgres:5432/postgres
```

2. Dentro do arquivo utils contido em app.ext.core, o get_client utilizado no templates
seta a url como "http://localhost:8000", se estiver rodando o docker com a porta 8000
fique atento ao tentar rodar no localhost depois. Podera haver conflitos de rotas, se vc alterar
a rota que uvicorn roda, lembre-se alterar no utils também.
