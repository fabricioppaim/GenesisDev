Decisão: criar um “adapter” por provider, isolando:

como dispara (trigger),
como interpreta callback,
como mapeia estados.

2.1 PipelineProvider

provider = Jenkins | AzureDevOps

2.2 PipelineDefinition
Representa “o que executar” (job do Jenkins / pipeline do ADO).

provider
displayName
externalId (ex.: job name / pipelineId)
companyId (se você quiser multi-tenant por empresa)
secretRefId (credencial de chamada: token Jenkins / PAT ADO no Key Vault)