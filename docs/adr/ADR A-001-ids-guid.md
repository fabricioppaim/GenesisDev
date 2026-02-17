Status: Accepted
Contexto:
Precisamos de IDs estáveis e facilmente correlacionáveis entre auditoria (SQL + Elastic), integrações (Jenkins/Azure DevOps), logs e possíveis eventos.
Decisão:
Usar uniqueidentifier como chave primária em entidades principais. Preferir geração no banco com NEWSEQUENTIALID() quando aplicável para reduzir fragmentação de índice.
Consequências / Trade-offs:

✅ Facilita correlação entre sistemas e eventos (audit/log/pipeline).
✅ Simplifica integrações e referências cruzadas.
⚠️ Índices podem fragmentar; mitigação com GUID sequencial e boas práticas de índices.
Alternativas consideradas:
bigint identity (mais compacto, mas pior para correlação distribuída e integrações).