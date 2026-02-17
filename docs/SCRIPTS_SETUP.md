# Genesis - Scripts de Setup

Coletânea de scripts prontos para executar cada fase do setup.

---

## 📋 Índice de Scripts

1. [Setup Completo (Windows)](#setup-completo-windows)
2. [Setup Completo (macOS/Linux)](#setup-completo-macos--linux)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [Database Setup](#database-setup)
6. [Docker/Observabilidade Setup](#dockerobservabilidade-setup)

---

## Setup Completo (Windows)

**Arquivo**: `scripts\setup-windows.ps1`

```powershell
# Execute como Administrator:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Write-Host "=== Genesis Setup (Windows) ===" -ForegroundColor Green

# 1. Criar diretórios
Write-Host "`n[1/6] Criando estrutura de diretórios..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path "backend\logs" -Force | Out-Null
New-Item -ItemType Directory -Path "frontend\public" -Force | Out-Null
New-Item -ItemType Directory -Path "infrastructure" -Force | Out-Null

# 2. Backend - Python venv
Write-Host "`n[2/6] Configurando Backend (FastAPI)..." -ForegroundColor Cyan
Push-Location backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Criar .env
$envContent = @"
DATABASE_URL=mssql+pyodbc://sa:SenhaForte123@localhost:1433/genesis_dev?driver=ODBC+Driver+17+for+SQL+Server
ENTRA_ID_TENANT_ID=UPDATE_ME
ENTRA_ID_CLIENT_ID=UPDATE_ME
ENTRA_ID_CLIENT_SECRET=UPDATE_ME
AZURE_KEYVAULT_URL=https://UPDATE_ME.vault.azure.net/
JENKINS_TOKEN=UPDATE_ME
AZURE_DEVOPS_PAT=UPDATE_ME
ELASTIC_APM_SERVER_URL=http://localhost:8200
DEBUG=True
"@
Set-Content -Path ".env" -Value $envContent
Write-Host ".env criado. ATUALIZE com suas credenciais!" -ForegroundColor Yellow
Pop-Location

# 3. Database - SQL Server
Write-Host "`n[3/6] Preparando Banco de Dados..." -ForegroundColor Cyan
$sqlCreateDb = @"
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'genesis_dev')
BEGIN
    CREATE DATABASE genesis_dev;
    PRINT 'Database genesis_dev criado.';
END
GO

USE genesis_dev;
GO

-- Verificar se usuário existe
IF NOT EXISTS (SELECT * FROM sys.server_principals WHERE name = 'genesis_user')
BEGIN
    CREATE LOGIN genesis_user WITH PASSWORD = 'SenhaForte123!';
    PRINT 'Login genesis_user criado.';
END
GO

USE genesis_dev;
IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'genesis_user')
BEGIN
    CREATE USER genesis_user FOR LOGIN genesis_user;
    ALTER ROLE db_owner ADD MEMBER genesis_user;
    PRINT 'User genesis_user criado com permissões.';
END
GO
"@

$sqlCreateDb | sqlcmd -S localhost -U sa -P SenhaForte123 -No
Write-Host "Database preparado (verifique credenciais)." -ForegroundColor Green

# 4. Frontend - Node.js
Write-Host "`n[4/6] Configurando Frontend (Next.js)..." -ForegroundColor Cyan
Push-Location frontend
npm install

# Criar .env.local
$envFrontend = @"
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_AUTHORITY=https://login.microsoftonline.com/UPDATE_ME/v2.0
NEXT_PUBLIC_CLIENT_ID=UPDATE_ME
NEXT_PUBLIC_REDIRECT_URI=http://localhost:3000/auth/callback
"@
Set-Content -Path ".env.local" -Value $envFrontend
Write-Host ".env.local criado. ATUALIZE com suas credenciais!" -ForegroundColor Yellow
Pop-Location

# 5. Git
Write-Host "`n[5/6] Configurando Git..." -ForegroundColor Cyan
git config core.autocrlf true
Write-Host "Git configurado (CRLF)." -ForegroundColor Green

# 6. Resumo
Write-Host "`n[6/6] Setup Completo!" -ForegroundColor Green
Write-Host "`n✅ Próximas etapas:" -ForegroundColor Green
Write-Host "  1. ATUALIZE .env com credenciais do Entra ID, Key Vault e Jenkins"
Write-Host "  2. ATUALIZE .env.local com credenciais Entra ID"
Write-Host "  3. Execute: cd backend && .\venv\Scripts\activate && alembic upgrade head"
Write-Host "  4. Terminal 1: cd backend && uvicorn main:app --reload"
Write-Host "  5. Terminal 2: cd frontend && npm run dev"
Write-Host "  6. Acesse: http://localhost:3000"
```

**Executar**:
```powershell
.\scripts\setup-windows.ps1
```

---

## Setup Completo (macOS / Linux)

**Arquivo**: `scripts/setup-unix.sh`

```bash
#!/bin/bash

echo "=== Genesis Setup (macOS/Linux) ==="

# 1. Criar diretórios
echo -e "\n[1/6] Criando estrutura de diretórios..."
mkdir -p backend/logs
mkdir -p frontend/public
mkdir -p infrastructure

# 2. Backend - Python venv
echo -e "\n[2/6] Configurando Backend (FastAPI)..."
cd backend || exit
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Criar .env
cat > .env <<EOF
DATABASE_URL=mssql+pyodbc://sa:SenhaForte123@localhost:1433/genesis_dev?driver=ODBC+Driver+17+for+SQL+Server
ENTRA_ID_TENANT_ID=UPDATE_ME
ENTRA_ID_CLIENT_ID=UPDATE_ME
ENTRA_ID_CLIENT_SECRET=UPDATE_ME
AZURE_KEYVAULT_URL=https://UPDATE_ME.vault.azure.net/
JENKINS_TOKEN=UPDATE_ME
AZURE_DEVOPS_PAT=UPDATE_ME
ELASTIC_APM_SERVER_URL=http://localhost:8200
DEBUG=True
EOF
echo ".env criado. ATUALIZE com suas credenciais!"
cd ..

# 3. Database - SQL Server
echo -e "\n[3/6] Preparando Banco de Dados..."
cat > /tmp/genesis_setup.sql <<'EOF'
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'genesis_dev')
BEGIN
    CREATE DATABASE genesis_dev;
    PRINT 'Database genesis_dev criado.';
