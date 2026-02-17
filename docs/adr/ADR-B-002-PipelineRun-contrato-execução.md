Decisão: toda execução vira um registro PipelineRun no SQL (fonte oficial), com:

correlationId,
externalRunId,
externalUrl,
status,
timestamps,
inputs/outputs (sanitizados).

Assim você garante rastreabilidade e auditoria consistentes.

2.3 PipelineRun
Representa “uma execução concreta”.

pipelineRunId (GUID)
instanceId
pipelineDefinitionId
triggeredByUserId (ou “system”)
correlationId (GUID por request)
status (Queued/Running/Succeeded/Failed/Canceled/Unknown)
externalRunId (build number, run id, etc.)
externalUrl
inputs (JSON sanitizado)
outputsSummary (JSON sanitizado)
startedAt, finishedAt


Isso conversa muito bem com os eventos do Azure DevOps (ex.: build.complete) e com eventos de Jenkins (start/success/failure).