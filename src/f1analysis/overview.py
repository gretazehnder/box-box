"""Key facts of a race: winner, fastest lap, best sectors, biggest gainer."""

import pandas as pd


def format_laptime(seconds: float) -> str:
    """Format seconds as m:ss.sss (e.g. 81.432 -> '1:21.432')."""
    minutes, rest = divmod(seconds, 60)
    return f"{int(minutes)}:{rest:06.3f}"


def valid_laps(laps: pd.DataFrame) -> pd.DataFrame:
    """Laps that count for records: not deleted for track limits."""
    return laps[laps["Deleted"] != True]


def fastest_lap(laps: pd.DataFrame) -> pd.Series:
    """The fastest valid lap of the session."""
    valid = valid_laps(laps)
    return valid.loc[valid["LapTime"].idxmin()]


def best_sectors(laps: pd.DataFrame) -> pd.DataFrame:
    """For each sector, the driver with the fastest valid time and that time."""
    valid = valid_laps(laps)
    rows = []
    for sector in (1, 2, 3):
        column = f"Sector{sector}Time"
        best = valid.loc[valid[column].idxmin()]
        rows.append({
            "Sector": sector,
            "Driver": best["Driver"],
            "Time": best[column].total_seconds(),
            "Lap": int(best["LapNumber"]),
        })
    return pd.DataFrame(rows)


def biggest_gainer(results: pd.DataFrame) -> pd.Series:
    """Classified driver who gained the most positions from the grid.

    Drivers starting from the pit lane have grid position 0 and are excluded.
    """
    classified = results[(results["GridPosition"] > 0) & results["Position"].notna()]
    gained = classified["GridPosition"] - classified["Position"]
    gainer = classified.loc[gained.idxmax()].copy()
    gainer["PositionsGained"] = int(gained.max())
    return gainer