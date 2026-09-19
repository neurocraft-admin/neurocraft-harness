# Orchestration — Client Sign-off on Mockups

Sits between stage 3 (Mockup) and stage 4 (Scaffold) in `full-pipeline.md`. This is
the one stage where an external, non-technical person (the client) is the approver,
not you or your QE person.

## Flow

1. Design Agent produces `/mockups/*.html` + `/mockups/screenshots/*.png` +
   `mockup-manifest.json` (stage 3).
2. `harness present --app <name>` packages the screenshots + a one-page summary
   (plain language, no tech jargon) and hands it to you to send the client — email,
   WhatsApp, whatever channel you already use with them. This step does not
   auto-send anything; you control what the client sees and when.
3. Client responds with one of:
   - **Approved as-is** → `harness signoff --app <name> --status approved`
   - **Approved with changes** → note the changes in `spec.md` (amend the spec, not
     just a side note), regenerate mockups (`harness run mockup`), re-present.
   - **Rejected** → treat as a fresh Intake-stage conversation; the requirement
     itself may be wrong, not just the mock.
4. `harness signoff` writes `.harness/client-signoff.json`:
   ```json
   {
     "status": "approved",
     "approved_by": "<client name/email as told to you>",
     "date": "<ISO date>",
     "spec_version": "<hash or version of spec.md at approval time>"
   }
   ```
5. Stage 4 (`harness init`) checks this file exists with `status: approved` before
   scaffolding. No sign-off recorded → `harness init` refuses to run.

## Why record `spec_version`

If the client asks for a change mid-build later (post-Beta, per the Alpha/QE plan),
you need to know whether that's a genuinely new request or something they already
signed off on and are now revising. The recorded spec version is what makes that
distinction checkable instead of a memory argument.
