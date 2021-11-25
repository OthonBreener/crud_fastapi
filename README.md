## Sobre o projeto


## Docker

* Banco de dados utilizado:
```sh
docker run --name database_postgre -e POSTGRES_PASSWORD=senha -p 5432:5432 -d postgres:14
```

* Criando a imagem da aplicação apartir do Dockerfile:
```sh
docker build --tag crud-fastapi .
```

## Dependencias

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
