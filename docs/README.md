# 📚 Genesis - Documentação de Setup & Execução

## 🎯 Bem-vindo!

Esta pasta contém toda a documentação necessária para **setup, configuração e execução** do projeto Genesis (CMDB avançado com FastAPI + Next.js).

---

## 📖 Documentos Disponíveis

### 🚀 [QUICKSTART.md](QUICKSTART.md) — **5 minutos de startup**
Quer começar AGORA? Este é seu documento.

- ⚡ 4 terminais com comandos prontos
- ⏱️ Tempo: ~5 minutos (com tudo já instalado)
- 🎯 Cenário: Você tem Python, Node.js, SQL Server e credenciais Azure

**Start aqui se**: Você só quer executar o projeto rapidamente.

---

### 📋 [SETUP_EXECUCAO.md](SETUP_EXECUCAO.md) — **Guia completo passo a passo**
Guia detalhado com 9 fases cobrindo setup completo.

**Fases**:
1. Preparação do Ambiente Local
2. Configuração do Backend (FastAPI)
3. Configuração do Frontend (Next.js)
4. Autenticação OIDC (Entra ID)
5. Configuração do SQL Server
6. Configuração do Azure Key Vault
7. Integração com Jenkins
8. Integração com Azure DevOps
9. Observabilidade (Elastic Stack)

⏱️ Tempo: ~30-45 minutos | 🎯 Primeira vez / Setup completo | 📖 2000+ palavras

**Start aqui se**: Você precisa entender cada passo ou é primeira vez.

---

### 🔧 [SCRIPTS_SETUP.md](SCRIPTS_SETUP.md) — **Scripts prontos (automatizado)**
Coletânea de scripts PowerShell, Bash e SQL para automatizar setup.

**Includes**:
- `setup-windows.ps1` — Setup completo Windows
- `setup-unix.sh` — Setup completo Linux/macOS
- `backend-setup.sh` — Backend isolado
- `frontend-setup.sh` — Frontend isolado
- `database-setup.sql` — Schema SQL
- `docker-compose.elastic.yml` — Stack observabilidade

⏱️ Tempo: ~10-15 minutos | 🎯 Automatização / CI-CD | 🤖 Scripts prontos

**Start aqui se**: Você prefere scripts prontos ou automatizar em pipeline.

---

### 🧭 [NAVIGATION.md](NAVIGATION.md) — **Índice estruturado & matriz de decisão**
Guia de navegação entre todos os documentos com fluxos recomendados.

**Includes**:
- Matriz de decisão (qual doc para cada necessidade)
- Fluxos recomendados (novo dev, setup repetido, CI-CD, debug)
- Checklist geral
- Links úteis

⏱️ Tempo: ~5-10 minutos | 🎯 Orientação / Navegação

**Start aqui se**: Você está perdido ou quer entender qual documento usar.

---

### 🏥 [HEALTHCHECK.md](HEALTHCHECK.md) — **Validação pós-setup**
Scripts e checklists para validar que tudo está funcionando.

**Includes**:
- Health check automático (PowerShell/Bash)
- Checklist manual de validação
- Diagnóstico de problemas comuns
- Métricas de saúde
- Pre-deploy checklist

⏱️ Tempo: ~5-10 minutos | 🎯 Validação / Troubleshooting

**Start aqui se**: Setup finalizado e quer validar tudo está OK.

---

## 🗺️ Escolha Seu Caminho

```
┌─────────────────────────────────────────────────────────┐
│          Qual é sua situação?                            │
└─────────────────────────────────────────────────────────┘
        │
        ├─ "Quero executar AGORA" ⚡
        │  └─→ QUICKSTART.md (5 min)
        │
        ├─ "Primeira vez / Setup completo" 🔧
        │  └─→ SETUP_EXECUCAO.md (30 min)
        │
        ├─ "Prefiro scripts automatizados" 🤖
        │  └─→ SCRIPTS_SETUP.md (10 min)
        │
        ├─ "Estou perdido / Qual doc ler?" 🧭
        │  └─→ NAVIGATION.md (5 min)
        │
        └─ "Setup pronto, quer validar" 🏥
           └─→ HEALTHCHECK.md (5 min)
```

---

## 📊 Comparação Rápida

| Documento | Tempo | Tipo | Para |
|-----------|-------|------|-----|
| **QUICKSTART** | 5 min | Executar | Startup rápido |
| **SETUP_EXECUCAO** | 30 min | Aprender | Primeira configuração |
| **SCRIPTS_SETUP** | 10 min | Automatizar | CI/CD, scripts |
| **NAVIGATION** | 5 min | Navegar | Orientação, decisões |
| **HEALTHCHECK** | 5-10 min | Validar | Verificação pós-setup |

---

## ✅ Quick Validation (2 minutos)

Se você JÁ tem tudo setup, use este checklist rápido:

```bash
# Terminal 1: Backend
cd backend && source venv/bin/activate && uvicorn main:app --reload
# Esperado: "Application startup complete" em http://localhost:8000/docs

# Terminal 2: Frontend  
cd frontend && npm run dev
# Esperado: "compiled client and server successfully" em http://localhost:3000

# Terminal 3: Database
cd backend && alembic current
# Esperado: Migrations listadas

# Acesse:
# - http://localhost:3000 (Frontend)
# - http://localhost:8000/docs (API Swagger)
```

---

## 🎯 Fluxo Recomendado por Perfil

