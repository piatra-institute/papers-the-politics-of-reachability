# Audit

Dated log of editorial passes and verification runs. Newest first.

## 2026-09-23 — structured-evidence migration

Structured-evidence migration (references and claims).
- references.yaml: 28 CSL entries. 11 resolved through doi.org content negotiation (Crossref) and checked for year, title and authors; 17 entered by hand (twelve books without DOIs, Deleuze and Hayek with JSTOR stable URLs, Zittrain, the CERN public-domain statement as cern1993 and the Digital Markets Act as eu2022). In-text citations converted to Pandoc [@id]; the legacy list replaced by the citeproc-rendered list (Chicago author-date).
- Correction: "The reachable sets of 5 deciles shrink, with the largest losses in deciles 6 to 8" -> "in deciles 7 and 8"; results.json /zero_price shows deciles 7 and 8 losing three pathways each and decile 6 losing one, like deciles 9 and 10.
- claims.yaml: 55 claims (38 computation, 2 source, 3 definition, 2 assumption, 7 interpretation, 3 normative). Every model number in abstract and body bound to results.json. Source claims checked against Crossref/OpenAlex abstracts (Cerf and Kahn's protocol; Winters and Page's material-power definition compatible with democracy).
- Unverified, not bound: the CERN release date (CERN Document Server blocks automated retrieval; relies on the earlier recorded fetch); Leiner et al. on public funding and plurality (the abstract describes the paper, not its content); Robeyns on democratic grounds independent of desert (abstract gives political equality but not desert); Arthur, Ostrom 2010 and Waddington 1942 (no abstract retrieved); Zittrain, Deleuze, Hayek and the book sources (Berlin, Sen, Gibson, Pettit, Waddington 1957, Pistor, Polanyi, Kauffman, Strange, Winters 2011, Anderson, Rawls, Ostrom 1990, Mazzucato, Unger), and the DMA interoperability statement.
- Run: reachability (uv run python run_all.py); results.json reproduced byte for byte.
- metadata claims_target: claim-ledger.

## 2026-09-23 — prose revision

Prose rewritten against the house standards. Headings made descriptive (Introduction, Freedom as reachability, Institutional landscapes, Open infrastructure and the venture pathway, Model design, Reachable sets and endogenous narrowing, Landscape power, Shared substrates, Insurance against failure, Design principles, Objections, Reproducibility).

Corrections found during the pass:
  - The text said that at generation 60 "18 pathway-deciles outside the canal survive under the cap, against 15 without it". results.json gives canalization.unbounded.rival_reach_last = 12; now "18 against 12".
  - "Over 0.9 of attempts route through the substrate" was stated for both worlds; the enclosed world is exactly 0.90. Now "at least 0.9 (0.97 open, 0.90 enclosed)".
  - The maintenance comparison is now stated as a grid of funding levels (enclosed strictly wins at 0, ties at 0.25 to 0.75, open wins at 1.0).
results.json unchanged by the figure edits.

## 2026-08-08 — v1, first full draft to publication

Scope: the entire paper, simulation, and evidence base, from the seed chat to publication.

Changes:
  - Sources: 28 entries verified against Crossref, OpenLibrary, or the live record (CERN CDS record 1164399 and EUR-Lex fetched live; Zittrain's locator confirmed via Harvard DASH). Cut from the seed and logged: Varoufakis/Žižek (commentary), Jessop (Strange carries the lineage), programme self-descriptions (STA/ARIA/NGI), the seed's wider constellation (Hirschman, Stiegler, Simondon, Wiener, Beer, Friston), and the Thatcher-era parliamentary material per the brief's do-not-become list.
  - Simulation design iterations logged: the missing valley needed the seed's own opening case added as a pathway (open foundational infrastructure) before the concept had a referent; the bounded-power invariant was rewritten from entropy-stabilization to the sharper, honest metric after the first run showed the cap cannot stop share concentration (the canal wins by genuinely improving) and preserves only the reachability of alternatives, which is the paper's own concept applied to itself; the maintenance grid's ties at 0.25–0.75 were reported as ties rather than counted as wins; landscape operations needed teeth (ridges + office capture) before the zero-price harm reached below one decile.
  - Voice: draft came in at 1 error (an epanorthosis) and 2 negate-pivots, all rewritten; "exactly" thinned 4 to 2. The seed's prose was not reused.

Verification:
  - voice: 0 errors, 0 review-candidates
  - refs: 28 in-text keys, 28 bib entries, 0 missing, 0 unused (CERN spelled out for the matcher)
  - claims: 328 sim values, 9 decimal claims in prose, 0 without a match
  - build: 12 pages, no missing-character warnings
  - simulation: 14/14 invariants
  - check => PASS
