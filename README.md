# swplanetapi

StawWars API REST de Planetas, que deve retornar a quantidade de filmes do SW que um planeta aparece usando a api https://swapi.co/

## Pré-requisitos
- makefiles (os comandos descritos usam Makefile, funciona no Linux e Mac, mas pode rodar sem)
- Docker
- docker-compose
https://docs.docker.com/compose/install/

obs.: O projeto foi desenvolvido com Python 3.6 + Flask 0.12 + PyMongo 3.6, porém como usa docker, o método recomendado de instalação descrito aqui no passo do "make build" já vai construir a máquina com suas dependências sem ter que instalar nada manualmente. E quando subir o ambiente já vai disponível um MongoDB e a URI de acesso já estará configurada.


## Para rodar a aplicação (depois do Docker e docker-compose instalado)
- Baixar a aplicação para algum lugar local
```
git clone https://github.com/mportela/swplanetapi.git
```

Você deve entrar no diretório clonado para rodar os comandos abaixo:
```
cd swplanetapi
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
  - Para rodar como daemon execute (demora até 1 minuto subindo e preparando cache da swapi.co após executar este comando acompanhe o log com o comando seguinte):
  ```
  make run
  ```
  - no modo daemon para ver o log e quando a app terminou de subir:
  ```
  make weblogs
  ```
  - Para parar os containeres iniciados no modo daemon:
  ```
  make stop
  ```
  - Para rodar no modo 'interativo' (escolher entre este e daemon):
  ```
  docker-compose up
  ```

## Listagem de todos os planetas
- enpoint url:		http://localhost:5000/planet
- method:		GET

## Buscar pelo ID do Planeta
- endpoint url:		http://localhost:5000/planet/[_id]
- method:		GET
- [_id]:		atributo "_id" do Planeta para Buscar

## Buscar pelo NOME do Planeta
- endpoint url:		http://localhost:5000/planet/name/[nome do planeta]
- method:		GET
- [nome do planeta]:	atributo "nome" do Planeta para Busca

## Criar um novo Planeta
- endpoint url:		http://localhost:5000/planet
- method:		POST
- content_type:		application/json
- json data:      formato de exemplo: {"nome": "nome do novo planeta", "terreno": "montanhoso", "clima": "seco"}

## Remover um Planeta
- endopint url:		http://localhost:5000/planet/[_id]
- method:		DELETE
- [_id]:		atributo _id do Planeta para Deletar

## Editar um novo Planeta
- endpoint url:		http://localhost:5000/planet/[_id]
- method:		PUT
- [_id]:		atributo _id do Planeta para Editar
- content_type:		application/json
- json data:      formato de exemplo: {"nome": "nome do novo planeta", "terreno": "montanhoso", "clima": "seco"}



# May the force be with you!
