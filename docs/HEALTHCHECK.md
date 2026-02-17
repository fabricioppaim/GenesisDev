# Genesis - Health Check & Validação Pós-Setup

Após completar o setup, use este guia para validar que todos os componentes estão funcionando corretamente.

---

## 🏥 Health Check Automático

### Windows (PowerShell)

**Arquivo**: `scripts/healthcheck.ps1`

```powershell
Write-Host "=== Genesis Health Check ===" -ForegroundColor Green

$checks = @{
    "Python 3.11+" = { python --version | Select-String "3.1[1-9]" }
    "Node.js 18+" = { node --version | Select-String "v1[8-9]" }
    "npm 9+" = { npm --version | Select-String "^9|^10" }
    "Git" = { git --version }
    "Docker" = { docker --version }
    "SQL Server" = { sqlcmd -S localhost -Q "SELECT @@VERSION" }
}

$passed = 0
$failed = 0

foreach ($check in $checks.GetEnumerator()) {
    try {
        $result = & $check.Value | Out-String
        Write-Host "✅ $($check.Name)" -ForegroundColor Green
        $passed++
    } catch {
        Write-Host "❌ $($check.Name)" -ForegroundColor Red
        $failed++
    }
}

Write-Host "`n=== Serviços Rodando ===" -ForegroundColor Cyan

# Backend
$backendPort = Test-NetConnection -ComputerName localhost -Port 8000 -InformationLevel Quiet
if ($backendPort) {
    Write-Host "✅ Backend (8000)" -ForegroundColor Green
} else {
    Write-Host "❌ Backend (8000)" -ForegroundColor Red
}

# Frontend
$frontendPort = Test-NetConnection -ComputerName localhost -Port 3000 -InformationLevel Quiet
if ($frontendPort) {
    Write-Host "✅ Frontend (3000)" -ForegroundColor Green
} else {
    Write-Host "❌ Frontend (3000)" -ForegroundColor Red
}

# Database
try {
    sqlcmd -S localhost -Q "SELECT 1" | Out-Null
    Write-Host "✅ SQL Server (1433)" -ForegroundColor Green
} catch {
    Write-Host "❌ SQL Server (1433)" -ForegroundColor Red
}

Write-Host "`n=== Resumo ===" -ForegroundColor Cyan
Write-Host "Pré-requisitos atendidos: $passed / $($checks.Count)" -ForegroundColor Green
Write-Host "Pré-requisitos falhando: $failed / $($checks.Count)" -ForegroundColor Red
```

**Executar**:
```powershell
.\scripts\healthcheck.ps1
```

---

### Linux/macOS (Bash)

**Arquivo**: `scripts/healthcheck.sh`

```bash
#!/bin/bash

echo "=== Genesis Health Check ==="

# Array de checagens
declare -A checks

checks[Python]="python3 --version"
checks[Node.js]="node --version"
checks[npm]="npm --version"
checks[Git]="git --version"
checks[Docker]="docker --version"

passed=0
failed=0

for check in "${!checks[@]}"; do
    if eval "${checks[$check]}" &> /dev/null; then
        echo "✅ $check"
        ((passed++))
    else
        echo "❌ $check"
        ((failed++))
    fi
done

echo ""
echo "=== Serviços Rodando ==="

# Backend
if timeout 1 bash -c "echo > /dev/tcp/localhost/8000" 2>/dev/null; then
    echo "✅ Backend (8000)"
else
    echo "❌ Backend (8000)"
fi

# Frontend
if timeout 1 bash -c "echo > /dev/tcp/localhost/3000" 2>/dev/null; then
    echo "✅ Frontend (3000)"
else
    echo "❌ Frontend (3000)"
fi

# Database (SQL Server)
if command -v sqlcmd &> /dev/null; then
    if sqlcmd -S localhost -Q "SELECT 1" &> /dev/null; then
        echo "✅ SQL Server (1433)"
    else
        echo "❌ SQL Server (1433)"
    fi
else
    echo "⚠️  sqlcmd não instalado (SQL Server)"
fi

echo ""
echo "=== Resumo ==="
echo "Pré-requisitos: $passed / ${#checks[@]} ✅"
echo "Falhando: $failed / ${#checks[@]} ❌"
```

**Executar**:
```bash
chmod +x scripts/healthcheck.sh
./scripts/healthcheck.sh
```

---

## ✔️ Checklist Manual de Validação

### 1️⃣ Pré-Requisitos

```bash
# Verificar Python
python --version
# Esperado: Python 3.11.x ou superior

# Verificar Node.js
node --version && npm --version
# Esperado: v18.x ou superior, npm 9.x ou superior

# Verificar SQL Server
sqlcmd -S localhost -U sa -P <password> -Q "SELECT @@VERSION"
# Esperado: SQL Server 2019 ou superior

