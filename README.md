# neurocraft-harness

Constitution + agents + skills + orchestration, packaged as one installable CLI.
Install once, `harness` is on your PATH everywhere, for any AI coding tool that
reads a root-level context file (CLAUDE.md / AGENTS.md).

## Install

```bash
git clone <your-remote-url> neurocraft-harness
cd neurocraft-harness

uv tool install .          # recommended
# or
pip install -e .           # editable, good while actively editing the Constitution
```

Once pushed to a remote, teammates skip the clone:
```bash
uv tool install git+https://github.com/<you>/neurocraft-harness.git
```

Confirm: `harness --help` and `harness stages` (prints the full pipeline table).

## The pipeline (requirement → deployment)

See `src/neurocraft_harness/orchestration/workflows/full-pipeline.md` for the full
stage table and gate rules. Short version:

```bash
harness review --spec requirement.md                       # 2: pick a stack
harness mockup --spec requirement.md --app ./my-app         # 3: clickable mocks
harness present --app ./my-app                              # 3: package for client
harness signoff --app ./my-app --status approved \
    --approved-by "client@example.com"                      # 3: gate recorded
harness init my-app --stack dotnet                          # 4: scaffold (checks sign-off)
# Codegen Agent works inside my-app, using CLAUDE.md as its context (5)
harness validate --app ./my-app                             # 6: guardrails
# Beta: customer/self verifies (7)
harness qe start --app ./my-app --spec requirement.md       # 8: Alpha-tier only
harness deploy --app ./my-app --confirm --env staging       # 9
harness deploy --app ./my-app --confirm --env production    # 9, explicit only
```

Every stage's result is recorded under `<app>/.harness/*.json` — that state is what
later stages (`init`, `deploy`) check before they'll run, so a gate can't be silently
skipped.

## What's real vs. stubbed
- `constitution/*`, `agents/*-prompt.md`, `orchestration/workflows/*.md` — real
  content, ready to use/edit.
- `harness context` / `harness init` / `harness signoff` / `harness stages` — fully
  functional (file generation, gate-checking logic, state tracking).
- `harness review` / `harness mockup` / `harness validate` / `harness qe start` /
  `harness deploy` — CLI structure, gate logic, and prompts are real; the actual LLM
  call is a marked stub (`STUB:` in `cli.py`) — wire it to the Claude Agent SDK.

## Token efficiency
See `src/neurocraft_harness/docs/token-efficiency.md` — covers what this harness
already does (stack-sliced Constitution context) and an optional third-party layer
(Caveman) you can add on top, with honestly-sourced numbers, not inflated ones.

## Updating the Constitution later
Edit files under `src/neurocraft_harness/constitution/`, bump the version in
`pyproject.toml`, reinstall, then re-run `harness context --stack <x>` in active
repos to pull the latest rules.
