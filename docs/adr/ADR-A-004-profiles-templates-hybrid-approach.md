Status: Accepted
Contexto:
Precisamos de padronização e validação forte (bindings, datastores, app pool etc.), mas também de extensibilidade por stack (Genexus, .NET, PHP…).
Decisão:

Campos fortemente tipados para o que é governável/validador (ex.: bindings, datastore mapping, perfis IIS).
Campo metadata (JSON) somente para extensões “não críticas” e por tecnologia.
Consequências / Trade-offs:
✅ Garante integridade e evita “bagunça de JSON no banco”.
✅ Permite evoluir stacks sem migrar schema a cada mudança pequena.
⚠️ Exige disciplina: o que for crítico não pode ir para metadata.