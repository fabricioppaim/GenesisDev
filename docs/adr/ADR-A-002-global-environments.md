Status: Accepted
Contexto:
Ambientes representam estágios padronizados (PRD/HLG/DEV/TST). O RBAC será interno e escopado por Empresa e Ambiente.
Decisão:
Modelar Environment como entidade global (ex.: PRD/HLG/DEV/TST). A empresa pode “habilitar” subconjunto via configuração/associação (se necessário).
Consequências / Trade-offs:

✅ Simplifica governança, relatórios e políticas (um DEV é DEV para todos).
✅ Reduz duplicidade e divergência de ambientes por empresa.
⚠️ Algumas empresas podem não usar todos os ambientes — tratável por associação “empresa x ambientes habilitados”.
Alternativas consideradas:
Ambiente por empresa (gera duplicidade e aumenta complexidade).