# Verificar Git
git --version
# Esperado: git version 2.x ou superior
```

### 2️⃣ Backend (FastAPI)

```bash
cd backend

# Validar venv
which python  # macOS/Linux
where python  # Windows
# Esperado: Caminho dentro de backend/venv

# Validar requirements instalados
pip list | grep fastapi
pip list | grep sqlalchemy
pip list | grep pydantic
# Esperado: Todas as dependências listadas

# Testar importação
python -c "import main; print(main.app)"
# Esperado: <fastapi.applications.FastAPI object...>

# Validar .env
cat .env
# Verificar: DATABASE_URL, ENTRA_ID_TENANT_ID, ENTRA_ID_CLIENT_ID existem e não vazios

# Testar migrations
alembic current
# Esperado: Vários(as) migration(s) listado(s) como "current"
```

### 3️⃣ Frontend (Next.js)

```bash
cd frontend

# Validar node_modules
ls -la node_modules | head
# Esperado: Vários pacotes listados

# Validar .env.local
cat .env.local
# Verificar: NEXT_PUBLIC_API_BASE_URL, NEXT_PUBLIC_AUTHORITY, NEXT_PUBLIC_CLIENT_ID

# Build test (opcional)
npm run build
# Esperado: Build completa sem erros (fase: compiled successfully)
```

### 4️⃣ Database (SQL Server)

```sql
-- Executar em SQL Server Management Studio (SSMS) ou sqlcmd

-- Verificar database
SELECT name FROM sys.databases WHERE name = 'genesis_dev';
-- Esperado: 1 linha retornada

-- Verificar tabelas
USE genesis_dev;
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES;
-- Esperado: Empresas, Ambientes, Aplicacoes, Instancias (ou suas variações)

-- Verificar usuário
SELECT name FROM sys.database_principals WHERE type = 'U';
-- Esperado: genesis_user (ou seu usuário) listado
```

### 5️⃣ Endpoints de API (Swagger)

Acessar: [http://localhost:8000/docs](http://localhost:8000/docs)

**Validações**:
- [ ] Página Swagger carrega
- [ ] Seções de endpoints visíveis (GET, POST, PUT, DELETE)
- [ ] Versão da API exibida
- [ ] "Try it out" básico funciona

```bash
# Testar com curl
curl -s http://localhost:8000/docs | grep -i "swagger\|openapi"
# Esperado: HTML com referências a swagger/openapi
```

### 6️⃣ Frontend (Next.js)

Acessar: [http://localhost:3000](http://localhost:3000)

**Validações**:
- [ ] Página carrega (não é 404)
- [ ] Layout base visível
- [ ] Botão de login presente
- [ ] Console não tem erros críticos (F12 → Console)

```bash
# Testar com curl
curl -I http://localhost:3000
# Esperado: HTTP 200
```

### 7️⃣ Autenticação (OIDC/Entra ID)

**Se configurado**:
1. Clique em "Login" no frontend
2. Você deve ser redirecionado para login.microsoftonline.com
3. Após login, voltará para `localhost:3000`
4. Token JWT deve estar em `localStorage` (F12 → Application → Local Storage)

```javascript
// No console do navegador (F12):
localStorage.getItem('auth_token')
// Esperado: JWT token (starts with eyJ...)
```

### 8️⃣ Azure Key Vault (Se configurado)

```bash
# Testar acesso
az keyvault secret show --vault-name <seu-vault> --name "jenkins-token"
# Esperado: Secret retornado (ou acesso negado se sem permissão)

# Testar no backend
python -c "from azure.identity import DefaultAzureCredential; print('✅ Azure Credential OK')"
```

### 9️⃣ Elastic Stack (Se configurado)

```bash
# Testar Elasticsearch
curl -u elastic:changeme http://localhost:9200/
# Esperado: JSON com versão do Elasticsearch

# Testar Kibana
curl -I http://localhost:5601
# Esperado: HTTP 200

# Testar APM Server
curl -I http://localhost:8200
# Esperado: HTTP 200 ou 404 (mas servidor rodando)
```

---

## 📊 Resultado Esperado

Após setup bem-sucedido, você deve ter:

```
✅ Pré-requisitos
  ✓ Python 3.11+
  ✓ Node.js 18+
  ✓ npm 9+
  ✓ Git
  ✓ SQL Server 2019+

✅ Backend
  ✓ http://localhost:8000 respondendo
  ✓ http://localhost:8000/docs acessível
  ✓ API retorna JSON válido
  ✓ Migrations executadas

✅ Frontend
  ✓ http://localhost:3000 respondendo
  ✓ Página carrega sem erros
  ✓ .env.local configurado
  ✓ Console sem erros críticos

