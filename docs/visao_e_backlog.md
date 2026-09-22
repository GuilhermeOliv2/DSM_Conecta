**Documento de visão e backlog \- DSM conecta** 

**1.Visão geral do produto**

O DSM Conecta é a plataforma oficial do curso de Desenvolvimento de Software Multiplataforma da FATEC Zona Sul, projetada para conectar futuros alunos, estudantes e a coordenação em um único ecossistema digital. O aplicativo simplifica o acesso a informações essenciais do curso como apresentação institucional, formas de ingresso e matriz curricular detalhada, destaca as competências técnicas adquiridas pelos alunos através de uma vitrine de projetos e depoimentos reais, e mantém a comunidade informada com a agenda de eventos e prazos do processo seletivo, além de oferecer um canal direto de comunicação e tirar-dúvidas com a coordenação.

**2.Fora de Escopo**

* Não haverá integração com o sistema acadêmico da Fatec nem com o sistema de inscrição do processo seletivo/vestibular.   
* Não será realizada a publicação do app na Google Play Store ou App Store, por depender de contas institucionais.   
* Não haverá aquisição, montagem ou instalação de hardware/placas físicas de sensores (a telemetria utiliza os sensores nativos dos aparelhos dos visitantes e nós de sensoriamento simulados).   
* O aplicativo será gerado a partir de código único em Flutter para Android, Web e Desktop, ficando o iOS de fora devido à necessidade de infraestrutura proprietária de compilação.   
* Não será feito nenhum cadastro coletando dados pessoais identificáveis dos visitantes, mantendo a identificação exclusivamente por ID aleatório de sessão (em conformidade com a LGPD). 

**3\. Requisitos Funcionais**	

| ID | Descrição do Requisito | Prioridade | Status | Comentários | Iteração Prevista |
| ----- | ----- | :---: | :---: | ----- | :---: |
| RF01 | Exibir a apresentação institucional do curso | alta | Em Desenvolvimento |  | Iteração 5 |
| RF02 | Disponibilizar matriz curricular com a descrição resumida | alta | Em Desenvolvimento |  | Iteração 5 |
| RF03 | Apresentar vitrine de projetos desenvolvidos pelos estudantes | média | Em Desenvolvimento |  | Iteração 5 |
| RF04 | Exibir depoimentos de estudantes e egressos | média | Em Desenvolvimento |  | Iteração 5 |
| RF05 | Apresentar a agenda de eventos, prazos e etapas do processo seletivo | alta | Em Desenvolvimento |  | Iteração 5 |
| RF06 | Disponibilizar canal de dúvidas | alta | Em Desenvolvimento |  | Iteração 5 |
| RF07 | Permitir o compartilhamento de conteúdos do aplicativo | baixa | Não Iniciado |  | Iteração 5 |
| RF08 | Operar com o conteúdo armazenado localmente quando não houver conexão de rede. | média | Não Iniciado |  | Iteração 5 |
| RF09 | Permitir que o visitante responda ao questionário de afinidade vocacional | baixa | Não Iniciado |  | Iteração 5 |
| RF10 | Registrar a presença do visitante em evento de divulgação por leitura de código QR. | média | Não Iniciado |  | Iteração 5 |
| RF11 | Registrar a presença por proximidade geográfica | baixa | Não Iniciado |  | Iteração 5 |
| RF12 | Apresentar ao visitante o histórico das próprias interações | baixa | Não Iniciado |  | Iteração 5 |
| RF13 | Publicar cada interação relevante do aplicativo como mensagem em tópico do broker de mensageria. | média | Não Iniciado |  | Iteração 2 |
| RF14 | Coletar leituras dos sensores do dispositivo | média | Não Iniciado |  | Iteração 2 |
| RF15 | Receber leituras provenientes de nó sensor externo simulado | média | Não Iniciado |  | Iteração 2 |
| RF16 | Validar o formato e a versão do esquema de cada mensagem recebida antes da persistência. | alta | Não Iniciado |  | Iteração 3 |
| RF17 | Descartar mensagens duplicadas ou malformadas | alta | Não Iniciado |  | Iteração 3 |
| RF18 | Persistir as mensagens válidas na base de série temporal preservando o instante de origem. | alta | Não Iniciado |  | Iteração 3 |
| RF19 | Exibir, em tempo real, a contagem de visitantes ativos e de registros de presença por evento. | média | Não Iniciado |  | Iteração 4 |
| RF20 | Apresentar o ranking dos conteúdos mais acessados em janela deslizante configurável. | baixa | Não Iniciado |  | Iteração 4 |
| RF21 | Exibir a distribuição dos resultados do questionário de afinidade vocacional. | média | Não Iniciado |  | Iteração 4 |
| RF22 | Emitir alerta quando o volume de acessos ultrapassar o limiar estatístico definido para a janela corrente. | baixa | Não Iniciado |  | Iteração 4 |
| RF23 | Permitir a gestão do conteúdo do aplicativo, com inclusão, alteração e remoção por usuário autenticado. | alta | Não Iniciado |  | Iteração 5 |
| RF24 | Permitir a exportação dos dados agregados nos formatos CSV e JSON. | média | Não Iniciado |  | Iteração 6 |
| RF25 | Publicar painel público de métricas agregadas e anonimizadas, acessível sem autenticação. | baixa | Não Iniciado |  | Iteração 6 |

