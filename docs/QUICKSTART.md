# Genesis - Quick Start Execution

## 🚀 Startup Rápido (5 minutos)

### Pré-requisitos: Já tem tudo instalado?
```bash
# Teste rapidamente:
python --version && node --version && npm --version
sqlcmd -S localhost -Q "SELECT @@VERSION"  # SQL Server deve estar rodando
```

---

## 1️⃣ Terminal 1: Backend FastAPI

```bash
# Entrar no backend
cd backend/

# Ativar virtual environment (Windows)
venv\Scripts\activate

# Ativar virtual environment (macOS/Linux)
source venv/bin/activate

# Instalar dependências (primeira vez)
pip install -r requirements.txt

# Rodar servidor FastAPI
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**✅ Status**: Acessar [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 2️⃣ Terminal 2: Frontend Next.js

```bash
# Entrar no frontend
cd frontend/

# Instalar dependências (primeira vez apenas)
npm install

# Rodar servidor de desenvolvimento
npm run dev
```

**✅ Status**: Acessar [http://localhost:3000](http://localhost:3000)

---

## 3️⃣ Terminal 3: SQL Server (Migrations)

```bash
# Primeira vez: criar banco e schema
cd backend/

# Ativar virtual environment
# (Windows) venv\Scripts\activate
# (macOS/Linux) source venv/bin/activate

# Executar migrations
alembic upgrade head

# Verificar status
alembic current
```

---

## 4️⃣ (Opcional) Terminal 4: Elastic Stack

```bash
# Se usar Docker:
docker-compose -f infrastructure/docker-compose.elastic.yml up -d

# Acessar Kibana: https://localhost:5601
```

---

## 📋 Checklist Rápido

| Componente | URL | Status |
|-----------|-----|--------|
| Backend (FastAPI) | [http://localhost:8000](http://localhost:8000) | ✅ Rodando? |
| Swagger/OpenAPI | [http://localhost:8000/docs](http://localhost:8000/docs) | ✅ Documentado? |
| Frontend (Next.js) | [http://localhost:3000](http://localhost:3000) | ✅ Rodando? |
| Kibana (Elastic) | [http://localhost:5601](http://localhost:5601) | ✅ Opcional |
| SQL Server | localhost:1433 | ✅ Conectado? |

---

## 🔧 Variáveis de Ambiente Essenciais

**Backend** (`.env` na raiz backend):
```env
DATABASE_URL=mssql+pyodbc://sa:password@localhost:1433/genesis_dev?driver=ODBC+Driver+17+for+SQL+Server
ENTRA_ID_TENANT_ID=xxxxx
ENTRA_ID_CLIENT_ID=xxxxx
AZURE_KEYVAULT_URL=https://vault.azure.net/
DEBUG=True
```

**Frontend** (`.env.local` na raiz frontend):
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_AUTHORITY=https://login.microsoftonline.com/xxxxx/v2.0
NEXT_PUBLIC_CLIENT_ID=xxxxx
```

---

## 🐛 Problemas Comuns

| Problema | Solução |
|----------|---------|
| `ModuleNotFoundError` | `pip install -r requirements.txt` no venv ativado |
| Backend não conecta DB | Verificar `DATABASE_URL` em `.env` e se SQL Server está rodando |
| Frontend não carrega | Verificar `NEXT_PUBLIC_API_BASE_URL` em `.env.local` |
| Porta 8000 já em uso | `netstat -ano \| findstr :8000` (Windows) e matar processo |
| CORS error | Adicionar frontend URL em `CORS_ORIGINS` backend |

---

## 📝 Fluxo de Desenvolvimento

```
1. Editar código backend → uvicorn recarrega automaticamente
2. Editar código frontend → Next.js recarrega automaticamente
3. Editar migrations → alembic upgrade head
4. Testar APIs → Swagger http://localhost:8000/docs
5. Testar frontend → Acessar http://localhost:3000
```

---

## 🎯 Próximas Etapas

Após startup bem-sucedido:

1. **Login OIDC**: Testar autenticação no frontend
2. **CRUD Básico**: Criar Empresa → Ambiente → Aplicação → Instância
3. **Auditoria**: Verificar logs em SQL Server / Kibana
4. **Webhooks**: Configurar Jenkins/Azure DevOps (se aplicável)

---

**Tempo estimado de setup**: 5-10 minutos (com tudo já instalado)

