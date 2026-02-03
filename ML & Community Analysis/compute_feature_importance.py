#!/usr/bin/env python3
"""
Compute aggregate feature importance from an OVO model with tree estimators.

"""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True, help="Path to saved OVO model (.joblib/.pkl)")
    p.add_argument("--out_dir", default="outputs/feature_importance")
    p.add_argument("--plot", action="store_true")
    args = p.parse_args()

    clf = joblib.load(args.model)

    n_feat = len(clf.estimators_[0].feature_importances_)
    imp = np.zeros(n_feat, dtype=float)
    for est in clf.estimators_:
        imp += est.feature_importances_
    imp /= len(clf.estimators_)

    order = np.argsort(imp)[::-1]
    cum = np.cumsum(imp[order])

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(
        {"feature_index": np.arange(n_feat), "importance": imp, "importance_percent": 100.0 * imp}
    ).sort_values("importance", ascending=False)
    df.to_csv(out_dir / "feature_importance.csv", index=False)
    np.savez(out_dir / "feature_importance.npz", importance=imp, order=order, cumulative=cum)

    if args.plot:
        import matplotlib.pyplot as plt

        x = np.arange(1, n_feat + 1)
        plt.figure()
        plt.plot(x, cum)
        plt.xlabel("Top-N features (sorted)")
        plt.ylabel("Cumulative importance")
        plt.tight_layout()
        plt.savefig(out_dir / "cumulative_importance.png", dpi=200)

    print(f"[OK] Wrote outputs to {out_dir}")


if __name__ == "__main__":
    main()
