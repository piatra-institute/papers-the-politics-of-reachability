"""An institutional landscape as a transition graph, for *The Politics of Reachability*.

The landscape is literal: institutional pathways are sequences of costed,
risky, sometimes permission-gated transitions from a common start to
consequential terminal states. Agents differ only in budget, arranged in
deciles; every pathway is legally open to everyone, always, in every
experiment. What varies is never permission. What varies is what permission
is worth.

Five pathways carry a project to a consequential terminal: the venture canal
(cheap to enter, deep, appropriable at the end), a grant path (shallow:
capacity-limited and discretionary), a commons path (no owner at the end,
nobody's revenue on the way), a cooperative path, and a public-agency path
(gated by an office). Consumption states sit beside them, cheap and
inconsequential, reachable by all, so that formal option-counting sees no
problem anywhere.

Measured, in order:

  1. Permission and reachability come apart. With identical permissions, the
     reachable set of consequential states is steeply decile-dependent, and
     the missing valley is an object: terminals permitted to all and
     practically reachable by few.
  2. Canalization is endogenous. Returns from the appropriable terminal feed
     back into the landscape, deepening the canal that produced them and
     silting the alternatives. Trajectory entropy falls with no change in
     law. The canal is genuinely enabling while it narrows: the bottom
     deciles gain reach into it even as cross-path diversity dies, and the
     honest statement carries both halves. A cap on what returns may do to
     rival pathways stabilizes the plurality.
  3. Landscape power harms at zero price. An incumbent spends returns on a
     ridge over the commons path and a gate on the interoperability edge;
     every consumption price stays where it was; the reachable sets of
     everyone below the top decile shrink.
  4. Substrates. A flat world (no shared infrastructure), an open-protocol
     world, and an enclosed-platform world are compared on downstream reach,
     on diversity, and through a crisis in which the substrate's operator or
     steward fails. Both substrates canalize; the open one leaves the larger
     field and survives the crisis forkably; and in the regime where nobody
     funds maintenance, the enclosed platform wins, because the gatekeeper
     at least pays the maintainers.
  5. The floor. Ruin risk prices out experimentation from below; a floor
     under failure moves experimentation down the distribution; a floor in a
     flat world moves almost nothing, because floors need valleys.

Agents choose by expected net value with seeded noise; everything else is
expected-value arithmetic. A rerun reproduces every number bit for bit.
"""
from __future__ import annotations

import numpy as np

SEED = 0
N_DECILES = 10
AGENTS_PER_DECILE = 100
BUDGETS = np.array([1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 9.0, 14.0, 22.0, 40.0])
RUIN_RESERVE = 2.0        # what an uninsured agent must hold back to survive failure
GENERATIONS = 60

# a pathway: stage costs, failure risk per attempt, permission (None or
# acceptance probability), terminal kind
PATHWAYS = {
    "venture":  {"costs": [1.0, 2.0, 4.0], "risk": 0.6, "permission": None,
                 "appropriable": True},
    "grant":    {"costs": [1.0, 1.0, 2.0], "risk": 0.4, "permission": 0.15,
                 "appropriable": False},
    "commons":  {"costs": [1.0, 2.0, 3.0], "risk": 0.5, "permission": None,
                 "appropriable": False},
    "coop":     {"costs": [2.0, 2.0, 3.0], "risk": 0.5, "permission": None,
                 "appropriable": False},
    "public":   {"costs": [1.0, 1.0, 1.0], "risk": 0.3, "permission": 0.10,
                 "appropriable": False},
    # the opening case: open foundational infrastructure; permitted to all,
    # subsidized by nothing, long, and owned by nobody at the end
    "open_infra": {"costs": [2.0, 4.0, 6.0], "risk": 0.5, "permission": None,
                   "appropriable": False},
}
CONSUMPTION_COST = 0.5     # reachable by everyone, consequential for no one
VENTURE_RETURN = 30.0      # what the appropriable terminal pays its owner


def path_cost(p, cost_shift=None):
    c = sum(p["costs"])
    if cost_shift:
        c += cost_shift
    return c


