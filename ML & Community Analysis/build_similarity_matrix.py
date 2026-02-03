#!/usr/bin/env python3
"""
Build a symmetric similarity matrix from a 1D importance vector.

Cleaned from legacy '9-matrix.py'.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--importance", required=True, help=".npy vector or .npz with key 'importance'")
    p.add_argument("--n_atoms", type=int, default=144)
    p.add_argument("--out", default="outputs/sim_mtx.npy")
    args = p.parse_args()

    imp_path = Path(args.importance)
    if imp_path.suffix == ".npz":
        imp = np.load(str(imp_path))["importance"]
    else:
        imp = np.load(str(imp_path))

    n = args.n_atoms
    sim = np.zeros((n, n), dtype=float)

    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if count >= len(imp):
                raise ValueError(f"importance too short: need {n*(n-1)//2}, got {len(imp)}")
            sim[i, j] = imp[count]
            sim[j, i] = imp[count]
            count += 1

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    np.save(out, sim)
    print(f"[OK] Saved similarity matrix -> {out}")


if __name__ == "__main__":
    main()
