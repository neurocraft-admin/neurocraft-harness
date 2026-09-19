# SQL / Database Constitution
Schema owned by migrations only (Flyway) — no hand-edited prod schema. Stored procedures versioned under `/Database/StoredProcedures/<Module>/`.
- snake_case tables/columns, plural table names.
- Every foreign key indexed.
- No SELECT * in application code.
- Multi-tenant projects only: tenant ID on every scoped table, enforced via base repository pattern. Single-tenant projects (like NEXUS) omit this.