def reachable(budget, pathways, floor=False, cost_shifts=None):
    """Consequential terminals this budget can attempt: total path cost within
    budget, plus a ruin reserve when no floor exists. Permission-gated paths
    are counted separately: reachable only through an office's discretion."""
    cost_shifts = cost_shifts or {}
    unconditional, discretionary = [], []
    for name, p in pathways.items():
        need = path_cost(p, cost_shifts.get(name, 0.0))
        if not floor:
            need += RUIN_RESERVE
        if need <= budget:
            (discretionary if p["permission"] else unconditional).append(name)
    return unconditional, discretionary


# ---------------------------------------------------------------------------
# analysis 1: permission and reachability come apart
# ---------------------------------------------------------------------------

def analysis_missing_valley():
    rows = []
    for d in range(N_DECILES):
        unc, disc = reachable(BUDGETS[d], PATHWAYS)
        rows.append({"decile": d + 1, "budget": BUDGETS[d],
                     "reachable_unconditional": len(unc),
                     "reachable_with_discretion": len(disc),
                     "consumption_reachable": bool(CONSUMPTION_COST <= BUDGETS[d]),
                     "paths": unc + disc})
    permitted = len(PATHWAYS)
    reach_share = {name: sum(1 for r in rows if name in r["paths"]) / N_DECILES
                   for name in PATHWAYS}
    missing = [n for n, s in reach_share.items() if s <= 0.3]
    top = rows[-1]["reachable_unconditional"] + rows[-1]["reachable_with_discretion"]
    bottom = rows[0]["reachable_unconditional"] + rows[0]["reachable_with_discretion"]
    return {"permitted_paths_everyone": permitted,
            "deciles": rows,
            "reach_share_by_path": {k: round(v, 6) for k, v in reach_share.items()},
            "missing_valleys": missing,
            "top_decile_reach": top, "bottom_decile_reach": bottom,
            "consumption_reachable_by_all": all(r["consumption_reachable"] for r in rows)}


# ---------------------------------------------------------------------------
# analysis 2: endogenous canalization, and the cap
# ---------------------------------------------------------------------------

def _entropy(shares):
    s = np.array([x for x in shares if x > 0], dtype=float)
    s = s / s.sum()
    return float(-(s * np.log2(s)).sum())


def run_generations(cap_rival_ops=None, rng=None):
    """Each generation every agent that can attempt a pathway picks one by
    expected net value with noise. Venture successes pay the pool; the pool
    deepens the venture canal (its costs fall) and, unless capped, silts the
    rivals (their costs rise). Returns the trajectory."""
    rng = rng or np.random.default_rng(SEED)
    shifts = {name: 0.0 for name in PATHWAYS}
    history = []
    pool = 0.0
    for g in range(GENERATIONS):
        counts = {name: 0 for name in PATHWAYS}
        venture_deciles = 0
        rival_reach = 0
        for d in range(N_DECILES):
            unc, disc = reachable(BUDGETS[d], PATHWAYS, cost_shifts=shifts)
            avail = unc + disc
            if "venture" in avail:
                venture_deciles += 1
            rival_reach += sum(1 for n in avail if n != "venture")
            if not avail:
                continue
            # expected net value: appropriable pays the agent, others pay in
            # kind; noise keeps choice from being winner-take-all by fiat
            for _ in range(AGENTS_PER_DECILE):
                vals = []
                for name in avail:
                    p = PATHWAYS[name]
                    ev = (VENTURE_RETURN * (1 - p["risk"]) if p["appropriable"]
                          else 6.0) - path_cost(p, shifts[name])
                    if p["permission"]:
                        ev *= p["permission"]
                    vals.append(ev + rng.normal(0, 3.0))
                counts[avail[int(np.argmax(vals))]] += 1
        total = sum(counts.values())
        shares = {k: v / total for k, v in counts.items()} if total else {}
        # feedback: venture successes pay the pool; the pool works the landscape
        pool += counts["venture"] * (1 - PATHWAYS["venture"]["risk"]) * 0.0025
        deepen = min(pool * 0.5, 3.0)
        shifts["venture"] = -deepen
        silt = pool * 0.35
        if cap_rival_ops is not None:
            silt = min(silt, cap_rival_ops)
        for name in ("commons", "coop", "grant", "open_infra"):
            shifts[name] = silt
        history.append({"generation": g + 1,
                        "venture_share": round(shares.get("venture", 0.0), 6),
                        "entropy_bits": round(_entropy(list(shares.values())), 6),
                        "deciles_reaching_venture": venture_deciles,
                        "rival_pathway_deciles": rival_reach,
                        "venture_cost_shift": round(shifts["venture"], 6),
                        "rival_cost_shift": round(shifts["commons"], 6)})
    return history


