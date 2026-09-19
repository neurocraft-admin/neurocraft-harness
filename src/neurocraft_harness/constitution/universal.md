# Universal Constitution Rules (apply to every stack)

- SOLID, checkable, not decorative:
  - Single Responsibility: one class/module = one reason to change.
  - Open/Closed: add features via new classes/interfaces, never by editing tested existing logic.
  - Liskov Substitution: a subclass/implementation must be swappable for its parent without breaking callers.
  - Interface Segregation: no interface with methods a client is forced to implement but never uses.
  - Dependency Inversion: high-level modules depend on abstractions, not concrete implementations. Always inject dependencies.
- No function/method over 40 lines.
- No magic numbers/strings — named constants or config only.
- Every I/O call (DB, API, file, network) must have explicit error handling. No silent failures.
- Comments explain *why*, not *what*.
- No task is "done" without passing tests.
