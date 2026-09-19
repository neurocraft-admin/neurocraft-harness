# API Contract Testing (Swagger/OpenAPI)
- Every backend auto-generates its OpenAPI spec from code annotations — never hand-written.
- Contract test step in the dev Loop: compares spec against example req/response shapes.
- Angular API client generated FROM the same OpenAPI spec (openapi-generator) — frontend/backend can't silently drift.
- Swagger UI deployed in non-prod for manual poke-around during Beta.
