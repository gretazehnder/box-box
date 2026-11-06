"""Race neutralisations (safety car, virtual safety car, red flag) from track status."""

import pandas as pd

# Track status codes: 4 = Safety Car, 5 = Red Flag, 6 = VSC deployed, 7 = VSC ending
NEUTRALISATIONS = {
    "Safety Car": {"4"},
    "Virtual Safety Car": {"6", "7"},
    "Red Flag": {"5"},
}


def _consecutive(lap_numbers: list[int]) -> list[list[int]]:
    """Group sorted lap numbers into runs of consecutive laps, e.g. [3, 4, 5, 9] -> [[3, 4, 5], [9]]."""
    groups = []
    for lap in lap_numbers:
        if groups and lap == groups[-1][-1] + 1:
            groups[-1].append(lap)
        else:
            groups.append([lap])
    return groups


def neutralisations(laps: pd.DataFrame, reference_driver: str) -> pd.DataFrame:
    """Periods of safety car, virtual safety car and red flag, as lap ranges.

    Lap numbers refer to `reference_driver` (usually the winner), since at the same
    moment drivers can be on different laps. A lap's TrackStatus lists every status
    seen during that lap (e.g. "14" = green, then safety car).
    """
    reference = laps[(laps["Driver"] == reference_driver) & laps["TrackStatus"].notna()]
    periods = []
    for label, codes in NEUTRALISATIONS.items():
        affected = sorted(
            int(lap["LapNumber"]) for _, lap in reference.iterrows()
            if set(str(lap["TrackStatus"])) & codes
        )
        for group in _consecutive(affected):
            periods.append({"Type": label, "StartLap": group[0], "EndLap": group[-1]})
    return pd.DataFrame(periods, columns=["Type", "StartLap", "EndLap"]).sort_values("StartLap")