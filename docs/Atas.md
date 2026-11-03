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
Ações pendentes

**prazos e responsáveis:**

- Investigar e corrigir o ajuste pendente no sensor e no CI, verificando o contorno aplicado e buscando uma solução que não ignore falhas legítimas dos testes — **responsável:** Henrique.  **Prazo mencionado:** iniciar a verificação em 27/10/2026 e corrigir o quanto antes; data de conclusão não definida.
- Avaliar uma ferramenta de simulação para o sensor externo, como o Wokwi ou alternativa equivalente — **responsável:** Henrique. **Prazo:** não definido; atividade a iniciar durante o trabalho de conclusão da interação 2.
- Implementar a base do aplicativo Flutter para leitura dos sensores do dispositivo e tratar o consentimento necessário — **responsável:** Lucas. Prazo **mencionado:** iniciar em 27/10/2026; data de conclusão não definida.
- Investigar e corrigir a validação de mensagens duplicadas no consumidor MQTT — **responsável:** Lucas. **Prazo:** não definido; ajuste identificado durante os testes da reunião.
- Estruturar um script de execução simplificada para preparar dependências e facilitar a inicialização dos terminais de teste — **responsável:** Lucas. **Prazo:** não definido.
- Atualizar continuamente o backlog e os documentos do projeto conforme as atividades forem concluídas e as prioridades mudarem — **responsável:** equipe. **Prazo:** contínuo, com revisão antes da próxima reunião.
- Retomar a avaliação de agente e dashboards após a estrutura básica da aplicação e do banco de dados estar disponível — **responsável:** equipe; Henrique se dispôs a pesquisar a viabilidade de agentes. **Prazo:** sem data definida; não é prioridade imediata.

**Próxima reunião:**

- 03/11/2026

---

**Ata 05**

**Data:** 03/11/2026
**Local/Formato:** Reunião on-line - chamada  
**Participantes:** Guilherme Vieira dos Reis de Oliveira, Henrique Conceição Brito, Lucas Machado de Alencar

**Pauta:**

- Revisão e organização da entrega da Iteração 2 do projeto DSM Conecta.
- Planejamento e divisão das atividades da Iteração 3, envolvendo ingestão assíncrona, modelagem da base de série temporal e carga sintética.
- Alinhamento inicial do escopo e das atividades preparatórias da Iteração 4.

**Pontos discutidos e decisões tomadas:**

- Foi revisada a pendência relacionada à leitura dos sensores do celular. Lucas informou que a leitura já estava funcionando localmente e que as variações eram exibidas na tela do dispositivo, mas os dados ainda não estavam sendo enviados para outro serviço.
- Foi discutida a necessidade de limitar a coleta ao que for efetivamente utilizado. A localização foi mencionada como possível dado útil para identificar a presença na faculdade; já os dados de movimentação do celular poderiam permanecer como informação interna do aplicativo, sem envio ou armazenamento, pois não foi identificado um uso necessário para eles.
- Lucas informou que havia preparado uma estrutura simples relacionada ao consentimento e à possibilidade de cancelar a assinatura de um sensor, interrompendo o envio de dados. A interface apresentada ainda não correspondia à tela final do aplicativo.
- A equipe considerou manter a implementação atual dos sensores no Flutter, que estava funcionando. A migração para uma ferramenta externa de simulação, como o Wokwi, foi tratada como melhoria opcional, a ser considerada somente se houver tempo disponível.
- Foi esclarecida a questão das mensagens duplicadas no consumidor MQTT. O teste anterior havia enviado apenas uma mensagem, portanto ela foi corretamente aceita como primeiro envio. A validação utiliza o ID do envio; assim, o comportamento observado não foi considerado um defeito pendente.
- As demais pendências da Iteração 2 foram consideradas encaminhadas. A equipe organizou a entrega pelo GitHub, com revisão/aprovação de pull request, acompanhamento da execução dos testes, criação da tag referente à Iteração 2 e preparação do envio do link do repositório por e-mail.
- Foram revisados os itens de desenvolvimento da iteração: serviço de ingestão assíncrona, validação de mensagens duplicadas e persistência, base de série temporal modelada e carga sintética.
- Henrique informou que já havia iniciado testes para gerar e validar uma carga sintética de um milhão de registros. Para isso, identificou a necessidade de ajustar ou criar estruturas e tabelas no PostgreSQL.
- A modelagem da base de série temporal foi discutida considerando a organização temporal dos dados, a estrutura e os tipos das colunas, os padrões de consulta e a política de retenção. Também foi debatido por quanto tempo os dados seriam mantidos, quando deveriam ser descartados ou transferidos para armazenamento de longo prazo e quais informações realmente precisariam ser coletadas.
- A definição sobre utilizar banco de dados local ou em nuvem não foi concluída durante a conversa; foi observado que essa escolha pode afetar a configuração e depender da máquina disponível.
- A divisão de responsabilidades foi confirmada ao final da reunião: Guilherme ficará com o serviço de ingestão assíncrona; Henrique ficará com a carga sintética; Lucas ficará com a modelagem da base de série temporal.
- A equipe fez uma leitura inicial dos entregáveis previstos: interface de programação documentada e autenticada, com endpoints de conteúdo e métricas; canal de comunicação em tempo real; e motor de análise com janela deslizante, média móvel e detecção de desvios/anomalias.
- Foi discutida a necessidade de planejar a interface e os contratos de comunicação antes de implementar a integração. Como preparação, a equipe pretende elaborar um esboço (*sketch*) da interface e revisar os modelos que Henrique havia compartilhado no grupo. Os modelos ainda estavam em estágio inicial.
- Foi sugerido utilizar como referência a solução de chat desenvolvida anteriormente no projeto Pikassistent, avaliando o reaproveitamento dos conceitos de comunicação e uma possível adaptação para Dart. Essa possibilidade não foi definida como decisão técnica final.
- O funcionamento do motor de análise ainda precisava ser melhor compreendido. A descrição consultada indicava um componente que analisa continuamente os eventos recebidos, identifica tendências de acesso e detecta comportamentos fora do padrão. A equipe relacionou essa atividade à análise/mineração de dados e à geração de gráficos ou indicadores.
- Lucas se dispôs a pesquisar melhor o requisito do motor de análise e mencionou a possibilidade de apoiar a geração e o envio de gráficos utilizando Python. A divisão definitiva das tarefas da Iteração 4 não foi fechada.
- Também foram discutidos os critérios de latência entre a publicação e a exibição dos eventos, autenticação e tratamento de erros. A equipe reconheceu que esses pontos precisarão ser implementados e medidos;

**Ações pendentes, prazos e responsáveis:**

- Desenvolver o serviço de ingestão assíncrona, incluindo validação de mensagens duplicadas e persistência — **responsável:** Guilherme.
- Implementar e validar a geração da carga sintética de um milhão de registros, realizando os ajustes necessários no PostgreSQL — **responsável:** Henrique.
- Modelar a base de série temporal, considerando estrutura dos dados, organização temporal e política de retenção — **responsável:** Lucas.
- Avaliar o reaproveitamento da solução de comunicação do Pikassistent como referência para a nova interface de programação — **responsável:** equipe.

**Próxima reunião:**

- 07/11/2026
