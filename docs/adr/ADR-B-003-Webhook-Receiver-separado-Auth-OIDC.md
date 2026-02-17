Decisão: endpoints de webhook não usam OIDC (porque é máquina→máquina).
Eles usam:

HMAC signature ou Basic Auth (segredo vindo do Key Vault via secretRef) ou ambos.
Para ADO, a recomendação é usar HTTPS e pode usar Basic Auth, mas somente via HTTPS. 
Para Jenkins, você pode usar plugin de outbound webhook ou um “curl” no pipeline com assinatura.