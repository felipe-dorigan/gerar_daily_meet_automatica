# Gerador Automático de Daily Meet

Sistema automatizado para criar reuniões do Google Meet e enviar notificações no Discord para dailies.

## Funcionalidades

- 🤖 **Automático**: Agenda reuniões automaticamente
- ⏰ **Horários Inteligentes**: Agenda para o próximo múltiplo de 10 minutos (com mínimo de 5 min de antecedência)
- 🔄 **Link Fixo**: Reutiliza o mesmo link do Meet para todas as reuniões
- 📅 **Dias Úteis**: Funciona apenas em dias úteis (segunda a sexta)
- 🎯 **Discord**: Envia notificação automática no Discord com @everyone
- 🏖️ **Feriados**: Ignora feriados brasileiros

## Configuração

### 1. Dependências

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client discord.py holidays
```

### 2. Credenciais do Google

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um projeto ou selecione um existente
3. Ative as APIs:
   - Google Calendar API
   - Google Meet API (opcional)
4. Crie credenciais OAuth 2.0
5. Baixe o arquivo `credentials.json` e coloque na pasta do projeto

### 3. Bot do Discord

1. Crie um bot no [Discord Developer Portal](https://discord.com/developers/applications)
2. Copie o token do bot
3. Adicione o bot ao seu servidor com permissões de envio de mensagens

### 4. Configurações

1. **Copie o arquivo de configuração**:

   ```bash
   cp config.py.example config.py
   ```

2. **Configure suas credenciais** no arquivo `config.py`:

   ```python
   EMAIL_CONVIDADO = "seu.email@gmail.com"
   DISCORD_TOKEN = "seu_token_do_discord"
   DISCORD_CANAL_ID = 123456789  # ID do canal do Discord
   MENSAGEM = "Bom dia, @everyone \n\n Link da Daily, início às {hora} \n\n {link_meet}"
   ```

3. **Configure as credenciais do Google**:
   ```bash
   cp credentials.json.example credentials.json
   ```
   Depois substitua o conteúdo com suas credenciais reais do Google Cloud Console.

## Como Usar

### Execução Manual

```bash
python agendar_reuniao.py
```

### Execução Automática (Windows)

Use o Agendador de Tarefas do Windows para executar automaticamente:

1. Abra `taskschd.msc`
2. Crie uma nova tarefa
3. Configure para executar de segunda a sexta às 08:20
4. Ação: executar `python` com argumento `agendar_reuniao.py`
5. Diretório inicial: pasta do projeto

## Como Funciona

1. **Verifica se é dia útil** (não é fim de semana nem feriado)
2. **Calcula o próximo horário** múltiplo de 10 minutos
3. **Reutiliza o link existente** (salvo em `link_meet.txt`) ou cria um novo
4. **Cria evento no Google Calendar** com o link
5. **Envia notificação no Discord** com @everyone

## Estrutura de Arquivos

```
├── agendar_reuniao.py       # Script principal
├── config.py.example        # Exemplo de configurações
├── config.py               # Suas configurações (não versionado)
├── credentials.json.example # Exemplo de credenciais Google
├── credentials.json        # Credenciais do Google (não versionado)
├── token.pickle           # Token de autenticação (não versionado)
├── link_meet.txt.example  # Exemplo de link do Meet
├── link_meet.txt         # Link fixo da reunião (não versionado)
├── requirements.txt      # Dependências Python
├── .gitignore           # Arquivos ignorados pelo Git
└── README.md           # Documentação
```

## Segurança

⚠️ **Importante**:

- Nunca compartilhe `credentials.json` ou tokens
- Use variáveis de ambiente em produção
- O `token.pickle` contém credenciais sensíveis

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request