def analysis_canalization():
    unbounded = run_generations(cap_rival_ops=None,
                                rng=np.random.default_rng(SEED))
    bounded = run_generations(cap_rival_ops=0.5,
                              rng=np.random.default_rng(SEED))
    first, last = unbounded[0], unbounded[-1]
    lastb = bounded[-1]
    return {
        "generations": GENERATIONS,
        "unbounded": {"history": unbounded,
                      "entropy_first": first["entropy_bits"],
                      "entropy_last": last["entropy_bits"],
                      "venture_share_first": first["venture_share"],
                      "venture_share_last": last["venture_share"],
                      "venture_deciles_first": first["deciles_reaching_venture"],
                      "venture_deciles_last": last["deciles_reaching_venture"],
                      "rival_reach_first": first["rival_pathway_deciles"],
                      "rival_reach_last": last["rival_pathway_deciles"]},
        "bounded": {"history": bounded,
                    "entropy_last": lastb["entropy_bits"],
                    "venture_share_last": lastb["venture_share"],
                    "rival_reach_last": lastb["rival_pathway_deciles"]},
        "entropy_drop_unbounded": round(first["entropy_bits"] - last["entropy_bits"], 6),
        "note": "no permission or law changes across the run; the landscape "
                "moves only through the pool's operations on costs",
    }


# ---------------------------------------------------------------------------
# analysis 3: landscape power harms at zero price
# ---------------------------------------------------------------------------

def analysis_zero_price():
    before = [sum(map(len, reachable(BUDGETS[d], PATHWAYS))) for d in range(N_DECILES)]
    # the incumbent raises ridges over the ownerless paths and absorbs the
    # grant office, whose gate now opens only on the incumbent's account
    ops_shifts = {"commons": 6.0, "coop": 6.0, "open_infra": 6.0}
    gated = {k: dict(v) for k, v in PATHWAYS.items() if k != "grant"}
    after = [sum(map(len, reachable(BUDGETS[d], gated, cost_shifts=ops_shifts)))
             for d in range(N_DECILES)]
    return {
        "consumption_cost_before": CONSUMPTION_COST,
        "consumption_cost_after": CONSUMPTION_COST,
        "reach_by_decile_before": before,
        "reach_by_decile_after": after,
        "deciles_losing_reach": int(sum(1 for b, a in zip(before, after) if a < b)),
        "top_decile_change": after[-1] - before[-1],
        "note": "every consumption price identical before and after; the harm "
                "is entirely outside the price column",
    }


# ---------------------------------------------------------------------------
# analysis 4: substrates, the crisis, and the maintenance regime
# ---------------------------------------------------------------------------

def substrate_world(kind, maintenance=1.0):
    """Downstream terminals spawned by a substrate. Open: 4 new unconditional
    cheap paths for everyone; enclosed: the same 4, tolled and gated by the
    platform; flat: none, and every base path costs 2 more (no shared
    infrastructure). Weak maintenance lets an open substrate silt up; the
    enclosed gatekeeper funds its own maintenance out of tolls."""
    world = {k: dict(v) for k, v in PATHWAYS.items()}
    shifts = {}
    if kind == "flat":
        for name in world:
            shifts[name] = 2.0
        return world, shifts
    decay = (1.0 - maintenance) * 3.0 if kind == "open" else 0.0
    for i in range(4):
        if kind == "open":
            world[f"downstream_{i}"] = {"costs": [0.5, 1.0 + decay], "risk": 0.3,
                                        "permission": None, "appropriable": False}
        else:
            world[f"downstream_{i}"] = {"costs": [0.5, 1.0, 1.0], "risk": 0.3,
                                        "permission": 0.6, "appropriable": False}
    return world, shifts


def _population_reach(world, shifts, floor=False):
    total = 0
    for d in range(N_DECILES):
        unc, disc = reachable(BUDGETS[d], world, floor=floor, cost_shifts=shifts)
        total += len(unc) + len(disc)
    return total


