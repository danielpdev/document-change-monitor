# Design record

## Decision

A document update stores a new revision and replaces the current searchable text in one transaction. Search reads only active current versions; historical text stays in a separate revision table.

## Failure model

Unchanged content does not create revisions, old terms disappear after replacement, retired documents disappear from search and history remains available.

## Tradeoffs

The index is an on-read lexical scan for a tiny corpus, not a vector database. Full documents are kept in memory; large-source streaming is not implemented.

## Next change to defend in review

Add an asynchronous embedding index with version fences and content-source polling.

## Reproducibility

`uv.lock` pins Python dependencies; the web lockfile pins the React build where present. Model-backed evaluations use a separately installed local service. Dataset examples are synthetic and intentionally small. Reported timing is a local observation, not a throughput SLA. Run `make test` after changing state transitions and `make eval` after changing decisions. Keep inference quality separate from deterministic invariant checks.
