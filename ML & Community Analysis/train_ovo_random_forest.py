#!/usr/bin/env python3
"""
Train a One-vs-One RandomForest classifier for one CV fold.

"""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsOneClassifier

from fibrin_ml.io_utils import load_crossvalidation_splits, stack_feature_files, stack_label_files


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--fold", type=int, default=0)
    p.add_argument("--depth", type=int, required=True)
    p.add_argument("--n_estimators", type=int, default=50)
    p.add_argument("--crossvalid", default="crossvalid.npy")
    p.add_argument("--feature_dir", default="alpha-carbon")
    p.add_argument("--label_dir", default="macromapping")
    p.add_argument("--out_dir", default="models/ovo_random_forest")
    args = p.parse_args()

    split = load_crossvalidation_splits(args.crossvalid, fold=args.fold)

    X_train = stack_feature_files(args.feature_dir, split.train_indices)
    y_train = stack_label_files(args.label_dir, split.train_indices)
    X_test = stack_feature_files(args.feature_dir, split.test_indices)
    y_test = stack_label_files(args.label_dir, split.test_indices)

    base = RandomForestClassifier(
        n_estimators=args.n_estimators,
        max_depth=args.depth,
        random_state=0,
        n_jobs=-1,
    )
    clf = OneVsOneClassifier(base)
    clf.fit(X_train, y_train)

    train_acc = float(np.mean(clf.predict(X_train) == y_train))
    test_acc = float(np.mean(clf.predict(X_test) == y_test))
    print(f"Fold: {args.fold} Depth {args.depth} Train Accu: {train_acc:.3f} Test Accu: {test_acc:.3f}")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"fold{args.fold}_depth{args.depth}.joblib"
    joblib.dump(clf, out_path)
    print(f"[OK] Saved model -> {out_path}")


if __name__ == "__main__":
    main()