**4\. Requisitos Não Funcionais**

| ID | Descrição do Requisito | Prioridade | Status | Comentários | Iteração Prevista |
| ----- | ----- | ----- | :---: | ----- | :---: |
| RNF01 | O aplicativo cliente deve ser gerado para Android, navegador web e desktop com um unico codigo | alta | Não Iniciado |  | Iteração 5 |
| RNF02 | As interfaces de programação devem ser descritas em OpenAPI 3, e o transporte de telemetria deve seguir o protocolo MQTT na versão 3.1.1 ou superior. | alta | Em Desenvolvimento |  | Iteração 4 |
| RNF03 | Os dados abertos devem ser publicados em formatos não proprietários, com dicionário de dados disponível. |   média | Não Iniciado |  | Iteração 6 |
| RNF04 | 95% das requisições à interface de programação devem ser respondidas em até 500 milissegundos sob carga nominal. | alta | Não Iniciado |  | Iteração 4 |
| RNF05 | Um evento publicado no broker deve estar visível no painel em tempo real em até 3 segundos | média | Não Iniciado |  | Iteração 4 |
| RNF06 | O sistema deve sustentar 1000 clientes conectados e 50 mensagens por segundo sem perda de mensagens em qualidade de serviço 1 | alta | Não Iniciado |  | Iteração 6 |
| RNF07 | O serviço de ingestão deve permitir a execução de múltiplas instâncias simultâneas sem duplicação de registros | alta | Não Iniciado |  | Iteração 3 |
| RNF08 | A base de dados deve manter o tempo de consulta dos painéis abaixo de 2 segundos com pelo menos um milhão de registros armazenados | alta | Não Iniciado |  | Iteração 3 |
| RNF09 | A ingestão de dados deve ser assíncrona e concorrente, com tratamento de contrapressão quando a taxa de chegada superar a de gravação | alta | Não Iniciado |  | Iteração 3 |
| RNF10 | O cliente deve permanecer alheio à localização física dos serviços consumidos, atendendo às transparências de acesso e de localização | baixa | Não Iniciado |  | Iteração 4 |
| RNF11 | A indisponibilidade temporária do broker não deve interromper o uso do aplicativo, que armazena os eventos localmente para envio posterior | média | Não Iniciado |  | Iteração 5 |
| RNF12 | O acesso administrativo deve exigir autenticação por token e trafegar sobre canal cifrado | alta | Não Iniciado |  | Iteração 4 |
| RNF13 | Credenciais e segredos devem residir em variáveis de ambiente, nunca no repositório de código | alta | Em Desenvolvimento | Já implementado o .gitignore com .env dentro dele para armazenamento de senhas e segredos com segurança | Iteração 4 |
| RNF14 | A coleta de dados deve ser precedida de consentimento explícito, informado e revogável, em conformidade com a Lei nº 13.709/2018 | alta | Não Iniciado |  | Iteração 2 |
| RNF15 | A identificação do visitante deve ocorrer por identificador aleatório de sessão, sem vinculação a dado pessoal | alta | Não Iniciado |  | Iteração 2 |
| RNF16 | O painel público não deve exibir informação que permita a reidentificação de um visitante | alta | Não Iniciado |  | Iteração 5 |
| RNF17 | A cobertura de testes automatizados do back-end deve ser de no mínimo setenta por cento das linhas | média | Não Iniciado |  | Iteração 1 |
| RNF18 | A integração contínua deve impedir a incorporação de alterações com teste falhando | média | Não Iniciado |  | Iteração 1 |
| RNF19 | A interface deve atender a requisitos básicos de acessibilidade, com contraste adequado, rótulos para leitores de tela e suporte ao aumento do tamanho de fonte | alta | Não Iniciado |  | Iteração 6 |
| RNF20 | Os dados brutos de telemetria devem ser retidos por noventa dias e os dados agregados por cinco anos | média | Não Iniciado |  | Iteração 3 |

**5\. Cronograma de Iterações**

| Iteração | Previsão de entrega | Objetivo e Entregáveis | Status | Comentarios |
| ----- | ----- | ----- | :---: | ----- |
| 0 | 14/09/2026 | Iniciação, levantamento de requisitos, arquitetura, contratos e ambiente docker compose | Em Andamento | Sem ata formalizada nesta sessão; pendência sob alinhamento da equipe para as próximas reuniões. |
| 1 | 28/09/2026 | Controle de versão, integração contínua e fundação da prática de testes | Não Iniciado |  |
| 2 | 12/10/2026 | Broker de mensageria, produtores de dados e nó sensor simulado | Não Iniciado |  |
| 3 | 26/10/2026 | Serviço de ingestão concorrente e persistência em série temporal | Não Iniciado |  |
| 4 | 09/11/2026 | Interface de programação e motor de análise em tempo real | Não Iniciado |  |
| 5 | 23/11/2026 | Aplicativo cliente nas três plataformas e painel administrativo | Não Iniciado |  |
| 6 | 07/12/2026 | Ensaio de carga, documentação final, ação de divulgação e apresentação pública | Não Iniciado |  |

