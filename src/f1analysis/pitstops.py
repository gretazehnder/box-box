"""Pit stops: time lost in each stop and gap between two drivers"""

import pandas as pd


def pit_stops(laps: pd.DataFrame, clean: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    """Time lost in each pit stop.

    A stop affects the in-lap (with PitInTime) and the out-lap (with PitOutTime).
    The time lost is compared with the driver's median clean lap within `window`
    laps before and after the stop.
    """
    all_laps = laps.copy()
    all_laps["LapTimeSeconds"] = all_laps["LapTime"].dt.total_seconds()

    in_laps = all_laps[all_laps["PitInTime"].notna()][["Driver", "Team", "LapNumber", "LapTimeSeconds"]]
    out_laps = all_laps[all_laps["PitOutTime"].notna()][["Driver", "LapNumber", "LapTimeSeconds"]].copy()
    out_laps["LapNumber"] -= 1  # align each out-lap with the in-lap before it

    stops = in_laps.merge(out_laps, on=["Driver", "LapNumber"], suffixes=("In", "Out"))

    # a race may have no valid pit stops (e.g. a red flag where tyres are changed on the grid)
    if stops.empty:
        return stops.assign(ReferenceLap=pd.Series(dtype=float), PitLoss=pd.Series(dtype=float))

    def reference_lap(stop):
        nearby = clean[
            (clean["Driver"] == stop["Driver"])
            & clean["LapNumber"].between(stop["LapNumber"] - window, stop["LapNumber"] + window + 1)
        ]
        return nearby["LapTimeSeconds"].median()

    stops["ReferenceLap"] = stops.apply(reference_lap, axis=1)
    stops["PitLoss"] = stops["LapTimeSecondsIn"] + stops["LapTimeSecondsOut"] - 2 * stops["ReferenceLap"]
    return stops


def gap(laps: pd.DataFrame, driver_a: str, driver_b: str) -> pd.DataFrame:
    """Gap of driver_b to driver_a at the end of each lap (positive: driver_b behind)."""
    lap_end = laps.pivot(index="LapNumber", columns="Driver", values="Time")
    return (lap_end[driver_b] - lap_end[driver_a]).dt.total_seconds().rename("Gap").reset_index()