### 👨‍💼 **Novo Developer (First Time)**
1. [SETUP_EXECUCAO.md](SETUP_EXECUCAO.md) — Fase 1 (Pré-requisitos)
2. [SCRIPTS_SETUP.md](SCRIPTS_SETUP.md) — Execute setup script
3. [SETUP_EXECUCAO.md](SETUP_EXECUCAO.md) — Fases 4-6 (Config Entra ID + Key Vault)
4. [QUICKSTART.md](QUICKSTART.md) — Inicie 4 terminais
5. [HEALTHCHECK.md](HEALTHCHECK.md) — Valide tudo

**⏱️ Tempo total**: ~60 minutos (primeira vez + credenciais)

---

### ⚡ **Developer Experiente (Setup Repetido)**
1. [SCRIPTS_SETUP.md](SCRIPTS_SETUP.md) — Execute setup script
2. Copie `.env` e `.env.local` de colega
3. [QUICKSTART.md](QUICKSTART.md) — Inicie 4 terminais
4. [HEALTHCHECK.md](HEALTHCHECK.md) — Quick validation

**⏱️ Tempo total**: ~15 minutos

---

### 🚀 **CI/CD Pipeline**
1. [SCRIPTS_SETUP.md](SCRIPTS_SETUP.md) — Embed em workflow
2. `alembic upgrade head` — Migrations
3. `gunicorn main:app` — Backend start
4. `npm run build && npm start` — Frontend start

**⏱️ Tempo total**: ~10 minutos (automatizado)

---

### 🐛 **Troubleshooting**
1. [HEALTHCHECK.md](HEALTHCHECK.md) — Execute health check
2. [SETUP_EXECUCAO.md](SETUP_EXECUCAO.md#-troubleshooting) — Consulte seção
3. [NAVIGATION.md](NAVIGATION.md#-suporte) — Procure seu erro na matriz

---

## 🔗 Documentação Técnica

Além deste guia de execution, o projeto contém:

- **[fluxos.md](fluxos.md)** — Fluxos técnicos (Jenkins, Azure DevOps, Webhooks)
- **[epc/](epc/)** — Épicos e arquitetura
- **[adr/](adr/)** — Decisões arquiteturais registradas
- **[../project-context.md](../project-context.md)** — Contexto completo do projeto

---

## 🆘 Precisa de Ajuda?

| Situação | Referência |
|----------|-----------|
| "Qual doc ler?" | [NAVIGATION.md](NAVIGATION.md) |
| "Erro na instalação" | [SETUP_EXECUCAO.md → Troubleshooting](SETUP_EXECUCAO.md#-troubleshooting) |
| "Backend não funciona" | [HEALTHCHECK.md → Backend validation](HEALTHCHECK.md#2️⃣-backend-fastapi) |
| "Frontend não funciona" | [HEALTHCHECK.md → Frontend validation](HEALTHCHECK.md#3️⃣-frontend-nextjs) |
| "Database não conecta" | [HEALTHCHECK.md → Database validation](HEALTHCHECK.md#4️⃣-database-sql-server) |
| "Esqueço os passos" | [QUICKSTART.md](QUICKSTART.md) (resumo em 5 min) |

---

## 📁 Estrutura de Pastas

```
.copilot/docs/
├── README.md (você está aqui!)
├── QUICKSTART.md (⚡ 5 min)
├── SETUP_EXECUCAO.md (📋 30 min completo)
├── SCRIPTS_SETUP.md (🤖 scripts prontos)
├── NAVIGATION.md (🧭 índice navegável)
├── HEALTHCHECK.md (🏥 validação)
├── fluxos.md (técnico)
├── epc/ (épicos)
├── adr/ (decisões)
└── ../project-context.md (contexto)
```

---

## 🎓 Stack do Projeto

- **Backend**: Python 3.11+ + FastAPI + SQLAlchemy + Pydantic
- **Frontend**: Next.js 14+ + TypeScript + React
- **Database**: SQL Server 2019+
- **Auth**: Entra ID (OIDC)
- **Secrets**: Azure Key Vault
- **Observabilidade**: Elastic Stack (opcional)
- **CI/CD**: Jenkins + Azure DevOps

---

## 💡 Dicas Rápidas

- 📌 **Bookmark [NAVIGATION.md](NAVIGATION.md)** — Use como seu "índice principal"
- ⚡ **QUICKSTART.md em 4 abas de terminal** — Mantém aberto durante dev
- 🔐 **Nunca commite `.env` ou `.env.local`** — SEMPRE use `.env.example`
- 🐳 **Use Docker para database** — Facilita setup em nova máquina
- 📊 **Ative HEALTHCHECK regularmente** — Valida saúde do projeto

---

## 📞 Contato & Contribuições

- **Issue de setup?** Consulte [HEALTHCHECK.md](HEALTHCHECK.md)
- **Erro nos scripts?** Verifique [SCRIPTS_SETUP.md](SCRIPTS_SETUP.md)
- **Documentação desatualizada?** Atualize a versão/data em cada doc

---

## 📈 Versão & Histórico

- **Versão**: 1.0
- **Data**: 16 de fevereiro de 2026
- **Docs**: 5 guias de setup + documentação técnica

---

## ⏭️ Próximos Passos Após Setup

1. **Validar CRUD** — Criar Empresa → Ambiente → Aplicação → Instância
2. **Testar Autenticação** — Login com Entra ID
3. **Explorar API** — Testar endpoints no Swagger
4. **Setup CI/CD** — Configurar pipelines
5. **Desenvolver** — Implementar features

---

**Boa sorte! 🚀**

Para começar, escolha seu caminho acima e clique no documento correspondente.

