"""Selection of laps that are representative of race pace"""

import pandas as pd


def lap_issues(laps: pd.DataFrame) -> pd.DataFrame:
    """Flag, for each lap, the reasons why it may not represent race pace.

    Returns one boolean column per issue, aligned with the input laps.
    """
    return pd.DataFrame({
        "First lap": laps["LapNumber"] == 1,
        "Pit in/out lap": laps["PitInTime"].notna() | laps["PitOutTime"].notna(),
        "Not green flag": laps["TrackStatus"] != "1",
        "Inaccurate": laps["IsAccurate"] == False,
        "Deleted": laps["Deleted"] == True,
        "No lap time": laps["LapTime"].isna(),
    })


def clean_laps(laps: pd.DataFrame) -> pd.DataFrame:
    """Keep only laps without any issue and add the lap time in seconds.

    No threshold on lap time is applied: slow laps of slower cars are genuine,
    and pace is compared through medians, which are robust to isolated slow laps.
    """
    clean = laps[~lap_issues(laps).any(axis=1)].copy()
    clean["LapTimeSeconds"] = clean["LapTime"].dt.total_seconds()
    return clean