END
GO
EOF
echo "SQL prep file criado em /tmp/genesis_setup.sql"

# 4. Frontend - Node.js
echo -e "\n[4/6] Configurando Frontend (Next.js)..."
cd frontend || exit
npm install

# Criar .env.local
cat > .env.local <<EOF
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_AUTHORITY=https://login.microsoftonline.com/UPDATE_ME/v2.0
NEXT_PUBLIC_CLIENT_ID=UPDATE_ME
NEXT_PUBLIC_REDIRECT_URI=http://localhost:3000/auth/callback
EOF
echo ".env.local criado. ATUALIZE com suas credenciais!"
cd ..

# 5. Git
echo -e "\n[5/6] Configurando Git..."
git config core.autocrlf input
echo "Git configurado (LF)."

# 6. Resumo
echo -e "\n[6/6] Setup Completo! ✅"
echo -e "\n✅ Próximas etapas:"
echo "  1. ATUALIZE backend/.env com credenciais"
echo "  2. ATUALIZE frontend/.env.local com credenciais"
echo "  3. Execute: cd backend && source venv/bin/activate && alembic upgrade head"
echo "  4. Terminal 1: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "  5. Terminal 2: cd frontend && npm run dev"
echo "  6. Acesse: http://localhost:3000"
```

**Executar**:
```bash
chmod +x scripts/setup-unix.sh
./scripts/setup-unix.sh
```

---

## Backend Setup

**Arquivo**: `scripts/backend-setup.sh` (ou `.ps1` Windows)

```bash
#!/bin/bash

cd backend || exit 1

echo "=== Backend Setup ==="

# Criar venv
python3 -m venv venv
source venv/bin/activate

# Instalar deps
pip install --upgrade pip
pip install -r requirements.txt

# Migrations
echo "Executando migrations..."
alembic upgrade head

echo "✅ Backend ready! Execute: uvicorn main:app --reload"
```

---

## Frontend Setup

**Arquivo**: `scripts/frontend-setup.sh`

```bash
#!/bin/bash

cd frontend || exit 1

echo "=== Frontend Setup ==="

# Instalar deps
npm install

# Build (opcional)
npm run build

echo "✅ Frontend ready! Execute: npm run dev"
```

---

## Database Setup

**Arquivo**: `scripts/database-setup.sql`

```sql
-- Execute no SQL Server Management Studio (SSMS) conectado como administrador

-- 1. Criar database
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'genesis_dev')
BEGIN
    CREATE DATABASE genesis_dev;
    PRINT 'Database genesis_dev criado.';
END
GO

-- 2. Usar database
USE genesis_dev;
GO

-- 3. Criar login (se não existir)
IF NOT EXISTS (SELECT * FROM sys.server_principals WHERE name = 'genesis_user')
BEGIN
    CREATE LOGIN genesis_user WITH PASSWORD = 'SenhaForte123!';
    PRINT 'Login genesis_user criado.';
END
GO

-- 4. Criar user
IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'genesis_user')
BEGIN
    CREATE USER genesis_user FOR LOGIN genesis_user;
    ALTER ROLE db_owner ADD MEMBER genesis_user;
    PRINT 'User genesis_user criado.';
END
GO

-- 5. Tabelas base (exemplo - substituir por suas migrações):
CREATE TABLE [Empresas] (
    [Id] UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    [Nome] NVARCHAR(255) NOT NULL,
    [Ativo] BIT DEFAULT 1,
    [CriadoEm] DATETIME2 DEFAULT GETUTCDATE(),
    [AlteradoEm] DATETIME2 DEFAULT GETUTCDATE()
);

