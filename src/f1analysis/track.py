"""Track layout from telemetry: position, speed and sector of each point of a lap."""

import numpy as np
import pandas as pd


def lap_layout(lap) -> pd.DataFrame:
    """X/Y position, distance and speed along a lap, with the sector of each point.

    Each point is assigned to a sector by comparing its session time with the
    time the driver crossed the end of sectors 1 and 2.
    """
    tel = lap.get_telemetry()
    tel["Sector"] = np.select(
        [tel["SessionTime"] < lap["Sector1SessionTime"],
         tel["SessionTime"] < lap["Sector2SessionTime"]],
        [1, 2],
        default=3,
    )
    return tel[["X", "Y", "Distance", "Speed", "Sector"]]