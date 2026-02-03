#!/usr/bin/env python3
"""
MiniBatchKMeans clustering of 2D RMSD features and saving labels per run.

"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from sklearn.cluster import MiniBatchKMeans


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--x", default="rmsd_dark.npy")
    p.add_argument("--y", default="light_rmsd.npy")
    p.add_argument("--n_clusters", type=int, default=300)
    p.add_argument("--n_runs", type=int, default=36)
    p.add_argument("--frames_per_run", type=int, default=999)
    p.add_argument("--out_dir", default="outputs/kmeans_labels")
    args = p.parse_args()

    x = np.load(args.x)
    y = np.load(args.y)
    if len(x) != len(y):
        raise ValueError("x and y must have same length")

    data = np.column_stack([x, y])
    km = MiniBatchKMeans(n_clusters=args.n_clusters, random_state=0)
    labels = km.fit_predict(data)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    np.save(out_dir / "labels_all.npy", labels)

    for i in range(args.n_runs):
        s = i * args.frames_per_run
        e = (i + 1) * args.frames_per_run
        np.save(out_dir / f"run{i:02d}.npy", labels[s:e])

    print(f"[OK] Saved labels -> {out_dir}")


if __name__ == "__main__":
    main()
