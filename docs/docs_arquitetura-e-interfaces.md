# Documento de Arquitetura e Interfaces \- DSM Conecta

## 1\. Apresentação

Este documento detalha a arquitetura de software adotada no projeto **DSM Conecta**, focando na organização em camadas, nas responsabilidades de cada módulo, nos fluxos de comunicação e nos benefícios dessa separação para o desacoplamento e a testabilidade da solução multiplataforma.

---

## 2\. Estrutura de Camadas

A arquitetura do sistema é estruturada em quatro camadas principais (`core/`, `data/`, `domain/` e `presentation/`), garantindo que regras de negócio e lógica de domínio fiquem isoladas de detalhes de infraestrutura, frameworks e interfaces de usuário.

src/

├── core/             \# Configurações globais, injeção de dependências, utilitários e tratamento de erros

├── data/             \# Fontes de dados, modelos de persistência, clientes MQTT/HTTP e repositórios concretos

├── domain/           \# Entidades de negócio, objetos de valor, contratos de repositórios (interfaces) e casos de uso

└── presentation/     \# Interfaces de usuário (Flutter multi-plataforma), telas, widgets e gerenciamento de estado

### 2.1. Camada `domain/` 

* **Responsabilidade:** É o coração da aplicação. Contém toda a lógica de negócio pura, regras institucionais, entidades centrais e os casos de uso.  
    
* **Características:** É completamente independente de frameworks externos. Define apenas as interfaces (*contracts*) para que a camada de dados possa implementar a persistência e a comunicação.

### 2.2. Camada `data/` 

* **Responsabilidade:** Responsável pela persistência, comunicação externa e fontes de dados. Implementa os contratos definidos na camada de domínio (`domain/`).  
* **Características:** Contém os clientes de rede (MQTT, HTTP/FastAPI), mapeadores que convertem modelos de dados externos como JSON em entidades de domínio, e as fontes de dados locais e remotas.

### 2.3. Camada `presentation/` 

* **Responsabilidade:** Gerencia a interface com o usuário e a interação em todas as plataformas suportadas (Android, Web e Desktop).  
* **Características:** Contém as telas,  widgets e o gerenciamento de estado da aplicação. Consome exclusivamente os Casos de Uso da camada de domínio, sem acesso direto às fontes de dados ou regras de negócio estruturais.

### 2.4. Camada `core/` 

* **Responsabilidade:** Concentra utilitários globais, tratamento centralizado de exceções, definições de constantes, configuração de injeção de dependências e extensões comuns a todo o projeto.  
* **Características:** Oferece suporte transversal a todas as outras camadas sem acoplá-las a regras de negócio específicas.

---

## 3\. Como as Camadas se Comunicam

A comunicação entre as camadas obedece estritamente a uma **regra de dependência unidirecional**, fluindo de fora para dentro, onde as camadas externas conhecem as internas, mas as internas ignoram a existência das externas:

1. **Presentation para Domain:** A interface de usuário invoca diretamente os **Casos de Uso** (`domain/usecases`) para executar ações ou obter dados, recebendo entidades puras de domínio.  
     
2. **Domain para Data (via Inversão de Dependência):** A camada de domínio define interfaces. A camada `data/` implementa essas interfaces. Através da injeção de dependências configurada no `core/`, o domínio interage com o mundo externo sem acoplamento direto às tecnologias de banco ou broker MQTT.  
     
3. **Core:** Fornece suporte transversal (como gerenciamento de estado global, logs e adaptadores de rede) acessível por qualquer camada, respeitando o isolamento do domínio.

---

## 4\. Desacoplamento e Facilidade de Testes

A separação rígida em camadas traz vantagens diretas para a qualidade, a manutenibilidade e a testabilidade do DSM Conecta:

* **Independência de Frameworks e UI:** Como a camada `domain/` não depende do Flutter, de bancos de dados ou de clientes MQTT, a lógica de negócio pode ser testada de forma isolada, rápida e sem necessidade de emuladores ou infraestrutura pesada.  
    
* **Mocks e Dublês de Teste Simples:** Como o domínio se comunica com a camada de dados por meio de interfaces, torna-se fácil substituir dependências reais por implementações simuladas durante os testes, permitindo validar a lógica de negócio de forma isolada e segura.  
    
* **Evolução Paralela:** Equipes e desenvolvedores diferentes podem trabalhar simultaneamente na interface (`presentation/`) e na infraestrutura de mensageria/banco (`data/`), desde que os contratos estabelecidos na camada `domain/` sejam respeitados.  
    
* **Conformidade com os Requisitos do Projeto:** Essa estrutura sustenta os requisitos de portabilidade, manutenibilidade e testabilidade estipulados na arquitetura distribuída do DSM Conecta, garantindo um código limpo, auditável e preparado para alta cobertura de testes.

