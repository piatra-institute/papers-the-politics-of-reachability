# The Politics of Reachability

Institutional Landscapes and the Distribution of Agency.

Theories of freedom based on non-interference, resources or substantive opportunity do not capture the fact that institutions construct the paths by which intentions become consequential action, and that these paths, with their costs, risks and gatekeepers, are objects of power. We define freedom as reachability, the set of consequential states an agent can attain from its position through existing institutional pathways within its budget of money, time, risk and permission and compute it in a simulation. In a landscape of 6 pathways permitted to every agent, with a cheap consumption state reachable by all, the top budget decile reaches 6 pathways and the bottom five reach none, and the pathway modelled on open foundational infrastructure is reachable by 3 deciles of 10. When returns feed back on the landscape, the one appropriable pathway deepens and its alternatives silt: over 60 generations the entropy of chosen pathways falls from 1.69 bits to 0.21 with no change in law. Capping what returns may do to rival pathways preserves their reachability (18 pathway-deciles against 12) while the dominant pathway's share still concentrates. An incumbent spending returns on raising rivals' costs and capturing a grant office shrinks the reachable sets of 5 deciles while every consumer price stays fixed. Shared substrates raise reach from 19 to 49 pathway-deciles (open) or 45 (enclosed); after the steward fails, the open substrate retains all of its reach and the enclosed platform 0.56, although the platform wins when no one funds maintenance. Insurance against failure raises the number of deciles able to attempt any consequential pathway from 5 to 7.

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

Requires `pandoc` and `xelatex` on PATH. From the workspace you can also run `papers build the-politics-of-reachability`.

Part of [piatra-papers](https://github.com/piatra-institute). See the workspace docs for the research and writing pipelines.
