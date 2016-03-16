=====================
## Instalação

#### 1) Banco de dados local/não instalado

#### 2) Banco de dados externo/instalado

=====================
## A solução

#### 1) Projeto
Cada ano o BBB tem uma nova edição, e precisa **adicionar os parcipantes** da edição.

A cada semana é lançado um **novo paredão** onde devem ser informados os participantes.

Durante o período do paredão as pessoas podem **fazer votos** para cada participante, acessando a página do **paredão atual**.

Ao final da votação, o **paredão será removido** e um **participante será removido** do BBB

Ainda é possível visualizar os dados de cada votação **por hora do dia** e para **cada candidato**


#### 2) API First
Resolvi disponibilizar o serviço em forma de API, pois permite que o projeto seja acessado por qualquer device em qualquer ambiente.

Todas as regras de negócio, banco dados e controles estão no server side.


#### 3) WebClient


#### 4) URLs
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
## Melhorias


#### 1) Back-end
**URLs**:
- Autenticação de usuário interno para adicionar participantes e paredões, pois isso resposabilidade apenas do BBB
- Autenticação de parceiros conhecidos para adicionar votos, para evitar requests de maquína
- Abrir URLs de get/id e get/all para participantes e paredões
- Detalhar as mensagens de erro


#### 2) Web client


#### 3) Testes
**REST**
- Testar o content de cada request

**Base de Dados**
- Criar ambiente mockado de base de dados

**Stress**
- Checar tempo total de execução