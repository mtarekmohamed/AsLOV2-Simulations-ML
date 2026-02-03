#!/usr/bin/env python3
"""
Train an MLP classifier for one CV fold.

"""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import numpy as np
from sklearn.neural_network import MLPClassifier

from fibrin_ml.io_utils import load_crossvalidation_splits, stack_feature_files, stack_label_files


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--fold", type=int, required=True)
    p.add_argument("--alpha_log10", type=int, required=True, help="alpha = 10**alpha_log10")
    p.add_argument("--crossvalid", default="crossvalid.npy")
    p.add_argument("--feature_dir", default="alpha_carbon_fs")
    p.add_argument("--label_dir", default="macro-mapping")
    p.add_argument("--out_dir", default="models/neural_network")
    args = p.parse_args()

    alpha = 10 ** int(args.alpha_log10)
    split = load_crossvalidation_splits(args.crossvalid, fold=args.fold)

    X_train = stack_feature_files(args.feature_dir, split.train_indices)
    y_train = stack_label_files(args.label_dir, split.train_indices)
    X_test = stack_feature_files(args.feature_dir, split.test_indices)
    y_test = stack_label_files(args.label_dir, split.test_indices)

    clf = MLPClassifier(alpha=alpha, hidden_layer_sizes=(400, 200, 100), random_state=1, max_iter=200)
    clf.fit(X_train, y_train)

    train_acc = float(np.mean(clf.predict(X_train) == y_train))
    test_acc = float(np.mean(clf.predict(X_test) == y_test))
    print(f"Fold: {args.fold} Alpha 1e{args.alpha_log10} Train Accu: {train_acc:.3f} Test Accu: {test_acc:.3f}")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"fold{args.fold}_alpha1e{args.alpha_log10}.joblib"
    joblib.dump(clf, out_path)
    print(f"[OK] Saved model -> {out_path}")


if __name__ == "__main__":
    main()
