## Como rodar o projeto
```
uvicorn app.main:app --reload
```

## Docker
* Banco de dados utilizado:
```
docker run --name database_postgre -e POSTGRES_PASSWORD=senha -p 5432:5432 -d postgres:14
```

* Servidor Redis:
```
docker run -d -p 6379:6379 -i -t redis:3.2.5-alpine
```
## Dependencias

* Para instalar todas as dependencias do fastapi:
```
pip install fastapi[all]
```

* Para gerar os hash da senha:
```
pip install passlib[bcrypt]
```

* Biblioteca necessária para o Pydantic validar emails:
```
pip install email-validator
```

* Instale a Biblioteca psycopg2 da seguinte maneira:
```
pip install psycopg2-binary
```

* Biblioteca utilizada para validar cpf e pis:
```
pip install validate-docbr
```

* Biblioteca utilizada para validar CEP:
```
pip install pycep-correios
```

* Api utilizada para gerar cpfs e pis válidos:

https://www.4devs.com.br/gerador_de_pis_pasep

* Biblioteca para gerar e verificar tokens JWT:
```
pip install python-jose[cryptography]
```

* Biblioteca necessária para rodar os testes assincronos:
```
pip install trio
```
