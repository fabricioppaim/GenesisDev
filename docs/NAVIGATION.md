# Genesis - Guia de Navegação dos Documentos de Setup

## 📚 Documentação Disponível

Este projeto possui documentação estruturada em camadas para diferentes necessidades:

```
📝 Documentação de Setup
├── 🎯 QUICKSTART.md (5 min - Iniciar rapidamente)
├── 📋 SETUP_EXECUCAO.md (30 min - Guia completo passo a passo)
├── 🔧 SCRIPTS_SETUP.md (Automatizado - Scripts prontos)
└── 📖 NAVIGATION.md (Você está aqui!)
```

---

## 🚀 Escolha Seu Caminho

### Opção 1️⃣: "Quero executar AGORA" ⚡
**Tempo**: ~5 minutos (com tudo já instalado)

📖 Leia: [QUICKSTART.md](QUICKSTART.md)

**O que faz**: Fornece 4 terminais com comandos prontos para iniciar backend, frontend, database e observabilidade.

**Cenário ideal**: Você já tem Python, Node.js, SQL Server e credenciais Azure configurados.

```bash
# Quick flow:
1. Terminal 1: cd backend && source venv/bin/activate && uvicorn main:app --reload
2. Terminal 2: cd frontend && npm run dev
3. Terminal 3: cd backend && alembic upgrade head
4. (Opcional) Terminal 4: docker-compose up
```

---

### Opção 2️⃣: "Preciso de Setup Completo" 🔧
**Tempo**: ~30-45 minutos (primeira vez)

📖 Leia: [SETUP_EXECUCAO.md](SETUP_EXECUCAO.md)

**O que faz**: Guia detalhado com 9 fases cobrindo:
- Validação de pré-requisitos
- Criação de virtual environments
- Configuração de banco de dados
- Setup de autenticação OIDC (Entra ID)
- Integração com Azure Key Vault
- Integração com Jenkins e Azure DevOps
- Observabilidade (Elastic Stack)
- Troubleshooting detalhado

**Cenário ideal**: Setup inicial, primeira volta ou você precisa entender cada passo.

```
Fases:
1. Preparação do Ambiente Local
2. Configuração do Backend (FastAPI)
3. Configuração do Frontend (Next.js)
4. Autenticação OIDC (Entra ID)
5. Configuração do SQL Server
6. Configuração do Azure Key Vault
7. Integração com Jenkins
8. Integração com Azure DevOps
9. Observabilidade (Elastic Stack)
```

---

### Opção 3️⃣: "Scripts Automatizados" 🤖
**Tempo**: ~10-15 minutos (automático)

📖 Leia: [SCRIPTS_SETUP.md](SCRIPTS_SETUP.md)

**O que faz**: Scripts prontos (PowerShell, Bash) que automatizam o setup completo.

**Includes**:
- `setup-windows.ps1` — Setup total Windows
- `setup-unix.sh` — Setup total Linux/macOS
- `backend-setup.sh` — Só backend
- `frontend-setup.sh` — Só frontend
- `database-setup.sql` — Schema SQL
- `docker-compose.elastic.yml` — Stack observabilidade

**Cenário ideal**: Automatizar setup em CI/CD, novas máquinas ou developers novos.

```bash
# Windows:
.\scripts\setup-windows.ps1

# Linux/macOS:
./scripts/setup-unix.sh

# Ou selecionar componentes individuais:
./scripts/backend-setup.sh
./scripts/frontend-setup.sh
```

---

## 📊 Matriz de Decisão

| Necessidade | Documento | Tempo |
|-------------|-----------|-------|
| "Executar em 5 min" | [QUICKSTART.md](QUICKSTART.md) | ⚡ 5 min |
| "Entender cada passo" | [SETUP_EXECUCAO.md](SETUP_EXECUCAO.md) | 📋 30 min |
| "Automatizar tudo" | [SCRIPTS_SETUP.md](SCRIPTS_SETUP.md) | 🤖 10 min |
| "Só backend" | [SCRIPTS_SETUP.md](SCRIPTS_SETUP.md) > Backend Setup | 🔧 5 min |
| "Só frontend" | [SCRIPTS_SETUP.md](SCRIPTS_SETUP.md) > Frontend Setup | 🎨 3 min |
| "Só database" | [SCRIPTS_SETUP.md](SCRIPTS_SETUP.md) > Database Setup | 💾 2 min |
| "Com observabilidade" | [SETUP_EXECUCAO.md](SETUP_EXECUCAO.md) > Fase 9 | 📊 15 min |
| "Troubleshooting" | [SETUP_EXECUCAO.md](SETUP_EXECUCAO.md) > Troubleshooting | 🐛 5-10 min |

---

## 🔄 Fluxos Recomendados

### 🆕 Novo Developer (Nunca setou antes)

1. Ler [SETUP_EXECUCAO.md](SETUP_EXECUCAO.md) **Fase 1** (pré-requisitos)
2. Executar [SCRIPTS_SETUP.md](SCRIPTS_SETUP.md) > `setup-windows.ps1` ou `setup-unix.sh`
3. **PARAR** e atualizar `.env` e `.env.local` com credenciais
4. Consultar [SETUP_EXECUCAO.md](SETUP_EXECUCAO.md) **Fases 4-6** para Entra ID + Key Vault
5. Depois seguir [QUICKSTART.md](QUICKSTART.md) para rodar

**Tempo total**: ~60 minutos (primeira vez com configuração de credenciais)

