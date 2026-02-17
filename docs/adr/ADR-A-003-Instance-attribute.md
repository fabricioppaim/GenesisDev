Status: Accepted
Contexto:
Além do “ambiente” (TST), existe a finalidade (Sandbox/Fixa) dentro desse ambiente, que muda a forma de uso/gestão.
Decisão:
Modelar “Sandbox/Fixa” como purpose (ou tags) na entidade Instance, não como Environment.
Consequências / Trade-offs:

✅ Evita explosão de ambientes e regras duplicadas.
✅ Mantém ambiente como estágio de pipeline e purpose como intenção/uso.
⚠️ Exige regras de unicidade incluindo purpose (ex.: não ter 2 “Sandbox” da mesma app no mesmo ambiente/empresa, se isso for desejado).