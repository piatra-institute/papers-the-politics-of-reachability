"""Orchestrator: reproduces every number and all four figures in the paper.

    cd simulation
    uv run run_all.py

Writes output/results.json and output/figures/*.png. Agent choice runs on a
recorded seed; everything else is expected-value arithmetic. A failed
invariant or a failed figure fails the run.
"""
from __future__ import annotations

import json
from pathlib import Path

from analyses import run

OUT = Path(__file__).parent / "output"


def main() -> None:
    (OUT / "figures").mkdir(parents=True, exist_ok=True)
    results = run()
    (OUT / "results.json").write_text(json.dumps(results, indent=2))

    from figures import (plot_missing_valley, plot_canalization,
                         plot_zero_price, plot_substrates)
    plot_missing_valley(results, str(OUT / "figures" / "missing_valley.png"))
    plot_canalization(results, str(OUT / "figures" / "canalization.png"))
    plot_zero_price(results, str(OUT / "figures" / "zero_price.png"))
    plot_substrates(results, str(OUT / "figures" / "substrates.png"))

    mv = results["missing_valley"]
    print(f"missing valley: {mv['permitted_paths_everyone']} pathways permitted "
          f"to all; top decile reaches {mv['top_decile_reach']}, bottom "
          f"{mv['bottom_decile_reach']}; missing: {mv['missing_valleys']}")
    ca = results["canalization"]
    u = ca["unbounded"]
    print(f"canalization: entropy {u['entropy_first']} -> {u['entropy_last']}; "
          f"canal share {u['venture_share_first']} -> {u['venture_share_last']}; "
          f"canal admits {u['venture_deciles_first']} -> {u['venture_deciles_last']} deciles; "
          f"capped entropy {ca['bounded']['entropy_last']}")
    zp = results["zero_price"]
    print(f"zero price: {zp['deciles_losing_reach']} deciles lose reach, "
          f"top change {zp['top_decile_change']}, prices unchanged")
    sb = results["substrates"]
    print("substrates:", {k: (sb[k]["population_reach"], sb[k]["crisis_retention"])
                          for k in ("flat", "open", "enclosed")})
    print(f"  routed through substrate: {sb['substrate_routing_share']}; "
          f"enclosed strictly wins at maintenance {sb['enclosed_strictly_wins_at']}, "
          f"ties at {sb['ties_at']}")
    fl = results["floor"]
    print(f"floor: deciles with any consequential path {fl['deciles_with_any_path_without_floor']} "
          f"-> {fl['deciles_with_any_path_with_floor']}; in the flat world "
          f"{fl['flat_world_deciles_without_floor']} -> {fl['flat_world_deciles_with_floor']}")
    print("checks:", f"{sum(results['checks'].values())}/{len(results['checks'])}")
    print("wrote", OUT / "results.json")


if __name__ == "__main__":
    main()
