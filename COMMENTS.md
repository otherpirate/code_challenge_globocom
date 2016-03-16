=====================
## Instalação

#### 1) Banco de dados local/não instalado

#### 2) Banco de dados externo/instalado

=====================
## A solução

#### 1) API First
Resolvi disponibilizar o serviço em forma de API, pois permite que o projeto seja acessado por qualquer device em qualquer ambiente.
Todas as regras de negócio, banco dados e controles estão no server side.


#### 2) WebClient


#### 3) URLs
-  **Adicionar participante**

    POST /candidate/ {id: "murari", name: "Mauro Murari"}

    500 - Erro interno

    409 - id duplicado

    400 - Dados inválidos

    201 - Sucesso {id: "murari", name: "Mauro Murari", active: True}


-  **Remover participante**

    DELETE /candidate/<id>

    500 - Erro interno

    409 - id já removido

    404 - id não existe

    202 - Sucesso

-  **Adicionar paredão, já informando os participantes**

    POST /wall/ {id: "abril_04", candidates: ["murari", "batman"]}

    500 - Erro interno

    409 - id duplicado e/ou existe um paredão ativo

    400 - Dados inválidos

    201 - Sucesso {id: "abril_04", candidates: ["murari", "batman"], active: True}

-  **Finalizar um paredão**

    DELETE /wall/<id>

    500 - Erro interno

    409 - id já removido

    404 - id não existe

    202 - Sucesso

-  **Consultar o paredão que está ativo**

    GET /wall/

    500 - Erro interno

    404 - Não existe paredão ativo

    200 - Sucesso {id: "abril_04", candidates: ["murari", "batman"], active: True}

-  **Consultar o resumo de votação do paredão por candidato**

    GET /wall/<id>/candidate/

    500 - Erro interno

    404 - id não existe

    200 - Sucesso {"batman": 200, "murari": 123}

-  **Consultar o resumo de votação do paredão por hora do dia**

    GET /wall/<id>/hour/

    500 - Erro interno

    404 - id não existe

    200 - Sucesso {"10": 100, "11": 200, "18": 123}

-  **Adicionar um voto**

    POST /vote/ {wall: "abril_04", candidate: "batman"}

    500 - Erro interno

    404 - wall e/ou candidate não existe

    400 - Dados inválidos

    201 - Sucesso


=====================
## Improvements


#### 1) Back-end
**URLs**:
- Autenticação de parceiros conhecidos para metodos de post e delete, para evitar requests não humanos
- Abrir URLs de get/<id> e get/<all> para candidate e wall
- Detalhar as mensagens de erro


#### 2) Web client


#### 3) Tests
**REST**
- Testar os json de cada request

**Mock**
- Criar ambiente mockado de base de dados

**Stress**
- Checar tempo total de execução