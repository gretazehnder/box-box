"""Track layout from telemetry: position, speed and sector of each point of a lap."""

import numpy as np
import pandas as pd


def lap_layout(lap) -> pd.DataFrame:
    """X/Y position, distance and speed along a lap, with the sector of each point.

    Sector boundaries are found from the time the driver crossed them
    (Sector1SessionTime, Sector2SessionTime).
    """
    tel = lap.get_telemetry()
    s1_end = tel.loc[tel["SessionTime"] >= lap["Sector1SessionTime"], "Distance"].iloc[0]
    s2_end = tel.loc[tel["SessionTime"] >= lap["Sector2SessionTime"], "Distance"].iloc[0]
    tel["Sector"] = np.select([tel["Distance"] < s1_end, tel["Distance"] < s2_end], [1, 2], default=3)
    return tel[["X", "Y", "Distance", "Speed", "Sector"]]