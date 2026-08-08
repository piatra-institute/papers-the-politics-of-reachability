# The Politics of Reachability

Institutional Landscapes and the Distribution of Agency. The paper develops an account of freedom as reachability, the set of consequential states an agent can actually attain from its position through existing institutional pathways within its budget of money, time, risk, and permission, and computes the account's objects in a simulated landscape. With 6 pathways permitted identically to everyone and a consumption state reachable by all, reach runs from 6 pathways at the top budget decile to 0 for the bottom five, and the pathway modeled on open foundational infrastructure is reachable by 3 deciles of 10: the missing valley measured. Returns feeding back into the landscape collapse pathway entropy from 1.69 bits to 0.21 over 60 generations with no change in law; capping operations against rival pathways preserves the reachability of alternatives while the canal's share concentrates anyway, so the cap protects the exit rather than the share. An incumbent's ridge-raising and office-capture shrink 5 deciles' reachable sets with every consumer price unchanged, the harm an option-space conception of competition sees and a price conception cannot. Both an open protocol and an enclosed platform canalize, routing over 0.9 of attempts through themselves; the open one leaves the larger field (49 pathway-deciles to 45) and survives its steward's failure at 1.0 retention against 0.56, while the enclosed platform strictly wins in exactly one regime, zero maintenance funding, because the gatekeeper at least pays the maintainers. A floor under failure moves the capacity to attempt anything consequential from 5 deciles to 7; in a flat world it moves 4 to 5, because floors need valleys. The politics: bound landscape power, build plural forkable pathways, fund stewardship, keep the landscape revisable.

## Simulation

```bash
cd simulation
uv run run_all.py        # -> output/results.json + output/figures/*.png
```

Agent choice runs on a recorded seed; everything else is expected-value arithmetic. Fourteen invariant checks fail the run loudly if broken, among them: permission flat while reach is a staircase; the entropy collapse endogenous with no law change; the canal genuinely admitting more deciles as it deepens; the cap preserving alternatives without stopping share concentration; the zero-price harm to 5 deciles; both substrates canalizing while only the forkable one survives its steward; the enclosed platform's strict win at zero maintenance; and the floor's dependence on valleys.

## Build

```bash
uv run build.py          # -> paper/PAPER.pdf  (vendored canonical recipe)
```

Requires `pandoc` and `xelatex` on PATH. From the workspace you can also run
`papers build the-politics-of-reachability`.

Part of [piatra-papers](https://github.com/piatra-institute). See the workspace
docs for the research and writing pipelines.
