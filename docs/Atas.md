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

---


Visualizando Ata_04.md
**Atas de Reunião DSM - Conecta**  
—

**Ata 04**

**Data:** 27/10/2026  
**Local/Formato:** Teams - chamada  
**Participantes:** Guilherme Vieira dos Reis de Oliveira, Henrique Conceição Brito, Lucas Machado de Alencar

**Pauta:**

- Alinhamento das entregas da interação 2 do projeto DSM Conecta, validação dos testes de integração MQTT e divisão das responsabilidades técnicas.

**Pontos discutidos e decisões tomadas:**

- Foi revisado o andamento da interação 2, incluindo o sensor simulado, o broker MQTT, a publicação de eventos e o consumidor das mensagens.
- Durante a verificação dos testes, foi observada cobertura de aproximadamente 91%, acima do mínimo de 70% mencionado na reunião. Apesar do resultado geral, foram identificados ajustes pendentes no consumidor MQTT, especialmente na validação de mensagens duplicadas.
- Foi discutida a possibilidade de utilizar uma ferramenta de simulação, como o Wokwi ou alternativa equivalente, para representar o sensor externo. A escolha e a implementação dessa solução ainda precisam ser verificadas.
Atas de Reunião DSM - Conecta
—

**Ata 04**

**Data:** 27/10/2026
**Local/Formato:** Teams - chamada
**Participantes:** Guilherme Vieira dos Reis de Oliveira, Henrique Conceição Brito, Lucas Machado de Alencar

**Pauta:**

Alinhamento das entregas da interação 2 do projeto DSM Conecta, validação dos testes de integração MQTT e divisão das responsabilidades técnicas.
Pontos discutidos e decisões **tomadas:**

- Foi revisado o andamento da interação 2, incluindo o sensor simulado, o broker MQTT, a publicação de eventos e o consumidor das mensagens.
- Durante a verificação dos testes, foi observada cobertura de aproximadamente 91%, acima do mínimo de 70% mencionado na reunião. Apesar do resultado geral, foram identificados ajustes pendentes no consumidor MQTT, especialmente na validação de mensagens duplicadas.
- Foi discutida a possibilidade de utilizar uma ferramenta de simulação, como o Wokwi ou alternativa equivalente, para representar o sensor externo. A escolha e a implementação dessa solução ainda precisam ser verificadas.
- Foi alinhado que vale manter separados o sensor simulado e a aplicação Flutter, já que o sensor representa uma fonte externa de dados.
- A rubrica foi consultada e a leitura dos sensores do dispositivo mediante consentimento foi identificada como item da interação 2, com peso de 15% da nota. Localização, luminosidade e movimento foram citados como exemplos, mas a lista completa de sensores e o fluxo final de permissão ainda precisam ser conferidos na documentação. Foi discutida a criação de uma base mínima do aplicativo, priorizando a parte lógica de leitura e consentimento, sem necessidade de desenvolver uma interface completa nesta etapa.
- Foi discutida a criação de um arquivo de execução simplificada (por exemplo, um script .bat) para preparar dependências e facilitar a abertura dos terminais usados nos testes. Lucas ficou de estruturar essa solução.
- A possibilidade de um agente e de dashboards administrativos foi considerada como melhoria futura. A equipe decidiu não priorizar essas funcionalidades neste momento, retomando a avaliação depois que a aplicação e a base de dados estiverem mais estruturadas.
- Foi reforçada a necessidade de manter o backlog e os documentos na pasta docs do GitHub atualizados conforme o desenvolvimento avança.
Ações pendentes, **prazos e responsáveis:**

- Investigar e corrigir o ajuste pendente no sensor e no CI, verificando o contorno aplicado e buscando uma solução que não ignore falhas legítimas dos testes — **responsável:** Henrique.  **Prazo mencionado:** iniciar a verificação em 27/10/2026 e corrigir o quanto antes; data de conclusão não definida.
- Avaliar uma ferramenta de simulação para o sensor externo, como o Wokwi ou alternativa equivalente — **responsável:** Henrique. **Prazo:** não definido; atividade a iniciar durante o trabalho de conclusão da interação 2.
- Implementar a base do aplicativo Flutter para leitura dos sensores do dispositivo e tratar o consentimento necessário — **responsável:** Lucas. Prazo **mencionado:** iniciar em 27/10/2026; data de conclusão não definida.
- Investigar e corrigir a validação de mensagens duplicadas no consumidor MQTT — **responsável:** Lucas. **Prazo:** não definido; ajuste identificado durante os testes da reunião.
- Estruturar um script de execução simplificada para preparar dependências e facilitar a inicialização dos terminais de teste — **responsável:** Lucas. **Prazo:** não definido.
- Atualizar continuamente o backlog e os documentos do projeto conforme as atividades forem concluídas e as prioridades mudarem — **responsável:** equipe. **Prazo:** contínuo, com revisão antes da próxima reunião.
- Retomar a avaliação de agente e dashboards após a estrutura básica da aplicação e do banco de dados estar disponível — **responsável:** equipe; Henrique se dispôs a pesquisar a viabilidade de agentes. **Prazo:** sem data definida; não é prioridade imediata.

**Próxima reunião:**

- 02/11/2026
