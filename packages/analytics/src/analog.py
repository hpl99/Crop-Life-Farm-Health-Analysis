"""Analog Years matching algorithm for Nagpur crops.

Ranks past historical seasons by similarity to the current monsoon deficit,
showing how the crop actually performed in those specific historical seasons.
This is the primary farmer-facing decision aid.
"""

from typing import List, Dict, Any
import numpy as np
import pandas as pd


def find_analog_years(
    df_merged: pd.DataFrame,
    target_monsoon_rf_mm: float,
    normal_rf_mm: float = 936.1,
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """Find the top-k most similar past seasons based on monsoon rainfall deficit.

    df_merged columns expected:
    - crop_year (int)
    - yield_kg_ha (float)
    - monsoon_rf_mm (float)
    """
    clean_df = df_merged.dropna(subset=["crop_year", "yield_kg_ha", "monsoon_rf_mm"]).copy()
    if clean_df.empty:
        return []

    target_deficit_mm = target_monsoon_rf_mm - normal_rf_mm
    target_deficit_pct = (target_deficit_mm / normal_rf_mm) * 100.0

    # Compute deficit for each past year
    clean_df["deficit_mm"] = clean_df["monsoon_rf_mm"] - normal_rf_mm
    clean_df["deficit_pct"] = (clean_df["deficit_mm"] / normal_rf_mm) * 100.0

    # Distance to target deficit in mm
    clean_df["rf_distance"] = (clean_df["monsoon_rf_mm"] - target_monsoon_rf_mm).abs()

    # Sort by absolute distance
    sorted_df = clean_df.sort_values("rf_distance").head(top_k)

    analogs = []
    for _, row in sorted_df.iterrows():
        yr = int(row["crop_year"])
        rf = round(float(row["monsoon_rf_mm"]), 1)
        def_mm = round(float(row["deficit_mm"]), 1)
        def_pct = round(float(row["deficit_pct"]), 1)
        yld = round(float(row["yield_kg_ha"]), 1)

        analogs.append({
            "year": yr,
            "monsoon_rf_mm": rf,
            "deficit_mm": def_mm,
            "deficit_pct": def_pct,
            "yield_kg_ha": yld,
            "similarity_rank": len(analogs) + 1,
            "summary_en": f"Year {yr}: {rf}mm ({def_pct:+.1f}%), Yield {yld} kg/ha",
            "summary_mr": f"वर्ष {yr}: {rf} मिमी ({def_pct:+.1f}%), उत्पादन {yld} किग्रा/हेक्टर"
        })

    return analogs

