# Packet A — Literature and GitHub prior-art lock

## Goal

Complete the pre-outcome evidence record for the exact use case: LLM extraction of forward-looking FX news sentiment and deterministic trading-rule evaluation.

## Required scope

At minimum fresh-read:

- SNB Working Paper 2025/11;
- Lopez-Lira & Tang JFE 2026 / current paper version;
- FINSABER paper, repository documentation, relevant issue/commit evidence where available;
- information-leakage / post-cutoff evaluation work;
- at least one repository/benchmark designed specifically to detect financial look-ahead.

## Questions

1. What task is the LLM actually doing?
2. Which findings require fine-tuning rather than off-the-shelf prompting?
3. What exact temporal alignment is used?
4. Are transaction costs included?
5. What failed in broader/longer replications?
6. Which evaluation controls are consistently recommended?
7. Is EUR/JPY selection defensible from prior art without repository outcome search?

## Deliverables

- update `PRIOR_ART.md`;
- evidence table with source, claim, evidence level, limitations;
- search/retrieval log;
- explicit list of claims that are not established.

## Prohibited

- historical EURJPY performance calculation;
- prompt/provider parameter search using market outcomes;
- current live trade recommendation.
