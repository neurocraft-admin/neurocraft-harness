# C# (.NET) Constitution
Architecture: Controller → Service → Repository → IDbConnection (Dapper). Controllers contain zero business logic.
- Constructor injection only, via built-in DI container.
- DTOs for every API boundary — never return raw DB result objects directly.
- Async all the way — no .Result / .Wait().
- Naming: PascalCase classes/methods, camelCase locals, I-prefix interfaces.