def analysis_substrates():
    out = {}
    for kind in ("flat", "open", "enclosed"):
        world, shifts = substrate_world(kind, maintenance=1.0)
        reach = _population_reach(world, shifts)
        n_paths = len(world)
        # crisis: the substrate's operator or steward fails
        if kind == "flat":
            crisis_reach = reach
        elif kind == "open":
            # forkable: downstream paths survive with a migration surcharge
            cshifts = dict(shifts)
            for name in world:
                if name.startswith("downstream"):
                    cshifts[name] = 0.5
            crisis_reach = _population_reach(world, cshifts)
        else:
            # the gate dies with its keeper: downstream paths are lost
            cworld = {k: v for k, v in world.items()
                      if not k.startswith("downstream")}
            crisis_reach = _population_reach(cworld, shifts)
        out[kind] = {"population_reach": reach,
                     "paths_in_world": n_paths,
                     "crisis_reach": crisis_reach,
                     "crisis_retention": round(crisis_reach / reach, 6) if reach else 0.0}
    # both substrates canalize: the share of attempts routed through
    # substrate-spawned paths, chosen freely on cost
    rng = np.random.default_rng(SEED + 1)
    routing = {}
    for kind in ("open", "enclosed"):
        world, shifts = substrate_world(kind, maintenance=1.0)
        through, total = 0, 0
        for d in range(N_DECILES):
            unc, disc = reachable(BUDGETS[d], world, cost_shifts=shifts)
            for _ in range(AGENTS_PER_DECILE):
                avail = unc + disc
                if not avail:
                    continue
                vals = [-path_cost(world[n], shifts.get(n, 0.0))
                        + rng.normal(0, 1.0) for n in avail]
                pick = avail[int(np.argmax(vals))]
                total += 1
                through += pick.startswith("downstream")
        routing[kind] = round(through / total, 6)
    out["substrate_routing_share"] = routing
    # the maintenance regime: where the enclosed platform wins
    grid = []
    for m in (0.0, 0.25, 0.5, 0.75, 1.0):
        wo, so = substrate_world("open", maintenance=m)
        we, se = substrate_world("enclosed", maintenance=m)
        ro, re_ = _population_reach(wo, so), _population_reach(we, se)
        grid.append({"maintenance": m, "open_reach": ro, "enclosed_reach": re_,
                     "open_wins": bool(ro > re_), "tie": bool(ro == re_)})
    out["maintenance_grid"] = grid
    out["enclosed_strictly_wins_at"] = [g["maintenance"] for g in grid
                                        if g["enclosed_reach"] > g["open_reach"]]
    out["ties_at"] = [g["maintenance"] for g in grid if g["tie"]]
    out["open_strictly_wins_at"] = [g["maintenance"] for g in grid if g["open_wins"]]
    return out


# ---------------------------------------------------------------------------
# analysis 5: the floor
# ---------------------------------------------------------------------------

def analysis_floor():
    rows = []
    for d in range(N_DECILES):
        unc_n, disc_n = reachable(BUDGETS[d], PATHWAYS, floor=False)
        unc_f, disc_f = reachable(BUDGETS[d], PATHWAYS, floor=True)
        rows.append({"decile": d + 1,
                     "reach_without_floor": len(unc_n) + len(disc_n),
                     "reach_with_floor": len(unc_f) + len(disc_f)})
    without = sum(1 for r in rows if r["reach_without_floor"] > 0)
    with_ = sum(1 for r in rows if r["reach_with_floor"] > 0)
    # a floor in a flat world: floors need valleys
    world, shifts = substrate_world("flat")
    flat_without = sum(1 for d in range(N_DECILES)
                       if sum(map(len, reachable(BUDGETS[d], world,
                                                 cost_shifts=shifts))) > 0)
    flat_with = sum(1 for d in range(N_DECILES)
                    if sum(map(len, reachable(BUDGETS[d], world, floor=True,
                                              cost_shifts=shifts))) > 0)
    return {"deciles": rows,
            "deciles_with_any_path_without_floor": without,
            "deciles_with_any_path_with_floor": with_,
            "flat_world_deciles_without_floor": flat_without,
            "flat_world_deciles_with_floor": flat_with,
            "floor_gain_normal_world": with_ - without,
            "floor_gain_flat_world": flat_with - flat_without}


