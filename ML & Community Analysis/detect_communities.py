#!/usr/bin/env python3
"""
Community detection by minimizing within-community cost for a similarity matrix.

"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np


def cost(bags: Dict[int, List[int]], sim: np.ndarray) -> float:
    t = 0.0
    for k, nodes in bags.items():
        for i in range(len(nodes)):
            for j in range(i, len(nodes)):
                t += float(sim[nodes[i], nodes[j]])
    return t


def local_cost(nodes: List[int], sim: np.ndarray) -> np.ndarray:
    out = np.zeros(len(nodes), dtype=float)
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            out[i] += float(sim[nodes[i], nodes[j]])
    return out


def rem_cost(l1: List[int], l2: List[int], sim: np.ndarray) -> np.ndarray:
    out = np.zeros(len(l1), dtype=float)
    for i in range(len(l1)):
        for j in range(len(l2)):
            out[i] += float(sim[l1[i], l2[j]])
    return out


def insert(bags: Dict[int, List[int]], i: int, j: int, m: int) -> None:
    bags[i].remove(m)
    bags[j].append(m)


def swap(bags: Dict[int, List[int]], i: int, j: int, m: int, n: int) -> None:
    bags[i].remove(m)
    bags[j].append(m)
    bags[j].remove(n)
    bags[i].append(n)


def maximum_bcost(bcost: Dict[int, Dict[int, np.ndarray]], ncluster: int) -> Tuple[float, int, int]:
    bmax, ei, ej = -1.0, 0, 0
    for i in range(ncluster):
        for j in range(ncluster):
            v = float(np.max(bcost[i][j]))
            if v > bmax:
                bmax, ei, ej = v, i, j
    return bmax, ei, ej


def maximum_ex_cost(ex: Dict[int, Dict[int, np.ndarray]], ncluster: int) -> Tuple[float, int, int, int, int]:
    best, ei, ej, pi, pj = -1.0, 0, 0, 0, 0
    for i in range(ncluster):
        for j in range(i + 1, ncluster):
            v = float(np.max(ex[i][j]))
            if v > best:
                best, ei, ej = v, i, j
                arg = int(np.argmax(ex[i][j]))
                pi = arg // ex[i][j].shape[1]
                pj = arg % ex[i][j].shape[1]
    return best, ei, ej, pi, pj


def local_min(bags: Dict[int, List[int]], sim: np.ndarray, nclusters: int) -> Dict[int, List[int]]:
    while True:
        old = cost(bags, sim)

        l_cost = {i: local_cost(bags[i], sim) for i in range(nclusters)}
        r_cost = {i: {j: rem_cost(bags[i], bags[j], sim) for j in range(nclusters)} for i in range(nclusters)}
        b_cost = {i: {j: l_cost[i] - r_cost[i][j] for j in range(nclusters)} for i in range(nclusters)}

        ex_cost: Dict[int, Dict[int, np.ndarray]] = {i: {} for i in range(nclusters)}
        for i in range(nclusters):
            for j in range(i + 1, nclusters):
                ex = np.zeros((len(b_cost[i][j]), len(b_cost[j][i])))
                for p in range(len(b_cost[i][j])):
                    for q in range(len(b_cost[j][i])):
                        n1, n2 = bags[i][p], bags[j][q]
                        ex[p, q] = sim[n1, n2] * 2 + b_cost[i][j][p] + b_cost[j][i][q]
                ex_cost[i][j] = ex

        maxb, ei, ej = maximum_bcost(b_cost, nclusters)
        maxex, xi, xj, xp, xq = maximum_ex_cost(ex_cost, nclusters)

        if maxb <= 0 and maxex <= 0:
            break

        if maxb > 0:
            n = bags[ei][int(np.argmax(b_cost[ei][ej]))]
            insert(bags, ei, ej, n)
        else:
            n1 = bags[xi][xp]
            n2 = bags[xj][xq]
            swap(bags, xi, xj, n1, n2)

        new = cost(bags, sim)
        if new > old + 1e-12:
            raise RuntimeError("Cost increased unexpectedly")

    return bags


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--sim", default="outputs/sim_mtx.npy")
    p.add_argument("--nclusters", type=int, required=True)
    p.add_argument("--restarts", type=int, default=2000)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--out", default="outputs/communities.json")
    args = p.parse_args()

    sim = np.load(args.sim)
    nodes = sim.shape[0]
    rng = random.Random(args.seed)

    best_bags = None
    best_cost = float("inf")

    interval = nodes // args.nclusters
    uniform = {i: list(range(interval * i, interval * (i + 1))) for i in range(args.nclusters - 1)}
    uniform[args.nclusters - 1] = list(range(interval * (args.nclusters - 1), nodes))
    uniform = local_min(uniform, sim, args.nclusters)
    best_bags = uniform
    best_cost = cost(uniform, sim)

    for r in range(args.restarts):
        all_nodes = list(range(nodes))
        rng.shuffle(all_nodes)
        bags = {i: all_nodes[interval * i : interval * (i + 1)] for i in range(args.nclusters - 1)}
        bags[args.nclusters - 1] = all_nodes[interval * (args.nclusters - 1) :]
        bags = local_min(bags, sim, args.nclusters)
        c = cost(bags, sim)
        if c < best_cost:
            best_cost = c
            best_bags = {k: list(v) for k, v in bags.items()}
        if (r + 1) % max(1, args.restarts // 10) == 0:
            print(f"[{r+1}/{args.restarts}] best_cost={best_cost:.6f}")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump({str(k): sorted(set(v)) for k, v in best_bags.items()}, f, indent=2)

    print("[OK] Best cost:", best_cost)
    print("[OK] Saved ->", out)


if __name__ == "__main__":
    main()
