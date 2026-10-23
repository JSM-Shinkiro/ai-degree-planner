# Team Progress

Updated October 22, 2026, Arizona time.

## Current implementation

The refined prototype includes five real course summaries, two resources, a shorter profile form, a searchable course picker, three learning stages, completion actions, profile export/import, a Gemini RAG adapter, evidence inspection, and an Adzuna adapter. Still exploring shows both career directions. Course and resource cards explain the suggested learning connection.

**Live RAG is not yet verified.** No Gemini key is configured here. The pipeline passes tests using controlled provider responses. Live Adzuna requests also need a credentialed check.

Four ECE academic rules remain unknown because the course entries expose internal requirement IDs. One CSC120 condition is reviewed from the current catalog program requirements. Course descriptions and credits were checked against official sources. Remaining rules and supporting records need review.

Automatic source retrieval is a target requirement, not an implemented runtime feature. The app currently reads bundled records. The saved source files are development references. The intended runtime fetches official evidence as needed, with a temporary cache and no required permanent course database.

## Milestones

| Milestone | Owner | Status | Evidence / next step |
| --- | --- | --- | --- |
| M0: Setup and sources | To assign | Partial | Environment and records ready. Review sample papers and confirm provider access |
| M1: Complete RAG interaction | To assign | Partial | Pipeline and tests implemented. Run with a real key |
| M2: Checkpoint interface | To assign | Partial | Hybrid retrieval, inspector, plots, profile files implemented. Complete live demo and rule review |
| M3: Midpoint submission | Team | Open | Report, screenshots, narrated video |
| M4: Returning students | To assign | Partial | Portable files work. Hosted authentication/storage remain |
| M5: Opportunities | To assign | Partial | Adapter and interface implemented. Confirm credentials and results |
| M6: Coverage and updates | To assign | Partial | Five-source review importer works. Add runtime source retrieval, edition checks, and freshness/failure handling |
| M7: Final evaluation | Team | Open | Held-out cases, student pilot, presentation |

## Verification

- Clean installation from pinned dependencies succeeded.
- 80 automated tests passed, including 12 Streamlit interaction tests.
- Streamlit started successfully and returned an `ok` health response and its root page.
- The importer fetched and parsed all five official course entries.
- All five keyword smoke cases passed, covering beginners, experienced students, changed goals, and completed coursework.
- Provider behavior was tested with controlled responses, not live credentials.
- Regression cases cover failed grades, blocked-course stages, stale results, imported fields, server-key visibility, completion actions, career choices, unsupported queries, and AI abstentions.

See [prototype verification](07_PROTOTYPE_VERIFICATION.md) for commands, timing scope, and limitations.

## Next work session

1. Configure a Gemini key and verify the model IDs.
2. Precompute the index and record a real generated answer with citations.
3. Resolve and review the four remaining ECE enrollment requirement references.
4. Review the six sample papers and their tools/videos.
5. Configure Adzuna and inspect actual opportunity results.
6. Assign owners and prepare the midpoint report/demo.

## Work log

```text
Date:
Contributors:
Tasks completed:
Files or commits:
Tests and live checks:
Measurements:
Open issues:
Next task and owner:
```

## Decisions

| Date | Decision |
| --- | --- |
| Oct 22 | Put the full RAG flow in the first working milestone |
| Oct 22 | Evaluate academic rules separately from generated explanations |
| Oct 22 | Begin with two reviewed directions and one job provider |
| Oct 22 | Keep opaque catalog requirements unknown until reviewed |
| Oct 22 | Use portable profile files before hosted accounts |
| Oct 22 | Use reported programming background and coursework when choosing foundations |
| Oct 22 | Keep learning stages separate from academic eligibility and preserve state through profile edits |
| Oct 22 | Retrieve source information automatically at runtime. Keep saved files as development references and prefer a temporary cache over a required course database |
| Oct 22 | Aim for source checks when a student submits a request. Any content database must also refresh automatically on a configurable schedule, with freshness and failed checks visible |