✅ Database
  ✓ genesis_dev criado
  ✓ Tabelas base criadas
  ✓ Conexão testada

✅ Segurança
  ✓ Entra ID aplicações registradas
  ✓ Azure Key Vault acessível
  ✓ Segredos armazenados

✅ (Opcional) Observabilidade
  ✓ Elasticsearch rodando
  ✓ Kibana acessível
  ✓ APM Server rodando
```

---

## 🐛 Diagnóstico de Problemas

### Backend não responde em 8000

```bash
# Verificar se processo está rodando
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # macOS/Linux

# Matar processo
taskkill /PID <PID> /F        # Windows
kill -9 <PID>                 # macOS/Linux

# Reiniciar
cd backend && source venv/bin/activate && uvicorn main:app --reload
```

### Frontend não conecta backend

```bash
# Verificar .env.local
cat frontend/.env.local
# NEXT_PUBLIC_API_BASE_URL deve ser: http://localhost:8000

# Verificar CORS no backend
# Em backend main.py, deve ter:
# CORSMiddleware com: allow_origins=["http://localhost:3000"]

# Testar conexão
curl -H "Origin: http://localhost:3000" http://localhost:8000/
# Esperado: Access-Control-Allow-Origin header presente
```

### Database não conecta

```bash
# Verificar DATABASE_URL
cat backend/.env | grep DATABASE_URL

# Testar conexão
sqlcmd -S localhost -U genesis_user -P <password> -d genesis_dev -Q "SELECT 1"

# Verificar SQL Server status
docker ps | grep mssql           # Se usando Docker
# Ou verificar em Services (Windows)

# Reiniciar SQL Server
# Windows: Get-Service MSSQLSERVER | Restart-Service
# Docker: docker restart <container-id>
```

### OIDC não funciona

```bash
# Verificar Entra ID configuração
cat backend/.env | grep ENTRA

# Testar discovery URL
curl "https://login.microsoftonline.com/<TENANT_ID>/v2.0/.well-known/openid-configuration" | jq .

# Verificar aplicação registrada no Entra ID
# Azure Portal → Entra ID → Registros de Aplicações → Sua App
# Verificar: Client ID, Tenant ID, Redirect URIs

# No frontend .env.local
cat frontend/.env.local | grep NEXT_PUBLIC
# Deve ter AUTHORITY e CLIENT_ID corretos
```

---

## 📈 Métricas de Saúde

Execute este teste full-cycle:

```bash
#!/bin/bash

echo "=== Genesis Full Test ==="

# 1. Backend health
echo "1. Backend..."
BACKEND=$(curl -s http://localhost:8000/healthz || echo "FAIL")
[[ $BACKEND == *"ok"* ]] && echo "✅ Backend" || echo "❌ Backend"

# 2. Frontend health
echo "2. Frontend..."
FRONTEND=$(curl -s http://localhost:3000 | grep -c "<!DOCTYPE")
[[ $FRONTEND -gt 0 ]] && echo "✅ Frontend" || echo "❌ Frontend"

# 3. Database health
echo "3. Database..."
DB=$(sqlcmd -S localhost -Q "SELECT 1" 2>&1)
[[ $DB == *"1"* ]] && echo "✅ Database" || echo "❌ Database"

# 4. API endpoints
echo "4. API Endpoints..."
curl -s http://localhost:8000/api/empresas | grep -q "\[" && echo "✅ GET /api/empresas" || echo "❌ GET /api/empresas"

echo ""
echo "✅ Full test complete!"
```

---

## ✔️ Pre-Deploy Checklist

Antes de fazer deploy para staging/produção:

- [ ] Todos os checks acima vermelho verde
- [ ] Testes unitários passando: `pytest tests/`
- [ ] Testes frontend passando: `npm test`
- [ ] Linting sem erros: `pylint backend/` e `npm run lint`
- [ ] Build frontend OK: `npm run build` sem erros
- [ ] Migrations OK: `alembic upgrade head`
- [ ] Variáveis de ambiente verificadas (sem secrets em código)
- [ ] Logs estruturados funcionando
- [ ] CORS configurado para domínio de produção
- [ ] HTTPS configurado (OIDC requer HTTPS em prod)

---

## 📞 Problemas Persistentes?

1. **Ler sec. Troubleshooting**: [SETUP_EXECUCAO.md](SETUP_EXECUCAO.md#-troubleshooting)
2. **Consultar fluxos**: [fluxos.md](fluxos.md)
3. **Verificar ADRs**: [adr/](adr/)
4. **Logs detalhados**: Habilitar `DEBUG=True` em `.env`

---

**Última atualização**: 16 de fevereiro de 2026  
**Versão**: 1.0

