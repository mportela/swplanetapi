# swplanetapi

StawWars API REST de Planetas, que deve retornar a quantidade de filmes do SW que um planeta aparece

## Pré-requisitos
- makefiles (os comandos descritos usam Makefile, funciona no Linux e Mac, mas pode rodar sem)
- Docker
- docker-compose
https://docs.docker.com/compose/install/

obs.: O projeto foi desenvolvido com Python 3.6 + Flask 0.12 + PyMongo 3.6, porém como usa docker, o método recomendado de instalação descrito aqui no passo do "make build" já vai contruir a máquina com suas dependências sem ter que instalar nada manualmente. E quando subir o ambiente já vai disponível um MondoDB e a URI de acesso já estará configurada.


## Para rodar a aplicação (depois do Docker e docker-compose instalado)
- Baixar a aplicação para algum lugar local
```
git clone https://github.com/mportela/swplanetapi.git
```

- Para preparar o ambiente e criar a imagem Docker:
```
make build
```

- Para rodar os testes unitários da aplicação:
```
make test
```
resultado esperado:
```
............
----------------------------------------------------------------------
Ran 14 tests in 0.240s

OK

```

- Para rodar o servidor da aplicação local:
  - Para rodar como daemon execute:
  ```
  make run
  ```
  - Para rodar 'interativo' execute:
  ```
  docker-compose up
  ```

## Listagem de todos os planetas
- enpoint url:		/planet
- method:		GET

## Buscar pelo ID do Planeta
- endpoint url:		/planet/[_id]
- method:		GET
- [_id]:		atributo "_id" do Planeta para Buscar

## Buscar pelo NOME do Planeta
- endpoint url:		/planet/name/[nome do planeta]
- method:		GET
- [nome do planeta]:	atributo "nome" do Planeta para Busca

## Criar um novo Planeta
- endpoint url:		/planet
- method:		POST
- content_type:		application/json
- json data:      formato de exemplo: {"nome": "nome do novo planeta", "terreno": "montanhoso", "clima": "seco"}

## Remover um Planeta
- endopint url:		/planet/[_id]
- method:		DELETE
- [_id]:		atributo _id do Planeta para Deletar

## Editar um novo Planeta
- endpoint url:		/planet/[_id]
- method:		PUT
- [_id]:		atributo _id do Planeta para Editar
- content_type:		application/json
- json data:      formato de exemplo: {"nome": "nome do novo planeta", "terreno": "montanhoso", "clima": "seco"}


# May the force be with you!
