# Java / Spring Boot Constitution
Architecture: Controller → Service → Repository, enforced via @RestController/@Service/@Repository.
- Constructor injection only — no field @Autowired.
- DTOs (records for Java 17+) — never leak JPA @Entity through the API.
- Centralized error handling via @ControllerAdvice.
Testing: JUnit 5 + Mockito for units. @SpringBootTest + Testcontainers for integration against a real test DB.
