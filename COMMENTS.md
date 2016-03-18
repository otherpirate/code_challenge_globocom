=====================
## Instalação

#### 1) Config
Se necessário, o arquivo para configurar o acesso a base de dados é

    ./restAPI/.env

#### 2) Banco de dados não instalado

    make install

#### 3) Banco de dados já instalado

    make install-without-database

#### 4) Testando

    make test

#### 5) Rodando
    make run

=====================
## A solução

#### 1) Projeto
Cada ano o BBB tem uma nova edição, e precisa **adicionar os parcipantes** da edição.

A cada semana é lançado um **novo paredão** onde devem ser informados os participantes.

Durante o período do paredão as pessoas podem **fazer votos** para cada participante, acessando a página do **paredão atual**.

Ao final da votação, o **paredão será removido** e um **participante será removido** do BBB

Ainda é possível visualizar os dados de cada votação **por hora do dia** e para **cada candidato**


#### 2) WebClient
Pode ser hospedado em qualquer local, basta ajustar a **API_URL** em "./js/bbb_app.js".

A página paredao.html é utilizada para os usuários realizarem seus votos no paredão atual, clicando em quem deve ser eliminado.

Após o voto, o usuário é direcionado para a página votacao.html onde é apresentado o estado votação, para o paredão atual.

As URLs para visualização de dados dos paredões, pode ser vista em resumo_por_participante.html e resumo_por_hora.html.x`

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
## Melhorias


#### 1) Back-end
**URLs**:
- Autenticação de usuário interno para adicionar participantes e paredões, pois isso é resposabilidade apenas do BBB
- Autenticação de parceiros conhecidos para adicionar votos, para evitar requests de maquina
- Abrir URLs de get/id e get/all para participantes e paredões
- Detalhar as mensagens de erro


#### 2) Web client
**Fixes**
- reCAPTCHA is not working

**Interface**
- Votação, melhorias de interface, UX e design
- Responsividade
- Resultados, poder navegar entre os paredões

**Funcionalidades**
- Resultados, comparar candidados/hora
- Resultados, comparar paredões

#### 3) Testes
**REST**
- Testar o content de cada request

**Base de Dados**
- Criar ambiente mockado de base de dados

**Stress**
- Checar tempo total de execução


=====================
## Escolhas


#### 1) API First
Resolvi disponibilizar o serviço em forma de API, pois permite que o projeto seja acessado por qualquer device em qualquer ambiente.

Todas as regras de negócio, banco dados e controles estão no server side.


#### 2) Where is Django?
Não achei necessário utilizar toda a arquitetura de Django para este projeto.

Acredito que API First tem mais valor e expande mais as possibilidades futuras.


#### 3) MongoDB
Optei por usar MongoDB pois é um banco de dados que tenho experiência.

Porém se fosse trocar o banco de dados, basta criar uma nova classe, implementando de DatabaseInterface.

E atualizar o código de Database para usar a nova classe de banco de dados.


#### 4) Web Client
Criei este web client como base para uso da API, eu ainda criaria um APP antes de um site.

Sei que não está nem próximo de aceitável, porém serve para validar a ideia.

Se tivesse mais tempo, usaria alguma ferramenta como bootstrap/skeleton para deixar "bonitão"


#### 5) Google Charts
Utilizei a API de google charts pois é bastante simples e rápida para implementar.


#### 6) Sprites
Estou assumindo que os candidados serão colocados em ordem alfabética da esquerda para a direita no arquivo de sprite.png.


#### 7) Engenharia
Procurei deixar o código o mais abstrato possível.

Busquei manter a coesão das classes e diminuir o acoplamento.


#### 8) make run
Eu validei usando uma VM de Ubuntu 14.04 64bits, limpa.

Aqui está um exemplo de request para iniciar um paredão.

    curl -H "Content-Type: application/json" -X POST -d '{"name": "Macgyver", "id": "code_master"}' http://localhost:5000/candidate/
    curl -H "Content-Type: application/json" -X POST -d '{"name": "Bruce", "id": "bruce_dickson"}' http://localhost:5000/candidate/
    curl -H "Content-Type: application/json" -X POST -d '{"name": "Batman", "id": "bruce_wayne"}' http://localhost:5000/candidate/

    curl -H "Content-Type: application/json" -X POST -d '{"id": "june_7", "candidates": ["code_master", "bruce_dickson"]}' http://localhost:5000/wall/


#### 9) Well...
Sei que a vaga é para Python/Django.

Porém para este projeto, isso não era requisito e na minha opnião um app teria mais valor que um site.

Caso vocês considerem necessário, posso começar um novo projeto, usando Django, sem problemas.