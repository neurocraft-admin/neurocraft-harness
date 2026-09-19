# C# (.NET) Constitution
Architecture: Controller → Service → Repository → DbContext. Controllers contain zero business logic.
- Constructor injection only, via built-in DI container.
- DTOs for every API boundary — never expose EF entities directly.
- Async all the way — no .Result / .Wait().
- Naming: PascalCase classes/methods, camelCase locals, I-prefix interfaces.
Testing: xUnit + Moq. Every public Service method: happy-path + failure-path test.
