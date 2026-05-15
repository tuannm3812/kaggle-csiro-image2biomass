from __future__ import annotations

import numpy as np
import pandas as pd

TARGET_WEIGHTS: dict[str, float] = {
    "Dry_Green_g": 0.1,
    "Dry_Dead_g": 0.1,
    "Dry_Clover_g": 0.1,
    "GDM_g": 0.2,
    "Dry_Total_g": 0.5,
}


def weighted_r2_score(
    y_true: np.ndarray | pd.Series,
    y_pred: np.ndarray | pd.Series,
    weights: np.ndarray | pd.Series,
) -> float:
    """Competition-style global weighted R2."""
    y_true_arr = np.asarray(y_true, dtype=float)
    y_pred_arr = np.asarray(y_pred, dtype=float)
    weight_arr = np.asarray(weights, dtype=float)

    if not (len(y_true_arr) == len(y_pred_arr) == len(weight_arr)):
        raise ValueError("y_true, y_pred, and weights must have the same length")

    weighted_mean = np.average(y_true_arr, weights=weight_arr)
    ss_res = np.sum(weight_arr * np.square(y_true_arr - y_pred_arr))
    ss_tot = np.sum(weight_arr * np.square(y_true_arr - weighted_mean))
    return float(1.0 - ss_res / ss_tot) if ss_tot > 0 else 0.0


def add_target_weights(df: pd.DataFrame, target_col: str = "target_name") -> pd.DataFrame:
    """Return a copy with the competition row weight for each target row."""
    out = df.copy()
    out["weight"] = out[target_col].map(TARGET_WEIGHTS)
    if out["weight"].isna().any():
        missing = sorted(out.loc[out["weight"].isna(), target_col].unique())
        raise ValueError(f"Unknown target names: {missing}")
    return out