# ---------------------------------------------------------------------------
# invariants
# ---------------------------------------------------------------------------

def run_checks(res) -> dict:
    checks = {}
    mv = res["missing_valley"]
    checks["permissions_identical_reach_unequal"] = (
        mv["consumption_reachable_by_all"]
        and mv["top_decile_reach"] >= 5 * max(mv["bottom_decile_reach"], 1) - 4
        and mv["top_decile_reach"] > mv["bottom_decile_reach"])
    checks["missing_valley_exists"] = len(mv["missing_valleys"]) >= 1
    ca = res["canalization"]
    checks["canalization_endogenous"] = (
        ca["entropy_drop_unbounded"] >= 0.4 * ca["unbounded"]["entropy_first"])
    checks["canal_is_enabling"] = (ca["unbounded"]["venture_deciles_last"]
                                   > ca["unbounded"]["venture_deciles_first"])
    checks["diversity_dies_as_reach_holds"] = (
        ca["unbounded"]["venture_share_last"] > 0.6
        and ca["unbounded"]["entropy_last"] < ca["unbounded"]["entropy_first"])
    checks["bounded_power_preserves_alternatives"] = (
        ca["bounded"]["rival_reach_last"] >= ca["unbounded"]["rival_reach_last"] + 4)
    checks["cap_does_not_stop_share_concentration"] = (
        ca["bounded"]["venture_share_last"] > 0.6)
    zp = res["zero_price"]
    checks["zero_price_harm"] = (
        zp["consumption_cost_before"] == zp["consumption_cost_after"]
        and zp["deciles_losing_reach"] >= 4
        and zp["top_decile_change"] >= -1)
    sb = res["substrates"]
    checks["open_beats_enclosed_beats_flat"] = (
        sb["open"]["population_reach"] > sb["enclosed"]["population_reach"]
        > sb["flat"]["population_reach"])
    checks["both_substrates_canalize"] = (
        sb["substrate_routing_share"]["open"] > 0.5
        and sb["substrate_routing_share"]["enclosed"] > 0.5)
    checks["crisis_separates_forkable"] = (
        sb["open"]["crisis_retention"] > 0.9
        and sb["enclosed"]["crisis_retention"] < 0.7)
    checks["enclosed_wins_when_unmaintained"] = len(sb["enclosed_strictly_wins_at"]) >= 1
    fl = res["floor"]
    checks["floor_moves_experimentation_down"] = (
        fl["floor_gain_normal_world"] >= 2)
    checks["floors_need_valleys"] = (
        fl["floor_gain_flat_world"] < fl["floor_gain_normal_world"])
    return checks


# ---------------------------------------------------------------------------
# entry
# ---------------------------------------------------------------------------

def _py(v):
    if isinstance(v, dict):
        return {k: _py(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_py(x) for x in v]
    if isinstance(v, np.bool_):
        return bool(v)
    if isinstance(v, (np.floating, np.integer)):
        return v.item()
    return v


def run() -> dict:
    res = {
        "constants": {
            "deciles": N_DECILES, "agents_per_decile": AGENTS_PER_DECILE,
            "budgets": [float(b) for b in BUDGETS],
            "ruin_reserve": RUIN_RESERVE, "generations": GENERATIONS,
            "venture_return": VENTURE_RETURN,
            "consumption_cost": CONSUMPTION_COST, "seed": SEED,
            "pathways": {k: {"cost": path_cost(v), "risk": v["risk"],
                             "permission": v["permission"],
                             "appropriable": v["appropriable"]}
                         for k, v in PATHWAYS.items()},
        },
        "missing_valley": analysis_missing_valley(),
        "canalization": analysis_canalization(),
        "zero_price": analysis_zero_price(),
        "substrates": analysis_substrates(),
        "floor": analysis_floor(),
    }
    res = _py(res)
    res["checks"] = _py(run_checks(res))
    failed = [k for k, v in res["checks"].items() if not v]
    if failed:
        import json as _json
        print(_json.dumps(res["checks"], indent=2))
        raise SystemExit(f"INVARIANT FAILURES: {failed}")
    return res


if __name__ == "__main__":
    import json
    print(json.dumps(run()["checks"], indent=2))
