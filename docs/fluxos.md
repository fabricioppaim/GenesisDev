3.1 Fluxo 1 — Disparar Jenkins e receber callback
Trigger (seu sistema → Jenkins)

Jenkins expõe Remote Access API para disparar builds via POST em /job/<name>/build ou /buildWithParameters. [jenkins.io]
Você dispara via backend (token do Jenkins vindo do Key Vault).

Callback (Jenkins → seu webhook)
Opções recomendadas:

Outbound WebHook plugin (post-build action) enviando eventos start/success/failure/unstable. [plugins.jenkins.io]
Pipeline step “HTTP call” (ex.: curl) com HMAC signature.


O plugin Outbound WebHook já define payload com buildUrl, projectName, event e variáveis. [plugins.jenkins.io]

✅ Correlacionar: sempre que disparar o job, envie pipelineRunId (ou correlationId) como parâmetro da build. O callback devolve isso (em build vars), e você identifica a execução com precisão.

3.2 Fluxo 2 — Disparar Azure DevOps e receber callback
Trigger (seu sistema → Azure DevOps)

Usar endpoint oficial “Runs - Run Pipeline” (POST). [learn.microsoft.com]
Autenticação pode ser OAuth2 ou PAT — mas como você vai usar secretRef no Key Vault, o token fica server-side.

Callback (Azure DevOps → seu webhook)

Azure DevOps Service Hooks permitem configurar “Web Hooks” para mandar eventos JSON a um endpoint HTTPS. [learn.microsoft.com], [github.com]
Eventos úteis para você:

build.complete (build finalizou) e outros de pipeline/run state. [learn.microsoft.com]



Importantes detalhes do ADO:

Use somente HTTPS (o próprio guia enfatiza isso) e webhooks não podem apontar para localhost/ranges especiais. [learn.microsoft.com]

✅ Correlacionar: ao disparar a pipeline, inclua pipelineRunId/correlationId em variables/templateParameters (não sensível). O evento de callback deve carregar esses dados (dependendo de quão “All vs Minimal” você configurar). [learn.microsoft.com], [learn.microsoft.com]