---

### 👨‍💼 Setup Repetido (Máquina nova, mesmo projeto)

1. Executar `setup-windows.ps1` ou `setup-unix.sh`
2. Copiar `.env` de colega (secretos já configurados)
3. Copiar `.env.local` de colega
4. Seguir [QUICKSTART.md](QUICKSTART.md)

**Tempo total**: ~15 minutos

---

### 🚀 Deploy / CI-CD

1. Usar scripts de [SCRIPTS_SETUP.md](SCRIPTS_SETUP.md)
2. Injetar variáveis de ambiente via pipeline
3. Executar migrations
4. Start services

**Exemplo (GitHub Actions)**:
```yaml
- run: ./scripts/setup-unix.sh
- run: cd backend && alembic upgrade head
- run: cd backend && gunicorn -w 4 main:app
```

---

### 🔍 Debug / Troubleshooting

1. Consultar [SETUP_EXECUCAO.md](SETUP_EXECUCAO.md) > **Troubleshooting**
2. Verificar URLs em endpoint do docum correspondente
3. Checar `.env` se credenciais estão corretas

---

## 📋 Checklist Geral

Independente do caminho escolhido, ao final você deve ter:

### ✅ Infrastructure
- [ ] Python 3.11+ instalado
- [ ] Node.js 18+ + npm 9+ instalado
- [ ] SQL Server 2019+ rodando
- [ ] Git configurado

### ✅ Backend
- [ ] Virtual environment criado em `backend/venv`
- [ ] `backend/.env` criado com todas as variáveis
- [ ] Dependencies instaladas via pip
- [ ] Migrations executadas: `alembic upgrade head`
- [ ] Backend rodando em `http://localhost:8000`
- [ ] Swagger acessível em `http://localhost:8000/docs`

### ✅ Frontend
- [ ] `frontend/.env.local` criado com variáveis
- [ ] Dependencies instaladas via npm
- [ ] Frontend rodando em `http://localhost:3000`
- [ ] Login OIDC testado (autenticação Entra ID)

### ✅ Database
- [ ] Database `genesis_dev` criado
- [ ] Usuário `genesis_user` criado
- [ ] Schema base criado (via migrations ou SQL)

### ✅ Security (Configurado)
- [ ] Entra ID aplicações registradas (backend + frontend)
- [ ] Azure Key Vault criado
- [ ] Segredos armazenados: jenkins-token, azure-devops-pat, etc.

### ✅ (Opcional) Observabilidade
- [ ] Elastic Stack rodando (docker-compose)
- [ ] Kibana acessível em `http://localhost:5601`
- [ ] APM Server em `http://localhost:8200`

---

## 🎯 Próximas Etapas Após Setup

1. **Validar CRUD básico**
   - Criar Empresa via API/Frontend
   - Criar Ambiente
   - Criar Aplicação
   - Criar Instância
   - Validar trilha de auditoria

2. **Testar Autenticação**
   - Login no frontend
   - Verificar token no localStorage
   - Testar requisições autenticadas

3. **Integração Jenkins/Azure DevOps** (Opcional)
   - Disparar pipeline via API
   - Receber webhook callback
   - Validar correlação de execução

4. **Desenvolvimento**
   - Implementar endpoints restantes
   - Adicionar validações
   - Criar testes unitários

---

## 📞 Suporte

| Problema | Referência |
|----------|-----------|
| Erro na instalação | [SETUP_EXECUCAO.md](SETUP_EXECUCAO.md#-troubleshooting) |
| Porta já em uso | [SETUP_EXECUCAO.md](SETUP_EXECUCAO.md#erro-porta-8000-já-em-uso) |
| CORS error | [SETUP_EXECUCAO.md](SETUP_EXECUCAO.md#erro-invalid-cors-origin-no-frontend) |
| DB não conecta | [SETUP_EXECUCAO.md](SETUP_EXECUCAO.md#erro-connection-refused-no-sql-server) |
| OIDC discovery fail | [SETUP_EXECUCAO.md](SETUP_EXECUCAO.md#erro-oidc-discovery-url-not-reachable) |
| Scripts não executam | [SCRIPTS_SETUP.md](SCRIPTS_SETUP.md#-troubleshooting) |

---

## 📌 Documentos Relacionados

- [Documentação Técnica: Fluxos](fluxos.md)
- [Arquitetura: EPC-A-001](epc/EPC-A-001%20—%20Fundação%20do%20Domínio%20(SQL%20Server%20+%20FastAPI%20+%20Next.js).md)
- [Decisões: ADR-B-003 (Webhook + OIDC)](adr/ADR-B-003-Webhook-Receiver-separado-Auth-OIDC.md)
- [Contexto do Projeto](../project-context.md)

---

## 🔗 Links Úteis

- **FastAPI Docs**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com/)
- **Next.js Docs**: [nextjs.org](https://nextjs.org/docs/)
- **SQL Server**: [microsoft.com/sql-server](https://www.microsoft.com/sql-server)
- **Entra ID**: [microsoft.com/entra](https://www.microsoft.com/entra/)
- **Azure Key Vault**: [learn.microsoft.com/key-vault](https://learn.microsoft.com/pt-br/azure/key-vault/)
- **Jenkins Docs**: [jenkins.io](https://jenkins.io/)
- **Azure DevOps**: [dev.azure.com](https://dev.azure.com/)

---

**Última atualização**: 16 de fevereiro de 2026  
**Versão**: 1.0

