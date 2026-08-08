"""Figures for *The Politics of Reachability*. Each reads the results dict and writes one PNG.

Palette (CVD-checked in a prior validation; direct labels and line styles as
secondary encoding): amber, green, blue, warm gray; red reserved for harm.
"""
from __future__ import annotations

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK = "#1a1a1a"
GRID = "#d9d9d9"
AMBER = "#b45309"
GREEN = "#15803d"
BLUE = "#2563eb"
GRAY = "#57534e"
RED = "#b3202c"


def _style(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(INK)
    ax.tick_params(colors=INK, labelsize=9)
    ax.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)


def plot_missing_valley(res: dict, path: str) -> None:
    mv = res["missing_valley"]
    fl = res["floor"]
    x = np.arange(1, 11)
    unc = [r["reachable_unconditional"] for r in mv["deciles"]]
    disc = [r["reachable_with_discretion"] for r in mv["deciles"]]
    with_floor = [r["reach_with_floor"] for r in fl["deciles"]]
    fig, ax = plt.subplots(figsize=(8.2, 3.8))
    ax.bar(x - 0.2, unc, 0.38, color=BLUE, label="reachable outright")
    ax.bar(x - 0.2, disc, 0.38, bottom=unc, color="#9db8e8",
           label="reachable through an office's discretion")
    ax.bar(x + 0.2, with_floor, 0.38, color=GREEN,
           label="reachable with a floor under failure")
    ax.axhline(mv["permitted_paths_everyone"], color=INK, lw=1.0, ls="--")
    ax.text(5.6, mv["permitted_paths_everyone"] + 0.15,
            "pathways permitted to every decile", fontsize=8.5, color=INK)
    ax.set_xticks(x)
    ax.set_xlabel("budget decile", fontsize=9)
    ax.set_ylabel("consequential pathways reachable", fontsize=9)
    ax.set_ylim(0, 7.2)
    ax.set_title("permission is flat; reachability is not", fontsize=10, color=INK)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    _style(ax)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_canalization(res: dict, path: str) -> None:
    ca = res["canalization"]
    hu = ca["unbounded"]["history"]
    hb = ca["bounded"]["history"]
    g = [h["generation"] for h in hu]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.8, 3.8))
    a1.plot(g, [h["entropy_bits"] for h in hu], "-", color=RED, lw=1.8,
            label="pathway entropy, unbounded returns")
    a1.plot(g, [h["entropy_bits"] for h in hb], "--", color=GREEN, lw=1.8,
            label="entropy, rival operations capped")
    a1.set_xlabel("generation", fontsize=9)
    a1.set_ylabel("entropy of chosen pathways (bits)", fontsize=9)
    a1.set_title("the landscape narrows with no change in law",
                 fontsize=10, color=INK)
    a1.legend(frameon=False, fontsize=8.5, loc="upper right")
    a2.plot(g, [h["rival_pathway_deciles"] for h in hu], "-", color=RED,
            lw=1.8, label="unbounded returns")
    a2.plot(g, [h["rival_pathway_deciles"] for h in hb], "--", color=GREEN,
            lw=1.8, label="rival operations capped")
    a2.set_xlabel("generation", fontsize=9)
    a2.set_ylabel("pathway-deciles reachable outside the canal", fontsize=9)
    a2.set_title("what the cap preserves is the exit, never the share",
                 fontsize=10, color=INK)
    a2.legend(frameon=False, fontsize=8.5, loc="lower left")
    for ax in (a1, a2):
        _style(ax)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_zero_price(res: dict, path: str) -> None:
    zp = res["zero_price"]
    x = np.arange(1, 11)
    fig, ax = plt.subplots(figsize=(7.8, 3.7))
    ax.bar(x - 0.19, zp["reach_by_decile_before"], 0.36, color=BLUE,
           label="before the incumbent's operations")
    ax.bar(x + 0.19, zp["reach_by_decile_after"], 0.36, color=RED,
           label="after: ridges raised, the grant office absorbed")
    ax.set_xticks(x)
    ax.set_xlabel("budget decile", fontsize=9)
    ax.set_ylabel("consequential pathways reachable", fontsize=9)
    ax.set_title("every consumer price unchanged; the harm is here",
                 fontsize=10, color=INK)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    _style(ax)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_substrates(res: dict, path: str) -> None:
    sb = res["substrates"]
    kinds = ["flat", "open", "enclosed"]
    labels = ["flat\n(no substrate)", "open\nprotocol", "enclosed\nplatform"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.7))
    x = np.arange(3)
    reach = [sb[k]["population_reach"] for k in kinds]
    crisis = [sb[k]["crisis_reach"] for k in kinds]
    a1.bar(x - 0.19, reach, 0.36, color=BLUE, label="population reach")
    a1.bar(x + 0.19, crisis, 0.36, color=GRAY,
           label="reach after the steward fails")
    for i, k in enumerate(kinds):
        a1.text(i + 0.19, crisis[i] + 0.8, f"{sb[k]['crisis_retention']:.2f}",
                ha="center", fontsize=8.5, color=INK)
    a1.set_xticks(x)
    a1.set_xticklabels(labels, fontsize=8.5)
    a1.set_ylabel("pathway-deciles reachable", fontsize=9)
    a1.set_title("both substrates canalize; one is forkable",
                 fontsize=10, color=INK)
    a1.legend(frameon=False, fontsize=8, loc="upper left")
    gridm = sb["maintenance_grid"]
    m = [g["maintenance"] for g in gridm]
    a2.plot(m, [g["open_reach"] for g in gridm], "o-", color=GREEN, lw=1.8,
            label="open substrate")
    a2.plot(m, [g["enclosed_reach"] for g in gridm], "s--", color=AMBER,
            lw=1.8, label="enclosed substrate")
    a2.set_xlabel("public maintenance funding", fontsize=9)
    a2.set_ylabel("population reach", fontsize=9)
    a2.set_title("the gatekeeper at least pays the maintainers",
                 fontsize=10, color=INK)
    a2.legend(frameon=False, fontsize=8.5, loc="lower right")
    for ax in (a1, a2):
        _style(ax)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
