#!/usr/bin/env python3
"""
Extract alpha-carbon pairwise distances for each trajectory in an MSMBuilder metadata table.

"""

from __future__ import annotations

import argparse
import contextlib
from multiprocessing import Pool
from typing import Tuple

import mdtraj as md
import numpy as np
from msmbuilder.featurizer import AtomPairsFeaturizer
from msmbuilder.io import load_meta, preload_tops, save_trajs


def build_all_pairs(n_atoms: int) -> np.ndarray:
    pairs = [(i, j) for i in range(n_atoms) for j in range(i + 1, n_atoms)]
    return np.asarray(pairs, dtype=int)


def _featurize_one(args: Tuple[int, dict, dict, AtomPairsFeaturizer]):
    i, row, tops, featurizer = args
    traj = md.load(row["traj_fn"], top=tops[row["top_fn"]])
    feat = featurizer.partial_transform(traj)
    return i, feat


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--meta", default="meta.pandas.pickl", help="MSMBuilder metadata pickle")
    p.add_argument("--out", default="alpha_carbon", help="Output name for save_trajs")
    p.add_argument("--n_atoms", type=int, default=144, help="Number of alpha-carbon atoms")
    p.add_argument("--processes", type=int, default=32, help="Multiprocessing workers")
    args = p.parse_args()

    meta = load_meta(args.meta)
    tops = preload_tops(meta)

    pair_index = build_all_pairs(args.n_atoms)
    featurizer = AtomPairsFeaturizer(pair_index)

    with contextlib.closing(Pool(processes=args.processes)) as pool:
        work = ((i, row, tops, featurizer) for i, row in meta.iterrows())
        feats = dict(pool.imap_unordered(_featurize_one, work))

    save_trajs(feats, args.out, meta)
    print(f"[OK] Saved features to '{args.out}/' for {len(feats)} trajectories.")


if __name__ == "__main__":
    main()
