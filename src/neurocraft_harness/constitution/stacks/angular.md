# Angular Constitution
Architecture: feature modules, each with its own components, services, and models.
- One service per API domain (e.g. LeadService, TicketService) — no raw HttpClient calls in components.
- Components contain zero business logic — delegate to services.
- Reactive forms only (no template-driven forms).
- Naming: PascalCase components/services, kebab-case file names, camelCase variables.
- Environment-specific configs via environment.ts — no hardcoded URLs or keys.
- Mobile-responsive UI required. Brand colors/theme are project-specific — set per project, not fixed here.