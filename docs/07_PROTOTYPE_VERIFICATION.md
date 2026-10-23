# Prototype Verification

Checked October 22, 2026, Arizona time.

## Checks performed

| Check | Result |
| --- | --- |
| Clean Python environment | Installed `requirements-dev.txt` successfully on Python 3.12 |
| Automated tests | 54 passed, including five Streamlit interaction tests |
| Server startup | Health endpoint returned `ok`. Root page returned successfully |
| Official source importer | Fetched and parsed all five starter course entries |
| Keyword smoke evaluation | Five cases passed, each repeated 20 times |
| Real embedding/generation requests | Not run. No Gemini key configured |
| Real job request | Not run. No Adzuna credentials configured |
| Browser screenshot review | Pending. Chromium download failed in this environment |

The tests exercise changed goals, beginner foundations, completed-course filtering, rule logic, malformed inputs, citation rejection, provider failures, cache invalidation, profile files, and opportunity response handling. Provider and vector fixtures are controlled test data. They are not used to manufacture live app results.

## Reproduce locally

From the repository root, after installing dependencies:

```bash
python -m pytest -q
python scripts/evaluate.py --runs 20 --output output/keyword_smoke.json
python -m streamlit run app.py
```

In the browser, submit an incoming AI/ML profile with no programming background. ECE101 should appear as a next learning step and ECE425 as a later goal. Change the direction to embedded systems to see ECE372A as the later goal. Report programming experience or mark a foundation course complete to change that ordering. Completing a recommended course removes it from the candidate list.

The smoke evaluation measured approximately 0.35–0.38 milliseconds per request at the median across the five cases on this machine. This measures the small, in-memory keyword pipeline only. It excludes app rendering, network calls, model inference, installation, and cold startup. It is not a live RAG latency result or a research benchmark.

## Live RAG acceptance check

1. Configure `GEMINI_API_KEY` locally and confirm the model IDs available to the account.
2. Run `python scripts/build_index.py` to precompute real public-record embeddings.
3. Enable AI explanations and submit a profile.
4. Confirm a generated response, valid record/chunk references, and resolvable source links.
5. Inspect the exact context, actual vectors, cache state, and separate stage timings.
6. Repeat with a changed goal, completed course, and a question outside the collection.
7. Check the explanation against its sources. Reference validation alone does not prove that a claim is supported.

Record live measurements before using them in the report. A cold index build embeds records individually and can take longer. Later requests reuse the compatible index.

## Remaining limits

- All five official enrollment conditions are unknown pending review of their internal requirement references.
- The learning-stage annotations are team suggestions. They do not establish a semester plan or enrollment eligibility.
- Coverage is five courses, two learning resources, and two career mappings.
- Profiles use portable JSON files and session state. Hosted accounts and durable storage are pending.
- Source refresh produces review candidates. It does not silently replace approved academic data.
- Online resources are curated. Automated broad research and job-skill extraction are later work.
- The required six sample-paper reviews, held-out evaluation, and student pilot remain open.

## Next evidence to collect

Save a real RAG trace, provider/model configuration, reviewed rule example, live job result, browser screenshots, and the measured latency table. Use those artifacts for the midpoint report and narrated demonstration.
