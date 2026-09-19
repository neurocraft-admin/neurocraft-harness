"""
Neurocraft Harness CLI.
Installed as a console-script entry point named `harness` (see pyproject.toml),
so once installed via pip or uv, `harness` is available globally on PATH.

Stage order and gate semantics are documented in
orchestration/workflows/full-pipeline.md — this module implements that contract.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

import typer

app = typer.Typer(help="Neurocraft agentic app-building harness")

PACKAGE_ROOT = Path(__file__).resolve().parent
CONSTITUTION_DIR = PACKAGE_ROOT / "constitution"
AGENTS_DIR = PACKAGE_ROOT / "agents"
ORCHESTRATION_DIR = PACKAGE_ROOT / "orchestration"

STACK_FILE_MAP = {
    "dotnet": ["csharp.md", "sql.md", "angular.md"],
    "spring": ["java-spring.md", "sql.md", "angular.md"],
    "fastapi": ["python.md", "sql.md", "angular.md"],
}


def _harness_dir(app_dir: Path) -> Path:
    d = app_dir / ".harness"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Stage 1-2: Intake / Tech Review
# ---------------------------------------------------------------------------
@app.command()
def review(spec: Path = typer.Option(..., help="Path to the spec/requirement file")):
    """Stage 2 — MANDATORY. Tech Review Agent ranks stack options before scaffolding."""
    if not spec.exists():
        typer.secho(f"Spec not found: {spec}", fg=typer.colors.RED)
        raise typer.Exit(1)
    prompt_path = AGENTS_DIR / "tech-review-agent-prompt.md"
    typer.echo(f"Running Tech Review Agent (prompt: {prompt_path.name}) against {spec.name}...")
    typer.secho(
        "STUB: wire to your agent runner (Claude Agent SDK / Claude Code). "
        "Expected output: JSON per tech-review-agent-prompt.md, written to .harness/tech-review.json",
        fg=typer.colors.YELLOW,
    )


# ---------------------------------------------------------------------------
# Stage 3: Mockup
# ---------------------------------------------------------------------------
@app.command()
def mockup(
    spec: Path = typer.Option(..., help="Path to the approved spec"),
    app_dir: Path = typer.Option(Path("."), "--app", help="App working directory"),
):
    """Stage 3 — Design Agent produces clickable HTML mocks + screenshots for client review."""
    prompt_path = AGENTS_DIR / "design-agent-prompt.md"
    typer.echo(f"Running Design Agent (prompt: {prompt_path.name}) against {spec.name}...")
    typer.secho(
        "STUB: wire to your agent runner. Expected output: /mockups/*.html, "
        "/mockups/screenshots/*.png, mockup-manifest.json",
        fg=typer.colors.YELLOW,
    )


@app.command()
def present(app_dir: Path = typer.Option(Path("."), "--app")):
    """Package mockup screenshots + a plain-language summary to send the client."""
    mockups = app_dir / "mockups"
    if not mockups.exists():
        typer.secho("No /mockups found — run `harness mockup` first.", fg=typer.colors.RED)
        raise typer.Exit(1)
    shots = sorted((mockups / "screenshots").glob("*.png")) if (mockups / "screenshots").exists() else []
    typer.echo(f"Found {len(shots)} screen(s) to present.")
    typer.secho(
        "This command prepares material only — it does not send anything. "
        "Attach the screenshots + mockup-manifest.json summary to whatever channel "
        "you already use with the client.",
        fg=typer.colors.YELLOW,
    )


@app.command()
def signoff(
    app_dir: Path = typer.Option(..., "--app"),
    status: str = typer.Option(..., help="approved | approved_with_changes | rejected"),
    approved_by: str = typer.Option(None, help="Client name/email, if approved"),
    spec_version: str = typer.Option(None, help="Hash/version of spec.md at approval time"),
):
    """Record the client's decision on the mockup — required before `harness init` will run."""
    valid = {"approved", "approved_with_changes", "rejected"}
    if status not in valid:
        typer.secho(f"status must be one of {valid}", fg=typer.colors.RED)
        raise typer.Exit(1)
    record = {
        "status": status,
        "approved_by": approved_by,
        "date": _now(),
        "spec_version": spec_version,
    }
    out = _harness_dir(app_dir) / "client-signoff.json"
    out.write_text(json.dumps(record, indent=2))
    typer.secho(f"Recorded sign-off ({status}) at {out}", fg=typer.colors.GREEN)


