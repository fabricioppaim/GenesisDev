1) TICKET A1 — Definir Glossário + Convenções de Nomes
Descrição: Criar docs/glossary.md com termos oficiais e naming.
Aceite:

Termos: Company, Environment, Application, Instance, Resource, DbServer, Database, Datastore, Profile, Template, SecretRef, PipelineRun.
Definir padrão de nomes (ex.: camelCase no front, snake_case no back; ou mapeamento via DTO).

Prompt Copilot:
Crie um documento docs/glossary.md com definições curtas e exemplos práticos para Company, Environment, Application, Instance (1 company/1 env + purpose), Resource (IIS host/proxy), DbServer/Database/Datastore, Profiles/Templates, SecretRef e PipelineRun. Inclua convenções de naming e exemplos de nomenclatura.

2) TICKET A2 — Modelo Canônico v1 (ERD lógico)
Descrição: Produzir a especificação do modelo (não o código): entidades, relacionamentos, constraints, enums, e o que vai para metadata.
Aceite:

Entidades mínimas: Company, Environment, Application, Instance
Recursos: WebHost (IIS/Proxy), DbServer, Database, Datastore, InstanceDatastoreBinding
Perfis: IisAppPoolProfile, BindingProfile, WebConfigPatchProfile, InstanceTemplate + assignments
Constraints: unicidades essenciais (ex.: Instance unique por company+env+app+purpose)
Auditoria: AuditEvent + Outbox (conceito)
SecretRef: referência Key Vault

Prompt Copilot:
Gere uma especificação markdown docs/model-v1.md com entidades, relacionamentos, constraints, enums e regras de validação para o sistema. Use SQL Server como alvo e IDs GUID. Separe Application de Instance (1 company/1 env + purpose). Use abordagem híbrida para perfis/templates (forte + metadata). Inclua seção de auditoria SQL+Elastic e secretRef para Key Vault.

3) TICKET A3 — Criar banco e migrações (baseline)
Descrição: criar as migrações iniciais para o Modelo v1.
Aceite:

Migração cria tabelas principais com GUIDs e constraints
Índices principais presentes
Sem segredos persistidos em texto
Scripts reexecutáveis em dev

Prompt Copilot:
Implemente migrações para SQL Server (GUID com NEWSEQUENTIALID quando apropriado) para as tabelas do Modelo v1. Inclua constraints e índices principais. Não inclua segredos, apenas secretRef. Gere instruções no README para subir localmente.

4) TICKET A4 — CRUD Backend (FastAPI) para entidades núcleo
Descrição: endpoints CRUD para Company, Environment, Application, Instance.
Aceite:

OpenAPI completo
Validações (unicidade, enums, integridade)
Paginação e filtros básicos (por company/env/app)
Respostas padronizadas (DTOs)

Prompt Copilot:
Crie endpoints CRUD em FastAPI para Company, Environment, Application e Instance, usando SQL Server e SQLAlchemy. Inclua validações, paginação, filtros (companyId, environmentId, applicationId, purpose), e DTOs Pydantic. IDs são GUID.

5) TICKET A5 — RBAC interno (enforcement na API)
Descrição: implementar Users/Roles/RoleAssignments e proteger rotas.
Aceite:

Usuário sem assignment não acessa dados
Viewer: leitura; Editor: CRUD em instâncias; Admin: tudo; Approver: aprovar PRD (se existir endpoint)
Escopo por Company + Environment (Environment global)
Testes de autorização cobrindo 403 e filtragem

Prompt Copilot:
Implemente RBAC interno no backend: tabelas User, Role, RoleAssignment (escopo companyId + environmentId opcional). Integre com autenticação OIDC (Entra ID) mapeando oid/sub para User interno. Aplique policies nas rotas: filtrar por company/env permitidos e negar por padrão. Crie testes de autorização.

6) TICKET A6 — Auditoria SQL (fonte oficial) + Emissão Elastic (outbox)
Descrição: registrar create/update/delete com before/after/diff e emitir evento estruturado para Elastic via worker.
Aceite:

AuditEvent gravado transacionalmente em SQL
Não logar segredos (sanitização)
Worker processa outbox com retry e idempotência
Endpoint para consultar auditoria por entidade e por período
correlationId por request

Prompt Copilot:
Implemente auditoria no backend: tabela AuditEvent com actor, ação, entityType/entityId, companyId/environmentId quando aplicável, beforeJson/afterJson e diffJson. Use correlationId por request. Crie outbox para envio ao Elastic (ECS-like). Sanitizar qualquer campo marcado como secretRef ou sensível. Criar endpoints GET /audit para consulta e um worker para envio.

7) TICKET A7 — Key Vault + secretRef (server-side)
Descrição: resolver segredos somente no backend para integrações; front nunca recebe segredo.
Aceite:

Tabela SecretRef com metadados mínimos
Serviço de resolução de segredo via Key Vault (somente backend)
Logs/audit sem segredos
Teste: endpoint retorna apenas secretRef, nunca o valor

Prompt Copilot:
Implemente SecretRef e integração com Azure Key Vault no backend. Persistir apenas vaultUri/vaultName + secretName + version opcional. Implementar serviço que resolve segredo apenas server-side para integrações (não expor ao frontend). Garantir sanitização nos logs e auditoria.

8) TICKET A8 — Frontend mínimo (Next.js) com navegação e RBAC
Descrição: UI básica para listar e ver detalhes de Company/Environment/Application/Instance, respeitando RBAC.
Aceite:

Login via Entra ID (OIDC)
Tela: “Minhas empresas” → “Ambientes” → “Aplicações” → “Instâncias”
Se não tem permissão, não aparece
Sem segredos

Prompt Copilot:
Crie um frontend Next.js (TypeScript) com login OIDC (Entra ID) e consumo da API. Implementar telas de listagem e detalhe para Company, Environment, Application e Instance. Respeitar RBAC: a UI deve mostrar somente dados permitidos e lidar com 403/404.