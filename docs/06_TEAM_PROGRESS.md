# Team Progress

Updated October 22, 2026, Arizona time.

## Current implementation

The prototype includes the profile form, five real course summaries, two resources, keyword retrieval, academic-rule evaluation, profile export/import, a Gemini RAG adapter, evidence inspection, and an Adzuna adapter. Beginners see programming foundations before advanced learning goals. A student's background and completed courses can change that order.

**Live RAG is not yet verified.** No Gemini key is configured here. The pipeline passes tests using controlled provider responses. Live Adzuna requests also need a credentialed check.

All five current academic rules remain unknown because the catalog exposes internal requirement IDs. Course descriptions and credits were checked against official sources. Resolving those rules is separate work.

## Milestones

| Milestone | Owner | Status | Evidence / next step |
| --- | --- | --- | --- |
| M0: Setup and sources | To assign | Partial | Environment and records ready. Review sample papers and confirm provider access |
| M1: Complete RAG interaction | To assign | Partial | Pipeline and tests implemented. Run with a real key |
| M2: Checkpoint interface | To assign | Partial | Hybrid retrieval, inspector, plots, profile files implemented. Complete live demo and rule review |
| M3: Midpoint submission | Team | Open | Report, screenshots, narrated video |
| M4: Returning students | To assign | Partial | Portable files work. Hosted authentication/storage remain |
| M5: Opportunities | To assign | Partial | Adapter and interface implemented. Confirm credentials and results |
| M6: Coverage and updates | To assign | Partial | Five-source review importer works. Expand and review changed fields |
| M7: Final evaluation | Team | Open | Held-out cases, student pilot, presentation |

## Verification

- Clean installation from pinned dependencies succeeded.
- 54 automated tests passed, including five Streamlit interaction tests.
- Streamlit started successfully and returned an `ok` health response and its root page.
- The importer fetched and parsed all five official course entries.
- All five keyword smoke cases passed, covering beginners, experienced students, changed goals, and completed coursework.
- Provider behavior was tested with controlled responses, not live credentials.

See [prototype verification](07_PROTOTYPE_VERIFICATION.md) for commands, timing scope, and limitations.

## Next work session

1. Configure a Gemini key and verify the model IDs.
2. Precompute the index and record a real generated answer with citations.
3. Resolve and review the five enrollment requirement references.
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