CREATE TABLE [Ambientes] (
    [Id] UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    [EmpresaId] UNIQUEIDENTIFIER NOT NULL,
    [Nome] NVARCHAR(50) NOT NULL,
    [Tipo] NVARCHAR(20) NOT NULL, -- PRD, HLG, DEV, TST, SANDBOX
    [Ativo] BIT DEFAULT 1,
    [CriadoEm] DATETIME2 DEFAULT GETUTCDATE(),
    [AlteradoEm] DATETIME2 DEFAULT GETUTCDATE(),
    FOREIGN KEY ([EmpresaId]) REFERENCES [Empresas]([Id]),
    UNIQUE([EmpresaId], [Nome])
);

CREATE TABLE [Aplicacoes] (
    [Id] UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    [Nome] NVARCHAR(255) NOT NULL,
    [Descricao] NVARCHAR(MAX),
    [Ativo] BIT DEFAULT 1,
    [CriadoEm] DATETIME2 DEFAULT GETUTCDATE(),
    [AlteradoEm] DATETIME2 DEFAULT GETUTCDATE()
);

CREATE TABLE [Instancias] (
    [Id] UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    [AplicacaoId] UNIQUEIDENTIFIER NOT NULL,
    [EmpresaId] UNIQUEIDENTIFIER NOT NULL,
    [AmbienteId] UNIQUEIDENTIFIER NOT NULL,
    [Nome] NVARCHAR(255) NOT NULL,
    [Ativo] BIT DEFAULT 1,
    [CriadoEm] DATETIME2 DEFAULT GETUTCDATE(),
    [AlteradoEm] DATETIME2 DEFAULT GETUTCDATE(),
    FOREIGN KEY ([AplicacaoId]) REFERENCES [Aplicacoes]([Id]),
    FOREIGN KEY ([EmpresaId]) REFERENCES [Empresas]([Id]),
    FOREIGN KEY ([AmbienteId]) REFERENCES [Ambientes]([Id]),
    UNIQUE([AplicacaoId], [EmpresaId], [AmbienteId])
);

PRINT 'Schema base criado com sucesso!';
```

---

## Docker/Observabilidade Setup

**Arquivo**: `infrastructure/docker-compose.elastic.yml`

```yaml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.10.0
    container_name: genesis-elasticsearch
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=true
      - ELASTIC_PASSWORD=changeme
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data
    networks:
      - genesis-network

  kibana:
    image: docker.elastic.co/kibana/kibana:8.10.0
    container_name: genesis-kibana
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
      - ELASTICSEARCH_USERNAME=elastic
      - ELASTICSEARCH_PASSWORD=changeme
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
    networks:
      - genesis-network

  apm-server:
    image: docker.elastic.co/apm/apm-server:8.10.0
    container_name: genesis-apm-server
    cap_add: ["CHOWN", "DAC_OVERRIDE", "SETFCAP", "SETGID", "SETUID"]
    cap_drop: ["ALL"]
    ports:
      - "8200:8200"
    environment:
      - apm-server.host=0.0.0.0:8200
      - apm-server.auth.api_key.enabled=false
      - setup.kibana.host=kibana:5601
      - output.elasticsearch.hosts=["elasticsearch:9200"]
      - output.elasticsearch.username=elastic
      - output.elasticsearch.password=changeme
    depends_on:
      - elasticsearch
      - kibana
    networks:
      - genesis-network

volumes:
  elasticsearch-data:
    driver: local

networks:
  genesis-network:
    driver: bridge
```

**Executar**:
```bash
docker-compose -f infrastructure/docker-compose.elastic.yml up -d
# Acessar Kibana: http://localhost:5601
# Acessar APM Server: http://localhost:8200
```

---

## 📋 Checklist de Execução

- [ ] **Windows**: `.\scripts\setup-windows.ps1` executado sem erros
- [ ] **Linux/macOS**: `./scripts/setup-unix.sh` executado sem erros
- [ ] `.env` criado e atualizado com credenciais
- [ ] `.env.local` criado e atualizado com credenciais
- [ ] SQL Server database criado
- [ ] Python venv ativado
- [ ] Migrations executadas: `alembic upgrade head`
- [ ] Backend rodando: `uvicorn main:app --reload`
- [ ] Frontend rodando: `npm run dev`
- [ ] Ambos acessíveis: http://localhost:3000 e http://localhost:8000/docs

---

## 🆘 Troubleshooting

| Erro | Causa | Solução |
|------|-------|---------|
| "venv command not found" | Python não no PATH | Instalar Python 3.11+ |
| "ModuleNotFoundError" | Venv não ativado | `source venv/bin/activate` or `.\venv\Scripts\activate` |
| "Connection refused" DB | SQL Server não rodando | Iniciar SQL Server / Docker |
| "Port 8000 already in use" | Outro processo | Matar processo em port 8000 |
| ".env not found" | .env não criado | Copiar de `.env.example` ou criar manualmente |

