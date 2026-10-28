"""Baseline yield models for Nagpur crops.

Includes:
1. 5-year Olympic Average (dropping min and max observations over past 5 years).
2. Linear Trend Yield (capturing long-term technological and cultivar drift).
"""

from typing import List, Tuple, Dict, Any, Optional
import numpy as np
import pandas as pd


def compute_olympic_average(yields: List[float]) -> Optional[float]:
    """Compute Olympic average over a window (drops highest and lowest value).

    Standard WFP / USDA / PMFBY baseline technique. Requires at least 3 values,
    typically used with a 5-year window.
    """
    valid_yields = [y for y in yields if y is not None and not np.isnan(y) and y > 0]
    if len(valid_yields) < 3:
        return float(np.mean(valid_yields)) if valid_yields else None

    # Drop min and max
    sorted_vals = sorted(valid_yields)
    trimmed = sorted_vals[1:-1]
    return float(np.mean(trimmed))


def compute_rolling_olympic_baseline(df: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    """Compute historical rolling Olympic average for each year in the series.

    Expects df with columns ['crop_year', 'yield_kg_ha'] sorted by crop_year.
    """
    df = df.sort_values("crop_year").copy()
    olympic_vals = []

    for i in range(len(df)):
        if i == 0:
            olympic_vals.append(None)
        else:
            prev_window = df.iloc[max(0, i - window):i]["yield_kg_ha"].tolist()
            avg = compute_olympic_average(prev_window)
            olympic_vals.append(avg)

    df["baseline_olympic"] = olympic_vals
    return df

