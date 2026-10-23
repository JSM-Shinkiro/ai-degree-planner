# Technical Design

## Stack

| Component | Starting choice |
| --- | --- |
| Interface | Python, Streamlit, Plotly |
| Semantic retrieval | Gemini Embedding 2 adapter, NumPy cosine ranking |
| Keyword and hybrid retrieval | BM25, Reciprocal Rank Fusion |
| Explanations | Configurable Gemini adapter, pending live access test |
| Records and validation | JSON, Pydantic, explicit citation checks |
| Academic rules | Python predicates and three-state evaluation |
| Profiles | Export/import first, then authenticated durable storage |
| Opportunities | One job API, initially Adzuna if access and coverage work |

Use one Python application. A separate frontend service and vector database are unnecessary for the initial collection. Model IDs are configurable and the tested top-level dependencies are pinned.

## Code organization

| Module | Responsibility |
| --- | --- |
| app.py | Forms, action buttons, and rendered results |
| src/models.py | Validated data contracts |
| src/catalog.py / src/ingest.py | Reviewed collection, evidence chunks, and source parsing |
| src/providers.py | Gemini calls, vectors, and versioned embedding cache |
| retrieval.py | BM25, semantic ranking, fusion, and deduplication |
| rules.py | Prerequisite evaluation |
| src/service.py | Query construction, context assembly, generation, and citation validation |
| app.py / src/retrieval.py | Inspection UI, scores, and embedding projection |
| profiles.py / jobs.py | Saved progress and opportunity search |

Provider calls run only after explicit actions, behind service adapters. Scripts build the index, refresh source candidates, and run smoke evaluation. Reviewed records and synthetic test fixtures are separate.

## Data design

The table describes the intended record design. The starter schema is smaller. It has source dates/hashes, course summaries and credits, rules, team topic/stage annotations, profile background, evidence IDs, and cache manifests. Publication dates, costs, skill mapping reviews, and durable profile IDs need further work. Public prerequisite wording is not yet resolved, so those conditions stay unknown.

| Record | Main fields |
| --- | --- |
| Source | ID, URL, title, type, retrieval time, publication time if known, catalog edition, hash, review status |
| Course | ID, exact code, edition, title, description, confirmed credits, source IDs, original prerequisite text, structured rule, reviewed skill links |
| Resource | ID, title, provider, URL, topic, level, known cost, source IDs, check date |
| Career direction | ID, reviewed skills, course/resource mappings, supporting rationale and sources, job query terms |
| Student | Profile ID, standing, catalog edition if known, interests, goal, completed courses, whether the history is complete, optional experience/current enrollment |
| Evidence chunk | Chunk ID, record ID, source ID, text, section locator, hash, edition, review status |
| Index manifest | Corpus hash, ordered chunk IDs/hashes, model, dimensions, normalization, format version, build time |

Course identity includes its catalog edition. Preserve suffixes and cross-listings. A graduate entry cannot automatically substitute for an undergraduate record.

Career mappings are reviewed team annotations. They are not official guarantees about employment. Retrieval time and publication time remain separate.

## Prerequisite rules

Support AND and OR conditions, course completion, minimum grades, completion-or-concurrent enrollment, standing, consent, and unknown conditions.

Return **satisfied**, **unsatisfied**, or **unknown**, with reasons and source references.

- For AND, any unsatisfied child makes the result unsatisfied. Otherwise, an unknown child makes it unknown.
- For OR, any satisfied child makes the result satisfied. Otherwise, an unknown child makes it unknown.
- Reject empty logical groups as malformed data.
- If a declared complete history lacks a required course, that completion condition is unsatisfied. If the history is incomplete, absence remains unknown.
- A missing required grade, unverified equivalency, or unsupported rule remains unknown.
- Respect alternatives and co-requisites when arranging a learning order. Flag cycles.

The roadmap suggests learning order. It does not establish official enrollment eligibility or complete a degree audit. The first implementation prioritizes foundations for students who report being new to programming and have no listed foundation course. It marks advanced matches as later goals. These stage annotations are team decisions, not catalog prerequisites.

## Request and output boundaries

The retrieval stage returns chunk/record IDs, method, rank, and the relevant scores. The context object stores the exact evidence sent to the generator, allowed record IDs, rule results, prompt version, and budget use.

The generated response contains:

```text
status: answered or insufficient_evidence
recommendations:
  - record_id
  - reasons:
      - text
      - claim_type: source_fact or recommendation
      - evidence_ids
clarification: optional text
```

Validate the structure, allowed IDs, evidence membership, citation resolution, and duplicate recommendations. Evidence must support the recommended record and any stated career connection. The generator cannot replace prerequisite results.

## Configuration, caching, and storage

Use configuration for providers, model IDs, dimensions, retrieval method, candidate count, context budget, recommendation count, timeouts, data version, and explicit fixture mode. Keep secrets outside source control.

Cache index data by corpus and model configuration. Request caches include the relevant profile, query, prompt, model, and data versions. Updating completed coursework invalidates dependent recommendations.

Session State supports the current interaction. The final hosted pilot needs durable profiles associated with authenticated users. Choose the hosting, sign-in, and database path after the local baseline works.

Job results contain provider/query metadata, retrieval time, listing IDs, titles, employers, locations, original application links, available posting dates, and descriptions as supplied. Distinguish snippets from full descriptions. Start with a roughly 20-minute cache, subject to provider terms.
