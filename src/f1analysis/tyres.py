"""Tyre strategies: stints and degradation"""

import numpy as np
import pandas as pd

MIN_STINT_LAPS = 8


def stints(laps: pd.DataFrame, driver_order: list[str]) -> pd.DataFrame:
    """One row per stint: driver, compound, first and last lap, number of laps.

    All laps are used (not only clean ones), since reconstructing a strategy
    needs the first lap and the pit laps too. Drivers follow `driver_order`.
    """
    result = (
        laps.groupby(["Driver", "Stint", "Compound"])
        .agg(StartLap=("LapNumber", "min"), EndLap=("LapNumber", "max"), Laps=("LapNumber", "count"))
        .reset_index()
    )
    result["Driver"] = pd.Categorical(result["Driver"], categories=driver_order, ordered=True)
    return result.sort_values(["Driver", "Stint"]).reset_index(drop=True)


def degradation(clean: pd.DataFrame, min_stint_laps: int = MIN_STINT_LAPS) -> pd.DataFrame:
    """Net degradation of each stint: slope of lap time against tyre age (s per lap).

    The slope includes the fuel effect, so it can be negative. Stints with fewer
    than `min_stint_laps` clean laps are skipped.
    """
    def slope(stint):
        if len(stint) < min_stint_laps:
            return pd.Series({"Laps": len(stint), "SlopePerLap": np.nan})
        value = np.polyfit(stint["TyreLife"], stint["LapTimeSeconds"], 1)[0]
        return pd.Series({"Laps": len(stint), "SlopePerLap": value})

    return (
        clean.groupby(["Driver", "Team", "Stint", "Compound"])
        .apply(slope, include_groups=False)
        .reset_index()
        .dropna(subset=["SlopePerLap"])
    )