"""Race pace relative to the field"""

import pandas as pd

MIN_CLEAN_LAPS = 10


def relative_pace(clean: pd.DataFrame, min_clean_laps: int = MIN_CLEAN_LAPS) -> pd.DataFrame:
    """Median gap of each driver to the field on the same lap.

    Each clean lap is compared with the median lap time of all drivers on that lap,
    so that fuel load and track evolution affect everyone equally. Negative values
    mean faster than the field. Drivers with fewer than `min_clean_laps` clean laps
    are kept but marked with '*' in the Label column.
    """
    laps = clean.copy()
    field_median = laps.groupby("LapNumber")["LapTimeSeconds"].transform("median")
    laps["DeltaToField"] = laps["LapTimeSeconds"] - field_median

    pace = (
        laps.groupby(["Driver", "Team"])
        .agg(PaceDelta=("DeltaToField", "median"), CleanLaps=("DeltaToField", "count"))
        .reset_index()
        .sort_values("PaceDelta")
    )
    pace["Label"] = pace["Driver"].where(pace["CleanLaps"] >= min_clean_laps, pace["Driver"] + "*")
    return pace