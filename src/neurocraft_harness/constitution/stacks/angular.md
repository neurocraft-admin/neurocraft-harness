# Angular Constitution
Architecture: Component → Service → API layer. Zero business logic in components.
- Smart/dumb component split.
- Services injectable, providedIn: 'root' where appropriate.
- Strongly typed everywhere — no `any`.
- Naming: Angular CLI conventions (kebab-case files, PascalCase classes, camelCase methods).
Testing: Jasmine/Karma or Jest. Every service method tested; components tested for public behavior only.
