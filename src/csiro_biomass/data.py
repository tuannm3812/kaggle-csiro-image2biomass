from __future__ import annotations

import os
from pathlib import Path

import pandas as pd


def find_data_dir() -> Path:
    """Find competition data in the Kaggle notebook input mount."""
    candidates = [
        "/kaggle/input/competitions/csiro-biomass",
        "/kaggle/input/csiro-biomass",
        os.environ.get("CSIRO_DATA_DIR"),
        "data/csiro-biomass",
        "input/csiro-biomass",
    ]
    for candidate in candidates:
        if not candidate:
            continue
        path = Path(candidate)
        if (path / "train.csv").exists() and (path / "test.csv").exists():
            return path
    raise FileNotFoundError(
        "Could not find competition data. Expected /kaggle/input/competitions/csiro-biomass."
    )


def read_competition_data(data_dir: str | Path | None = None) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    root = Path(data_dir) if data_dir is not None else find_data_dir()
    train = pd.read_csv(root / "train.csv")
    test = pd.read_csv(root / "test.csv")
    sample_submission = pd.read_csv(root / "sample_submission.csv")
    return train, test, sample_submission


def image_path(data_dir: str | Path, relative_path: str) -> Path:
    return Path(data_dir) / relative_path
