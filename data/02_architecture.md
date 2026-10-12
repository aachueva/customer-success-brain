# Architecture Review (October 3)
Acme's assistant uses a web chat frontend, API gateway, retrieval service, vector index of approved FAQs, LLM answer generation, and ticketing integration.
Production authentication uses SSO. Audit logging is implemented in staging but production retention settings are not verified. Encryption in transit is enabled.
Open architecture item: PHI redaction must run before logs and external model requests. Ravi owns the redaction gate. No evidence of production sign-off yet.
