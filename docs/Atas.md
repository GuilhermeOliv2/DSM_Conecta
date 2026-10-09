**Atas de Reunião DSM \- Conecta**  

---

**Ata 01**

**Data:** 22/09/26   
**Local/Formato:** Teams \- chamada   
**Participantes:** Henrique / Guilherme   

1. **Pauta:**   
   Alinhamento dos documentos de backlog e decisão de prioridades    
2. **Pontos Discutidos e Decisões Tomadas:**  
    Prioridade das entregas   
3. **Ações Pendentes, Prazos e Responsáveis:**  
    Proteção da Branch Principal, Pipeline de CI e Testes com TDD  
4. **Próxima Reunião:**  
    Não definida

---

**Ata 02**

**Data:** 23/09/2026  
 **Local/Formato:** Teams \- chamada  
 **Participantes:** Guilherme Vieira dos Reis de Oliveira, Henrique Conceição Brito, Lucas Machado de Alencar

**Pauta:**

* Definição de responsabilidades sobre o backlog e pipelines do projeto DSM Conecta

**Pontos discutidos e decisões tomadas:**

* O documento de backlog deve ser atualizado a cada interação, com status, comentários e prioridades  
* Foi discutida a divisão de tarefas do projeto DSM Conecta  
* Guilherme ficou responsável pelos testes com TDD, por já estar mais integrado ao ambiente Docker  
* Henrique ficou com o fluxo de versionamento em operação com o ramo principal protegido  
* Lucas ficou com a pipeline de integração contínua

**Ações pendentes, prazos e responsáveis:**

* Atualizar o backlog e os requisitos conforme novas interações — responsável: equipe  
* Realizar testes com TDD — responsável: Guilherme  
* Implementar/ajustar o fluxo de versionamento com proteção do ramo principal — responsável: Henrique  
* Trabalhar na pipeline de integração contínua — responsável: Lucas

**Próxima reunião:**

* 26/09/2026 - reunião de alinhamento
* 09/10/2026

---

**Ata 03**

**Data:** 09/10/2026
**Local/Formato:** Reunião on-line  
**Participantes:** Guilherme Vieira dos Reis de Oliveira, Henrique Conceição Brito, Lucas Machado de Alencar

**Pauta:**

* Alinhamento dos requisitos da Iteração 2 do DSM Conecta e divisão das tarefas relacionadas ao broker de mensageria, à publicação de eventos e à leitura de sensores.
* Organização do fluxo de versionamento, pull requests e revisão de código no GitHub.

**Pontos discutidos e decisões tomadas:**

* A equipe consultou o documento de visão e requisitos e a rubrica da entrega para interpretar o escopo da Iteração 2, que menciona broker de mensageria em operação, publicação de eventos, leitura de sensores e produtores de dados/nó sensor simulado.
* Foi discutida a dificuldade de testar a leitura dos sensores sem equipamento físico e antes de a interface do aplicativo estar disponível. A possibilidade de usar um sensor simulado foi considerada, mas a solução técnica ainda precisa ser definida.
* Foi discutida a necessidade de obter consentimento antes de qualquer coleta de dados. Luminosidade, movimento e localização foram citados como exemplos de dados; a lista completa precisa ser confirmada na documentação do projeto.
* A aplicação foi discutida no contexto de Flutter/Dart, com a possibilidade de utilizar Python no back-end. Ficou pendente detalhar como a leitura/simulação dos sensores será integrada à aplicação.
* A equipe alinhou que as alterações de código devem passar por pull requests no GitHub e por revisão de outro integrante. A revisão deve ser registrada na plataforma, com comentários e solicitação de ajustes quando necessário, antes do merge.

**Ações pendentes, prazos e responsáveis:**

* Implementar/estudar a leitura dos sensores e investigar uma forma de simulação na ausência de hardware físico — responsável: Henrique.
* Desenvolver a estrutura básica para a publicação de eventos e alinhar sua integração com a leitura dos sensores — responsável: Lucas, em conjunto com Henrique.
* Continuar trabalhando na configuração e no funcionamento do broker de mensageria — responsável: Guilherme.
* Confirmar a lista de dados coletados e detalhar o consentimento obrigatório antes da coleta — responsável: equipe.
* Utilizar branches e pull requests, solicitar revisão de outro integrante e registrar a validação do código no GitHub antes do merge — responsável: equipe.
* Verificar a configuração final das regras de merge/proteção da branch principal e o resultado completo dos checks da pipeline de CI — responsável: equipe.

**Próxima reunião:**

* 13/10/2026
