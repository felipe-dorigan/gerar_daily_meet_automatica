# 🚀 Instruções de Deploy

## Problema Atual
O GitHub está bloqueando o push devido à detecção de tokens sensíveis no histórico do Git.

## Soluções Possíveis

### Opção 1: Criar Novo Repositório
1. Crie um novo repositório no GitHub (ex: `daily-meet-generator`)
2. Use este comando para adicionar o novo remote:
   ```bash
   git remote set-url origin https://github.com/felipe-dorigan/daily-meet-generator.git
   ```

### Opção 2: Ignorar Proteção (Temporário)
1. Acesse a URL fornecida pelo GitHub no erro
2. Clique em "Allow secret" temporariamente
3. Faça o push novamente

### Opção 3: GitHub CLI
Se você tem o GitHub CLI instalado:
```bash
gh repo create gerar-daily-meet --public
git push origin main
```

## ✅ Status Atual
- ✅ Código limpo sem tokens sensíveis
- ✅ Arquivos de exemplo criados
- ✅ Configuração externa implementada
- ✅ Documentação atualizada
- ⚠️ Aguardando push para repositório

## 📁 Arquivos Prontos
- `agendar_reuniao.py` - Script principal
- `config.py.example` - Exemplo de configurações
- `credentials.json.example` - Template do Google
- `link_meet.txt.example` - Exemplo de link
- `requirements.txt` - Dependências
- `README.md` - Documentação completa
- `.gitignore` - Ignora arquivos sensíveis