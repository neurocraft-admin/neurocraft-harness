# Orchestration — Requirement to Deployment

This is the single source of truth for stage order, gates, and hand-offs. The CLI
(`harness run <stage>`) and any agent runner should follow this exactly — no stage
skips ahead of a required gate.

## Stages

| # | Stage | Agent / Actor | Input | Output | Gate after |
|---|---|---|---|---|---|
| 1 | Intake | Human (or Intake Agent, future) | raw requirement | `spec.md` | none (spec is draft) |
| 2 | Tech Review | Tech Review Agent | `spec.md` | ranked stack options JSON | **Human picks stack** |
| 3 | Mockup | Design Agent | `spec.md` + chosen stack | `/mockups/*.html` + `.png` | **Client GO/NO-GO** |
| 4 | Scaffold | `harness init` | approved stack | repo + `CLAUDE.md` context | none |
| 5 | Codegen | Codegen Agent (loop, per module) | `spec.md` + Constitution | PRs | **Human PR review** |
| 6 | Guardrails | `harness validate` | repo at HEAD | pass/fail report | auto-blocks bad PRs |
| 7 | Beta | Human / customer | running app | sign-off or change requests | **Beta sign-off** |
| 8 | QE (Alpha-tier only) | QE Agent | `spec.md` (NOT the code, read first) | red/green report, `/qe-suite/` | **Bugs fixed, suite green** |
| 9 | Deploy | Deploy Agent | approved build | deployed URL | **Human `--confirm`, prod needs `--env production`** |

Beta-tier apps (per the two-tier plan) can skip stage 8 entirely. Whether an app is
Beta or Alpha tier is recorded at stage 2 in `.harness/tech-review.json` (`tier` field)
based on complexity/multi-tenancy signals in the spec.

## State tracking

Every app repo carries a `.harness/` folder as the pipeline's memory:
```
.harness/
├── tech-review.json      # stage 2 output + tier decision
├── client-signoff.json   # stage 3 gate result
├── validate-report.json  # stage 6 latest run
├── qe-report.json        # stage 8 latest run
└── deploy-target.json    # stage 9 config (set once, human-provided)
```
A later stage's agent always checks the prior gate's file exists and is in the
expected state before proceeding — this is what makes `harness run <stage>` safe
to re-run without re-litigating earlier decisions.

## Why mockup comes before codegen (stage 3, not after stage 5)

A misunderstood requirement caught in a static HTML mock costs an hour. The same
misunderstanding caught after Codegen has built real backend + DB + tests costs a
rebuild. Client sign-off on the mock is what makes stage 5 safe to run mostly
unattended — the shape of the app is already agreed, so Codegen is filling in a
known shape rather than guessing at one.

## Failure handling

- If Tech Review's spec is too ambiguous to score (stage 2), the pipeline halts and
  returns to stage 1 — never guess a stack from a bad spec.
- If the client rejects a mockup at stage 3, Design Agent revises and re-presents —
  does not proceed to scaffold.
- If Codegen and the Constitution conflict at stage 5, the agent follows the spec but
  flags the conflict in the PR — human decides at PR review.
- If QE finds `SPEC_AMBIGUOUS` failures at stage 8, that goes to the human, not back
  to Codegen (Codegen can't resolve an ambiguity Codegen didn't create).
