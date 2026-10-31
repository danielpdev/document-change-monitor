# Demo walkthrough

## Start

```bash
make setup
make demo
make test
make eval
```

## What to show

A document update stores a new revision and replaces the current searchable text in one transaction. Search reads only active current versions; historical text stays in a separate revision table.

## Failure case to discuss

Unchanged content does not create revisions, old terms disappear after replacement, retired documents disappear from search and history remains available.

## Evidence

Open the JSON evaluation report alongside the implementation. Distinguish synthetic fixture outputs, synthetic trace timing, actual elapsed evaluation time, and local model inference. Do not present a tiny test set as a production benchmark.

## Closing tradeoff

The index is an on-read lexical scan for a tiny corpus, not a vector database. Full documents are kept in memory; large-source streaming is not implemented.

The repository's `docs/demo.webm` or `docs/demo.mp4`, when present, records the demonstration. A terminal replay is also available for focused projects as `docs/demo.cast`.
