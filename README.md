# KANIVET XP — CYBER-GIT MDNATOR UNIVERSAL SUITE (ENTERPRISE EDITION v5.0)

# ========================================================================================
Autor Principal : Philipe Sampaio Lima (@OldBoy465)
Co-Autoria      : Engenharia de Prompts & Inteligência Artificial
Ano             : 2026
Contatos        : cienciaegestao@gmail.com | WhatsApp: +55 98 98250-6920
Repositório     : [https://github.com/OldBoy465](https://www.google.com/search?q=https://github.com/OldBoy465)

## 1. VISÃO GERAL DO SISTEMA

O Kanivet XP — Cyber-Git MDnator Universal Suite é uma aplicação desktop monolítica, robusta e de alta performance desenvolvida em Python 3 puro (Tkinter/TTK nativo). Ele foi arquitetado para unificar cinco grandes utilitários críticos de engenharia de software, automação de arquivos, deploy seguro e análise de dados em uma única interface standalone, com visual clássico retrô Windows XP / Java Swing e terminal integrado CRT de fósforo verde.

A aplicação opera de forma totalmente não-bloqueante (multi-threading nativo com workers em daemon), garantindo que varreduras massivas de diretórios, compilações pesadas de código, processamento estatístico de planilhas e operações de rede do Git jamais congelem a interface do usuário.

## 2. NÚCLEOS OPERACIONAIS INTEGRADOS

### 2.1. Sanitizador Heurístico Universal & Git Pusher

* Criação de Diretório Limpo: O projeto ativo nunca é alterado diretamente. O software gera um espelho de exportação em `<projeto>_clean_export`.
* Neutralização Automática de Credenciais e Segredos:
* Tokens de Bot do Telegram (\b\d{8,11}:[a-zA-Z0-9_-]{34,36}\b)
* Telegram Chat IDs numéricos atribuídos a variáveis de autorização
* GitHub Personal Access Tokens (ghp_, github_pat_, gho_)
* Chaves de IA (OpenAI sk-..., Anthropic sk-ant-...)
* Google Cloud API Keys (AIza...)
* AWS Access Key IDs (AKIA..., ASIA...)
* JWT Tokens assinados (eyJ...)
* Atribuições genéricas em Python, C/C++, Arduino, JS, JSON e YAML para 'password', 'token', 'secret', 'api_key'


* Bloqueio Estrito de Vazamento: Arquivos `.env`, chaves privadas (`.pem`, `.key`, `id_rsa`), certificados locais, bancos de dados SQLite (`.db`, `.sqlite`, `.sqlite3`), caches de compilação (`.build_cache`, `.pio`, `__pycache__`) são barrados e nunca entram no build.
* Geração de .gitignore Universal: Injeta automaticamente um arquivo de regras de exclusão blindado na raiz da pasta limpa.
* Deploy Seguro: Suporte a envio forçado (`--force`), renomeação de branch (`main`) e autenticação HTTPS direta com PAT via URL embutida em memória.

### 2.2. Central de Operações Git Baremetal

Execução nativa de comandos do Git diretamente no diretório do projeto ativo, com impressão de saída em tempo real no terminal CRT:

* git status (verificação de modificações e staged files)
* git log -n 5 (visualização do histórico recente da árvore)
* git diff (comparação linha a linha das alterações locais)
* git fetch --all (atualização de ponteiros e referências remotas)
* git pull origin  (mescla de atualizações remotas)
* git add . (indexação completa no stage)
* git commit -m (gravação com mensagem personalizada)
* git push origin  (envio para o servidor remoto)
* git remote -v (listagem de remotes configurados)
* git branch -a (exibição de todas as ramificações locais e remotas)
* git stash & git stash pop (armazenamento e recuperação de modificações voláteis)
* git clone (módulo dedicado para clonagem de repositórios remotos com seletor de pasta)

### 2.3. Motor MDnator v4.0 (Matrix Engine)

* Varredura profunda de projetos de software e hardware embarcado: Arduino Sketch (.ino), PlatformIO / ESP32 Header (.io), C/C++ (.c, .cpp, .h, .hpp), Python (.py), Web (HTML, CSS, JS, TS, PHP), Dados (JSON, XML, YAML, SQL).
* Geração de relatório consolidado em arquivo Markdown único (.md), composto por:
* Cabeçalho estruturado com metadados e data de geração
* Árvore de navegação ASCII completa e indentada
* Ingestão total do código-fonte de cada arquivo com identificadores e sintaxe syntax highlighting por linguagem
* Sumário de métricas de arquivos processados e total de linhas


* Ideal para alimentação massiva de Large Language Models (ChatGPT, Claude, Gemini, DeepSeek, modelos locais via Ollama/LM Studio) e documentação de código.
* Inspecionador de Métricas de Código: Analisa o volume total de arquivos, linhas estimadas e frequência por extensão sem precisar compilar o relatório completo.

### 2.4. Módulo InfoPlan (Análise Estrutural e Estatística de Planilhas)

* Engenharia reversa e diagnóstico dimensional para arquivos `.xlsx` e `.xls`.
* Resiliência de ambiente: Executa com `pandas` e `openpyxl`/`xlrd`; caso ausentes, orienta a instalação e opera com fallback nativo puro para letras de coluna.
* Métricas e dados extraídos:
* Metadados do arquivo (bytes, MB, última modificação, quantidade de abas)
* Dimensões por aba (linhas, colunas e range aproximado de células, ex: A1:H500)
* Detecção heurística de tipos: Booleano, Inteiro, Decimal, Data/Hora, Data em texto, Texto, Vazio
* Estatísticas descritivas completas: Soma, Média, Mediana, Desvio Padrão, Mínimo e Máximo
* Amostragem posicional de células reais (ex: B2 = 150.0, C2 = ATIVO)
* Amostra das primeiras 10 linhas da tabela (head)
* Balanço dimensional: total de células, preenchimento absoluto e percentual de ocupação


* Exportação direta do relatório em formato `.txt` ou `.md`.

### 2.5. Módulo Listador de Estruturas (Tree & Dump)

* Emulador e expansor nativo do utilitário `tree /F` do DOS/Windows, compatível com Windows, Linux e macOS sem depender de binários externos.
* Geração de arquivo de dump estrutural com nomenclatura automática padronizada: `estrutura_YYYY-MM-DD_HHhMMm.txt` na raiz do projeto ativo.
* Exibição paralela da árvore completa em tempo real no console CRT.

### 2.6. Módulo Hardware-Z (Telemetria do Computador)

* Diagnóstico estilo CPU-Z integrado, avaliando em tempo real a máquina host:
* Sistema Operacional, distribuição, versão e build
* Arquitetura da CPU (x86_64, ARM, etc.) e identificação do processador
* Núcleos lógicos (threads/vCPUs) e núcleos físicos
* Memória RAM Total, Usada, Livre e Percentual de Ocupação
* Capacidade, uso e espaço livre da partição raiz de armazenamento
* Tempo de atividade ininterrupto do sistema (Uptime)
* Suporte nativo via `shutil` e expansão de alta fidelidade via `psutil`.



### 2.7. Manual do Usuário Integrado & Dialog Windows Help

Acessível pelo menu superior (`Ajuda -> Manual do Usuário / Orientações...`) contendo 7 seções detalhadas de instrução técnica:

1. Como usar o Sanitizador e evitar vazamento de credenciais
2. O que fazer caso um token do Telegram ou chave vaze (revogação no BotFather e fechamento de alertas no GitHub Secret Scanning)
3. Como gerar e utilizar o GitHub Personal Access Token (PAT) com escopo `repo`
4. Como utilizar a Suite Git para commits, pulls e clones sem linha de comando
5. Como compilar projetos inteiros com o MDnator para alimentar IAs
6. Como extrair a radiografia estrutural de planilhas Excel pelo InfoPlan
7. Como gerar relatórios de estrutura e árvore de diretórios

## 3. REQUISITOS DO SISTEMA E COMPATIBILIDADE

* Interpretador: Python 3.8 ou superior (testado e homologado em Python 3.10, 3.11 e 3.12).
* Sistemas Operacionais Suportados:
* Windows 11, Windows 10, Windows 8.1, Windows 7
* Distribuições Linux (Ubuntu, Debian, Fedora, Arch, Mint) com pacote `python3-tk` ativo
* macOS (10.15 Catalina ou superior)


* Git: Git instalado e presente nas variáveis de ambiente do sistema (`PATH`) para as operações de commit, push e status.

## 4. INSTALAÇÃO E EXECUÇÃO

O Kanivet XP é um script monolítico autossuficiente. A interface gráfica opera 100% com as bibliotecas internas do Python.

### 4.1. Execução Imediata (Zero Dependências Externas)

Para rodar imediatamente com os módulos de Git, Sanitizador, MDnator, Listador de Estruturas e Telemetria básica:

```bash
python kanivet_xp.py

```

### 4.2. Pacote Completo (Recomendado para InfoPlan e Hardware-Z avançado)

Para habilitar o motor estatístico de planilhas e a telemetria detalhada de memória/CPU:

```bash
pip install pandas openpyxl xlrd psutil
python kanivet_xp.py

```

## 5. GUIA RÁPIDO DE OPERAÇÃO

1. Inicie o programa via terminal ou clique duplo no script.
2. Na barra superior "Seletor Global de Diretório / Projeto Ativo", clique em "Selecionar Pasta..." e aponte para o diretório do seu projeto de software, firmware ou planilhas.
3. Para publicar com segurança no GitHub:
* Verifique o `Git user.name` e `Git user.email`.
* Insira seu Token de Acesso Pessoal (PAT) com permissão `repo`.
* Clique em "🛡️ SANITIZAR PROJETO INTEIRO & ENVIAR AO GITHUB COM PAT". O software cuidará de limpar segredos, criar o `.gitignore`, estruturar os commits e realizar o push.


4. Para compilar seu código para IA:
* Acesse a aba "Motor MDnator v4.0" e clique em "Compilar Projeto Ativo em Markdown Único (.MD)".
* Anexe o arquivo `.md` gerado no prompt da sua LLM de preferência.


5. Para auditar planilhas:
* Vá na aba "Módulo InfoPlan", selecione qualquer arquivo `.xlsx` ou `.xls` e salve a radiografia completa.


6. Para diagnosticar a sua máquina:
* Acesse a aba "Hardware-Z" e clique em "Atualizar Telemetria de Hardware Agora".



## 6. POLÍTICA DE SEGURANÇA E HIGIENIZAÇÃO

O motor de sanitização do Kanivet XP foi desenvolvido segundo o princípio de menor privilégio e isolamento de arquivos:

* Nenhuma modificação destrutiva é feita sobre a pasta original do usuário.
* O pipeline de deploy opera exclusivamente sobre o diretório de exportação limpa.
* O token PAT utilizado para o transporte HTTPS nunca é registrado em texto claro nas mensagens de commit nem gravado em arquivos de log públicos.

## 7. CRÉDITOS E INFORMAÇÕES DE DESENVOLVIMENTO

* Projeto: Kanivet XP — Cyber-Git MDnator Universal Suite
* Versão: 5.0 Enterprise Monolithic Standalone
* Engenheiro Responsável: Philipe Sampaio Lima (@OldBoy465)
* Assistência Técnica: Inteligência Artificial & Engenharia de Prompts
* Localização: São Luís, Maranhão, Brasil
* Ano de Homologação: 2026
