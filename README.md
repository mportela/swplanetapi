# swplanetapi

StawWars API REST de Planetas, que deve retornar a quantidade de filmes do SW que um planeta aparece

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
