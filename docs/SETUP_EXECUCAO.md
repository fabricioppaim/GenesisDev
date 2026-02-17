# Genesis - Guia de Setup e Execução

## 📋 Pré-Requisitos

### Sistemas Operacionais
- **Windows 11+** ou **macOS 12+** ou **Linux (Ubuntu 22.04+)**

### Softwares Obrigatórios
- **Python 3.11+** ([python.org](https://www.python.org/))
- **Node.js 18+** e **npm 9+** ([nodejs.org](https://nodejs.org/))
- **SQL Server 2019+** ou **SQL Server Express** ([microsoft.com/sql-server](https://www.microsoft.com/sql-server))
- **Git** ([git-scm.com](https://git-scm.com/))
- **Azure CLI** (para integração com Azure Key Vault) ([learn.microsoft.com](https://learn.microsoft.com/pt-br/cli/azure/)) *(Opcional, mas recomendado)*

### Contas/Serviços Externos
- **Azure Entra ID** tenant com aplicação OIDC registrada (para autenticação SSO)
- **Azure Key Vault** (para armazenamento de segredos)
- **Jenkins** (instância acessível para integrações de pipeline)
- **Azure DevOps** (para integrações de releases)

---

## 🎯 Fase 1: Preparação do Ambiente Local

### 1.1 Clonar o Repositório
```bash
cd c:\Repositorios
git clone <repo-url> GenesisDev
cd GenesisDev
```

### 1.2 Validar Versões Instaladas
```bash
# Python
python --version  # Esperado: 3.11+

# Node.js
node --version
npm --version    # Esperado: npm 9+

# Git
git --version

# SQL Server (verificar via SQL Server Management Studio ou sqlcmd)
sqlcmd -S localhost -Q "SELECT @@version"
```

---

## 🔧 Fase 2: Configuração do Backend (FastAPI)

### 2.1 Criar Virtual Environment Python
```bash
cd backend/  # ou conforme a estrutura do projeto
python -m venv venv

# Ativar virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2.2 Instalar Dependências Python
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
# Se houver requirements-dev.txt para ambiente de desenvolvimento:
pip install -r requirements-dev.txt
```

### 2.3 Configurar Variáveis de Ambiente
Criar arquivo `.env` na raiz do backend com as variáveis necessárias:

```env
# Database
DATABASE_URL=mssql+pyodbc://user:password@localhost:1433/genesis_dev?driver=ODBC+Driver+17+for+SQL+Server

# Entra ID / OIDC
ENTRA_ID_TENANT_ID=<seu-tenant-id>
ENTRA_ID_CLIENT_ID=<sua-app-id>
ENTRA_ID_CLIENT_SECRET=<seu-client-secret>
OIDC_DISCOVERY_URL=https://login.microsoftonline.com/<seu-tenant-id>/v2.0/.well-known/openid-configuration

# Azure Key Vault
AZURE_KEYVAULT_URL=https://<seu-vault>.vault.azure.net/

# Jenkins
JENKINS_BASE_URL=https://<seu-jenkins>/
JENKINS_TOKEN=<token-do-jenkins>  # Alternativa: buscar via Key Vault

# Azure DevOps
AZURE_DEVOPS_ORG_URL=https://dev.azure.com/<sua-org>/
AZURE_DEVOPS_PAT=<seu-pat>  # Alternativa: buscar via Key Vault

# Elastic Stack (Observabilidade)
ELASTIC_APM_SERVICE_NAME=genesis-backend
ELASTIC_APM_SERVER_URL=http://localhost:8200

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False  # True para desenvolvimento
```

### 2.4 Executar Migrations do Banco de Dados
```bash
# Exemplo com Alembic (se configurado)
alembic upgrade head

# Ou executar script SQL manualmente:
# sqlcmd -S localhost -U sa -P <password> -d genesis_dev -i schema.sql
```

### 2.5 Iniciar Backend (Desenvolvimento)
```bash
# Com hot-reload (uvicorn)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Ou com gunicorn (produção):
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

✅ **Verificar**: Acessar [http://localhost:8000/docs](http://localhost:8000/docs) para validar Swagger/OpenAPI.

---

## 🎨 Fase 3: Configuração do Frontend (Next.js)

### 3.1 Instalar Dependências Node
```bash
cd frontend/
npm install
# Ou com yarn/pnpm:
yarn install
pnpm install
```

### 3.2 Configurar Variáveis de Ambiente
Criar arquivo `.env.local` na raiz do frontend:

```env
# API Backend
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

# Entra ID / OIDC
NEXT_PUBLIC_AUTHORITY=https://login.microsoftonline.com/<seu-tenant-id>/v2.0
NEXT_PUBLIC_CLIENT_ID=<sua-app-id-frontend>
NEXT_PUBLIC_REDIRECT_URI=http://localhost:3000/auth/callback  # Ajustar conforme ambiente

# Feature flags (opcional)
NEXT_PUBLIC_ENABLE_AUDIT_UI=true
NEXT_PUBLIC_ENABLE_PIPELINE_UI=true
```

### 3.3 Iniciar Frontend (Desenvolvimento)
```bash
npm run dev
# Ou:
yarn dev
pnpm dev
```

✅ **Verificar**: Acessar [http://localhost:3000](http://localhost:3000) para validar.

---

## 🔐 Fase 4: Autenticação OIDC (Entra ID)

### 4.1 Registrar Aplicação no Entra ID (Portal Azure)
1. Navegue para **Azure AD → Registros de aplicações**
2. Clique em **Novo Registro**
3. Configure:
   - **Nome**: Genesis CMDB Backend (ou similar)
   - **Tipos suportados**: Accounts in any organizational directory
   - **Redirect URI**: (deixar em branco por enquanto)
4. Após criar, anote **Client ID** e **Tenant ID**
5. Em **Certificados e segredos**, crie um novo segredo para backend
6. Adicione segredo no Azure Key Vault

### 4.2 Registrar Aplicação Frontend
Repetir processo para aplicação frontend com:
- **Redirect URI**: `http://localhost:3000/auth/callback` (dev) e URLs de produção

### 4.3 Configurar Permissões de API
1. Em ambas as aplicações, vá para **Permissões de API**
2. Adicione **Microsoft Graph**:
   - `openid`, `profile`, `email` (delegadas)
3. Conceder consentimento do administrador

---

## 💾 Fase 5: Configuração do SQL Server

### 5.1 Criar Banco de Dados
```sql
-- Conectar como admin
CREATE DATABASE genesis_dev;
GO

USE genesis_dev;
GO

-- Criar usuário (se necessário)
CREATE LOGIN genesis_user WITH PASSWORD = 'SenhaForte123!';
CREATE USER genesis_user FOR LOGIN genesis_user;
ALTER ROLE db_owner ADD MEMBER genesis_user;
GO
```

### 5.2 Executar Schema Inicial
```bash
# Exemplo com migrations (Alembic):
alembic upgrade head

# Ou manualmente via SQL Server Management Studio (SSMS):
# 1. Conectar ao servidor
# 2. Executar scripts em: backend/migrations/versions/
```

---

## 🔐 Fase 6: Configuração do Azure Key Vault

### 6.1 Crear Key Vault no Azure
```bash
az keyvault create --resource-group <seu-rg> --name <seu-vault> --location eastus
```

### 6.2 Armazenar Segredos
```bash
az keyvault secret set --vault-name <seu-vault> --name "jenkins-token" --value "<token>"
az keyvault secret set --vault-name <seu-vault> --name "azure-devops-pat" --value "<pat>"
az keyvault secret set --vault-name <seu-vault> --name "database-password" --value "<password>"
```

### 6.3 Configurar Acesso (IAM)
1. No portal Azure, abra Key Vault
2. **Access Control (IAM)** → **Add Role Assignment**
3. Atribua `Key Vault Secrets User` ao seu usuário ou aplicação

---

## 🔌 Fase 7: Integração com Jenkins (Opcional)

### 7.1 Gerar Token de Acesso Jenkins
1. No Jenkins, aceda a **Manage Jenkins → Security → API Tokens**
2. Gere um novo token
3. Armazene no Azure Key Vault:
```bash
az keyvault secret set --vault-name <seu-vault> --name "jenkins-token" --value "<token>"
```

### 7.2 Testar Webhook Callback
Após configurar Jenkins com Outbound WebHook plugin:

```bash
# Testar endpoint webhook local (usar ngrok para tunelar):
ngrok http 8000

# Configurar Jenkins para enviar callbacks para:
# https://<seu-ngrok-url>/api/webhooks/jenkins
```

---

## 🚀 Fase 8: Integração com Azure DevOps (Opcional)

### 8.1 Gerar PAT (Personal Access Token)
1. No Azure DevOps, vá para **User Settings → Personal Access Tokens**
2. Crie novo token com:
   - **Scopes**: Build (Read & Execute), Release (Read & Execute)
3. Armazene no Azure Key Vault:
```bash
az keyvault secret set --vault-name <seu-vault> --name "azure-devops-pat" --value "<pat>"
```

### 8.2 Configurar Service Hooks
1. No Azure DevOps, vá para **Project Settings → Service Hooks**
2. Crie novo webhook para eventos de build/release
3. Configure endpoint:
```
https://<seu-dominio>/api/webhooks/azure-devops
```

---

## 📊 Fase 9: Observabilidade (Elastic Stack - Opcional)

### 9.1 Iniciar Elastic Stack (Docker)
```bash
docker-compose -f infrastructure/docker-compose.elastic.yml up -d
```

Assumindo um arquivo `docker-compose.elastic.yml` com:
```yaml
version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.x
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=true
      - ELASTIC_PASSWORD=changeme
    ports:
      - "9200:9200"
  
  kibana:
    image: docker.elastic.co/kibana/kibana:8.x
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
```

### 9.2 Validar Conexão
- Acessar Kibana: [http://localhost:5601](http://localhost:5601)
- Backend deve enviar logs estruturados

---

## ✅ Checklist de Execução

### Backend
- [ ] Virtual environment criado e ativado
- [ ] Dependências pip instaladas
- [ ] `.env` configurado com todas as variáveis
- [ ] SQL Server acessível e banco criado
- [ ] Migrations executadas
- [ ] API inicia sem erros em `http://localhost:8000`
- [ ] Swagger acessível em `/docs`

### Frontend
- [ ] `npm install` executado sem erros
- [ ] `.env.local` configurado
- [ ] Aplicação inicia em `http://localhost:3000`
- [ ] Login OIDC funciona

### Integração
- [ ] Azure Entra ID configurado
- [ ] Azure Key Vault acessível
- [ ] Jenkins webhook testado (se aplicável)
- [ ] Azure DevOps webhook testado (se aplicável)

### Observabilidade
- [ ] Elasticsearch/Kibana rodando (se aplicável)
- [ ] Logs sendo capturados no backend

---

## 🐛 Troubleshooting

### Erro: `ModuleNotFoundError` no Backend
```bash
# Verificar se virtual environment está ativo:
which python  # macOS/Linux
where python  # Windows

# Reinstalar dependências:
pip install -r requirements.txt --force-reinstall
```

### Erro: `Connection refused` no SQL Server
```bash
# Verificar se SQL Server está rodando:
# Windows: Services → SQL Server (MSSQLSERVER)
# macOS/Docker: verificar container

# Testar conexão:
sqlcmd -S localhost -U sa -P <password> -Q "SELECT 1"
```

### Erro: `Invalid CORS origin` no Frontend
```
# Backend está bloqueando requisições do frontend.
# Adicionar em backend .env:
CORS_ORIGINS=http://localhost:3000

# Verificar configuração CORS em fastapi main.py:
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGINS", "").split(",")],
    ...
)
```

### Erro: `OIDC discovery URL not reachable`
```bash
# Verificar internet e acesso a Entra ID:
curl https://login.microsoftonline.com/<tenant-id>/v2.0/.well-known/openid-configuration

# Verificar ENTRA_ID_TENANT_ID e ENTRA_ID_CLIENT_ID
```

---

## 📚 Documentos Relacionados

- [Fluxos de Execução](fluxos.md) — Detalhes de disparar Jenkins e Azure DevOps
- [ADR: Webhook Receiver separado com Auth OIDC](adr/ADR-B-003-Webhook-Receiver-separado-Auth-OIDC.md)
- [EPIC: Fundação do Domínio](epc/EPC-A-001%20—%20Fundação%20do%20Domínio%20(SQL%20Server%20+%20FastAPI%20+%20Next.js).md)

---

## 🎓 Próximos Passos

1. **Desenvolvimento**: Implementar endpoints iniciais de CRUD (Empresa, Ambiente, Aplicação, Instância)
2. **Auditoria**: Configurar triggers SQL e listeners de eventos para rastreamento
3. **RBAC**: Implementar autorização baseada em roles por empresa/ambiente
4. **Testes**: Adicionar testes unitários e de integração
5. **Deploy**: Criar pipelines CI/CD com Azure DevOps ou GitHub Actions

---

**Última atualização**: 16 de fevereiro de 2026  
**Versão**: 1.0
