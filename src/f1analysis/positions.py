"""Race positions lap by lap, starting from the grid"""

import pandas as pd


def lap_positions(laps: pd.DataFrame, results: pd.DataFrame) -> pd.DataFrame:
    """Position of each driver at the end of every lap, with the grid as lap 0."""
    grid = (
        results[["Abbreviation", "GridPosition"]]
        .rename(columns={"Abbreviation": "Driver", "GridPosition": "Position"})
        .dropna(subset=["Position"])
    )
    # Drivers starting from the pit lane have grid position 0. They start behind everyone else, so they are placed last on the grid
    grid.loc[grid["Position"] == 0, "Position"] = len(results)
    grid = grid.assign(LapNumber=0)

    return pd.concat([grid, laps[["Driver", "LapNumber", "Position"]]], ignore_index=True)