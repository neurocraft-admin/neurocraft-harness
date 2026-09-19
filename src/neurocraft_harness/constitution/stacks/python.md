# Python (FastAPI) Constitution
Architecture: Router → Service → Repository.
- Type hints mandatory on every function signature.
- Dependency injection via FastAPI's Depends() — no global singletons.
- Pydantic models for every request/response boundary.
- Naming: snake_case functions/vars, PascalCase classes.
Testing: pytest + pytest-mock. Every service function: happy-path + failure-path test.