# ---------------------------------------------------------------------------
# Stage 4: Scaffold
# ---------------------------------------------------------------------------
@app.command()
def init(
    app_name: str,
    stack: str = typer.Option(..., help="e.g. dotnet, spring, fastapi (backend) — Angular assumed for frontend"),
    skip_signoff_check: bool = typer.Option(False, help="Bypass the client sign-off gate (not recommended)"),
):
    """Stage 4 — Scaffold a new app repo. Refuses to run without a recorded client sign-off."""
    if stack not in STACK_FILE_MAP:
        typer.secho(f"Unknown stack '{stack}'. Options: {list(STACK_FILE_MAP)}", fg=typer.colors.RED)
        raise typer.Exit(1)

    target = Path.cwd() / app_name

    if not skip_signoff_check:
        signoff_file = target / ".harness" / "client-signoff.json"
        if not signoff_file.exists():
            typer.secho(
                "No client sign-off recorded for this app. Run `harness signoff` first, "
                "or pass --skip-signoff-check to bypass (not recommended).",
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
        record = json.loads(signoff_file.read_text())
        if record.get("status") != "approved":
            typer.secho(f"Sign-off status is '{record.get('status')}', not 'approved'. Refusing to scaffold.", fg=typer.colors.RED)
            raise typer.Exit(1)

    target.mkdir(parents=True, exist_ok=True)
    _harness_dir(target)
    _write_context_file(stack, target / "CLAUDE.md")
    typer.secho(f"Scaffolded {app_name} with stack={stack}. Context file written to CLAUDE.md.", fg=typer.colors.GREEN)


@app.command()
def context(
    stack: str = typer.Option(..., help="e.g. dotnet, spring, fastapi, angular"),
    out: Path = typer.Option(Path("CLAUDE.md"), help="Output context filename"),
):
    """Regenerate the slim context file for an existing repo."""
    _write_context_file(stack, Path.cwd() / out)
    typer.secho(f"Context regenerated at {out}", fg=typer.colors.GREEN)


def _write_context_file(stack: str, out_path: Path) -> None:
    parts = [(CONSTITUTION_DIR / "universal.md").read_text()]
    for fname in STACK_FILE_MAP.get(stack, []):
        f = CONSTITUTION_DIR / "stacks" / fname
        if f.exists():
            parts.append(f.read_text())
    testing_dir = CONSTITUTION_DIR / "testing"
    if testing_dir.exists():
        for f in sorted(testing_dir.glob("*.md")):
            parts.append(f.read_text())
    out_path.write_text("\n\n---\n\n".join(parts))


# ---------------------------------------------------------------------------
# Stage 5-6: Codegen / Guardrails
# ---------------------------------------------------------------------------
@app.command()
def validate(app_dir: Path = typer.Option(Path("."), "--app")):
    """Stage 6 — local guardrails before a PR: linter, coverage, Constitution checks."""
    typer.echo("Running guardrails...")
    checks = ["lint", "unit-tests", "coverage-threshold", "constitution-rules", "security-scan"]
    results = {c: "STUB" for c in checks}
    for c in checks:
        typer.echo(f"  [ ] {c} -- STUB, wire real tool call here")
    report = {"timestamp": _now(), "results": results, "passed": False}
    (_harness_dir(app_dir) / "validate-report.json").write_text(json.dumps(report, indent=2))
    typer.secho("Validation stubbed — wire real checks before relying on this.", fg=typer.colors.YELLOW)


# ---------------------------------------------------------------------------
# Stage 8: QE
# ---------------------------------------------------------------------------
qe_app = typer.Typer(help="QE workflow — independent, spec-first TDD, triggered on demand only (Alpha-tier)")
app.add_typer(qe_app, name="qe")


@qe_app.command("start")
def qe_start(
    app_dir: Path = typer.Option(..., "--app"),
    spec: Path = typer.Option(..., help="Path to the ORIGINAL spec — QE agent reads this, not the code, first"),
):
    """Runs the QE Agent's TDD cycle: spec-first test writing, red, fix loop, green."""
    prompt_path = AGENTS_DIR / "qe-agent-prompt.md"
    typer.echo(f"Running QE Agent (prompt: {prompt_path.name})\n  spec: {spec}\n  app:  {app_dir}")
    typer.secho(
        "STUB: wire to agent runner. Ordering must be enforced: spec read fully "
        "BEFORE any implementation file is opened.",
        fg=typer.colors.YELLOW,
    )


@qe_app.command("regress")
def qe_regress(app_dir: Path = typer.Option(..., "--app")):
    """Re-run the committed QE suite in /qe-suite/."""
    suite_dir = app_dir / "qe-suite"
    if not suite_dir.exists():
        typer.secho("No QE suite found — run `harness qe start` first.", fg=typer.colors.RED)
        raise typer.Exit(1)
    typer.echo(f"Re-running QE suite at {suite_dir} -- STUB, wire test runner")


@qe_app.command("report")
def qe_report(app_dir: Path = typer.Option(..., "--app")):
    """Print the last QE run's red/green summary."""
    report_path = app_dir / ".harness" / "qe-report.json"
    if not report_path.exists():
        typer.secho("No QE report found.", fg=typer.colors.RED)
        raise typer.Exit(1)
    typer.echo(json.dumps(json.loads(report_path.read_text()), indent=2))


# ---------------------------------------------------------------------------
# Stage 9: Deploy
# ---------------------------------------------------------------------------
@app.command()
def deploy(
    app_dir: Path = typer.Option(..., "--app"),
    confirm: bool = typer.Option(False, "--confirm", help="Required — deploy never runs without this"),
    env: str = typer.Option("staging", help="staging | production"),
):
    """Stage 9 — Deploy Agent. Refuses unless preconditions in deploy-agent-prompt.md are met."""
    if not confirm:
        typer.secho("Refusing to deploy without --confirm.", fg=typer.colors.RED)
        raise typer.Exit(1)

    harness_dir = app_dir / ".harness"
    missing = []
    validate_report = harness_dir / "validate-report.json"
    signoff_report = harness_dir / "client-signoff.json"
    if not validate_report.exists():
        missing.append("validate-report.json (run `harness validate`)")
    if not signoff_report.exists():
        missing.append("client-signoff.json (run `harness signoff`)")

    tech_review = harness_dir / "tech-review.json"
    tier = None
    if tech_review.exists():
        tier = json.loads(tech_review.read_text()).get("tier")
    if tier == "alpha" and not (harness_dir / "qe-report.json").exists():
        missing.append("qe-report.json (Alpha-tier app requires QE — run `harness qe start`)")

    if missing:
        typer.secho("Cannot deploy — missing preconditions:", fg=typer.colors.RED)
        for m in missing:
            typer.echo(f"  - {m}")
        raise typer.Exit(1)

    if env == "production":
        typer.secho(f"Deploying to PRODUCTION for {app_dir.name} — confirmed explicitly.", fg=typer.colors.GREEN)
    else:
        typer.echo(f"Deploying to {env} for {app_dir.name}...")

    typer.secho(
        "STUB: wire actual build/publish/deploy commands for the detected stack "
        "per deploy-agent-prompt.md.",
        fg=typer.colors.YELLOW,
    )


# ---------------------------------------------------------------------------
# Orchestration helper
# ---------------------------------------------------------------------------
@app.command()
def stages():
    """Print the full pipeline stage table (see orchestration/workflows/full-pipeline.md)."""
    f = ORCHESTRATION_DIR / "workflows" / "full-pipeline.md"
    typer.echo(f.read_text())


def main():
    app()


if __name__ == "__main__":
    main()
