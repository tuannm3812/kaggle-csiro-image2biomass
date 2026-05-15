from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageStat
from tqdm.auto import tqdm


def extract_image_features(image_paths: list[Path], image_size: int = 256) -> pd.DataFrame:
    """Extract lightweight color and texture features from image files."""
    rows: list[dict[str, float | str]] = []

    for path in tqdm(image_paths, desc="image features"):
        row: dict[str, float | str] = {"image_path": str(path)}
        try:
            image = Image.open(path).convert("RGB")
            row["width"], row["height"] = image.size
            small = image.resize((image_size, image_size))
            arr = np.asarray(small, dtype=np.float32) / 255.0
            stat = ImageStat.Stat(small)

            for idx, channel in enumerate("rgb"):
                row[f"{channel}_mean"] = float(stat.mean[idx] / 255.0)
                row[f"{channel}_std"] = float(stat.stddev[idx] / 255.0)
                row[f"{channel}_p10"] = float(np.quantile(arr[:, :, idx], 0.10))
                row[f"{channel}_p50"] = float(np.quantile(arr[:, :, idx], 0.50))
                row[f"{channel}_p90"] = float(np.quantile(arr[:, :, idx], 0.90))

            green = arr[:, :, 1]
            red = arr[:, :, 0]
            blue = arr[:, :, 2]
            row["excess_green"] = float(np.mean(2 * green - red - blue))
            row["green_red_ratio"] = float(np.mean(green / (red + 1e-4)))
            row["visible_ndvi_proxy"] = float(np.mean((green - red) / (green + red + 1e-4)))
            row["brightness"] = float(np.mean(arr))
            row["contrast"] = float(np.std(arr))
        except Exception as exc:
            row["image_error"] = str(exc)
        rows.append(row)

    return pd.DataFrame(rows)


def add_calendar_features(df: pd.DataFrame, date_col: str = "Sampling_Date") -> pd.DataFrame:
    out = df.copy()
    if date_col not in out.columns:
        return out
    dates = pd.to_datetime(out[date_col], errors="coerce")
    out["sample_month"] = dates.dt.month
    out["sample_dayofyear"] = dates.dt.dayofyear
    out["sample_year"] = dates.dt.year
    return out
