1) TICKET B1 — Criar modelo de PipelineDefinition e PipelineRun
Aceite:

Tabelas no SQL (GUID)
PipelineRun vincula Instance + Definition
Campos de correlação (correlationId, externalRunId, externalUrl)
Constraints de idempotência (provider+externalEventId)

Prompt Copilot:
Crie a especificação do modelo de dados (SQL Server) e endpoints CRUD mínimos para PipelineDefinition e PipelineRun. Inclua constraints para idempotência e campos correlationId/externalRunId/externalUrl/status/timestamps.

2) TICKET B2 — Endpoint: Trigger Execution (API interna)
Aceite:

POST /instances/{id}/deploy cria PipelineRun e dispara provider
Resposta imediata (202 Accepted) com pipelineRunId
AuditEvent CREATE para PipelineRun

Prompt Copilot:
Defina o contrato do endpoint POST /instances/{id}/deploy: criação do PipelineRun (Queued), validação RBAC, auditoria, e disparo assíncrono via provider adapter. Inclua payload de inputs (sem segredos) e correlationId.

3) TICKET B3 — Jenkins Adapter: Trigger
Aceite:

Dispara job via Jenkins Remote Access API (POST build/buildWithParameters) [jenkins.io]
Autenticação via token obtido do Key Vault (secretRef)
Registra external queue item/build url (quando disponível)

Prompt Copilot:
Especifique o adapter Jenkins: como disparar jobs via Remote Access API (POST /buildWithParameters), quais parâmetros enviar (pipelineRunId/correlationId), como armazenar externalUrl e como tratar erros (PipelineRun=Failed + AuditEvent).

4) TICKET B4 — Jenkins Callback Receiver
Aceite:

Endpoint POST /webhooks/jenkins
Valida assinatura/HMAC (ou segredo compartilhado)
Atualiza PipelineRun status com base em event: start/success/failure/unstable [plugins.jenkins.io]
Idempotente

Prompt Copilot:
Defina endpoint POST /webhooks/jenkins que recebe eventos de build (start/success/failure/unstable) e atualiza PipelineRun. Implementar validação por assinatura/HMAC, idempotência por eventId, sanitização do payload e geração de AuditEvent UPDATE.

5) TICKET B5 — Azure DevOps Adapter: Trigger
Aceite:

Dispara pipeline via REST “Runs - Run Pipeline” [learn.microsoft.com]
Inclui correlationId/pipelineRunId em variables/templateParameters
Token/PAT vindo do Key Vault

Prompt Copilot:
Especifique adapter Azure DevOps para disparar pipeline via REST (Runs - Run Pipeline). Inclua como passar variables/templateParameters para correlacionar com PipelineRun e como registrar externalRunId/externalUrl.

6) TICKET B6 — Azure DevOps Callback Receiver (Service Hooks)
Aceite:

Endpoint POST /webhooks/azuredevops
Recebe eventos de service hooks (ex.: build.complete) [learn.microsoft.com]
HTTPS obrigatório (documentar) [learn.microsoft.com]
Atualiza PipelineRun (Succeeded/Failed/Stopped)
Idempotente
Sem segredos no log

Prompt Copilot:
Defina endpoint POST /webhooks/azuredevops para receber service hook events (principalmente build.complete). Parsear payload, correlacionar por pipelineRunId/correlationId e atualizar PipelineRun. Implementar idempotência, sanitização e auditoria.

7) TICKET B7 — Observabilidade: logs e eventos para Elastic
Aceite:

Evento estruturado para cada mudança de status de PipelineRun
correlação com requestId/correlationId
sem segredos

Prompt Copilot:
Defina o evento de observabilidade para Elastic quando PipelineRun mudar de status. Inclua trace/correlationId, provider, instanceId, pipelineDefinitionId, externalUrl, status e timestamps, garantindo sanitização.

8) TICKET B8 — UI: histórico de execuções e status
Aceite:

Tela da instância mostra lista de PipelineRuns
Visualiza status e links externos
Exibe auditoria relacionada

Prompt Copilot:
Defina telas/rotas Next.js para listar execuções (PipelineRuns) por Instância, com status, timestamps, link externo e filtro. Integrar com RBAC e exibir auditoria associada.