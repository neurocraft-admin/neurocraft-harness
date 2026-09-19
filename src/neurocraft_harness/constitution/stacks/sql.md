# SQL / Database Constitution
Schema owned by migrations only (EF Migrations / Flyway / Liquibase / Alembic) — no hand-edited prod schema.
- snake_case tables/columns, plural table names.
- Every foreign key indexed.
- No SELECT * in application code.
- Multi-tenant: tenant ID on every scoped table, enforced via base repository pattern.
Testing: migration up/down tested. Repository-layer integration tests against a real test DB.
