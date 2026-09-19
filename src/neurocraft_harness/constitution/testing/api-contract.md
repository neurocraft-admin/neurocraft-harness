# API Contract (Swagger + Postman)
- Every backend auto-generates its OpenAPI spec from code annotations — never hand-written.
- Swagger UI deployed in non-prod for manual poke-around during Beta.
- Postman collection maintained per module — covers all endpoints with example request/response.
- Contract test step in the dev loop: run the Postman collection to verify API behaviour after every change.