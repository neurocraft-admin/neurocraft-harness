# Token Efficiency — Constitution slicing + optional Caveman layer

## What this harness already does for tokens
`harness context` (see `cli.py`) only ever writes the Constitution slice relevant to
the chosen stack into a repo's `CLAUDE.md` — e.g. picking `dotnet` pulls in
`csharp.md` + `sql.md`, never the Java/Python/Angular files too. That's the main
token saving in this system: agents load a few pages of relevant rules, not the
whole multi-stack Constitution, every session.

## Optional: Caveman (github.com/JuliusBrussee/caveman)
A separate, third-party, MIT/BSL-licensed tool that works at the conversation layer,
independent of this harness. Two pieces:
- **The skill** — makes the agent's own prose replies terser. Its maintainer's
  published numbers: ~65% average cut in *output* tokens across a 10-prompt
  benchmark, but the maintainer is explicit that this does not translate 1:1 into
  whole-session savings (input/reasoning tokens are unaffected, and the skill's own
  rules cost ~1-1.5k input tokens per turn). See their `docs/HONEST-NUMBERS.md`.
- **The proxy** — runs locally between the agent and the provider, compresses what
  the agent *reads* (logs, diffs, JSON, search results) before it's sent. Their
  pinned benchmark: ~33% reduction in input tokens across 6 cases, with one case
  showing an increase (their own README flags this openly).

## Should you use it with this harness?
It's complementary, not required — this harness's own token discipline (slim,
stack-specific context files) and Caveman's (terser agent replies + compressed
tool-output reading) address different parts of the bill. Worth trying if your
Codegen Agent sessions involve a lot of back-and-forth prose or large log/diff
reads, since that's specifically what Caveman targets.

## Install (if you want it)
```bash
npx skills add JuliusBrussee/caveman        # the skill (free, MIT)
# or, for the proxy too:
npm install -g @caveman-ai/cli && caveman setup --install
caveman claude
```
This is not wired into `harness` itself — it's an independent tool you point at
whichever agent CLI you're already using (Claude Code, etc.). Measure your own
setup before assuming a specific percentage — the maintainer says the same about
their own numbers.
