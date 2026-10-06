from pathlib import Path

import fastf1
import pandas as pd

# cache/ folder at the repo root
CACHE_DIR = Path(__file__).resolve().parents[2] / "cache"


def enable_cache() -> None:
    CACHE_DIR.mkdir(exist_ok=True)
    fastf1.Cache.enable_cache(str(CACHE_DIR))


def get_schedule(year: int) -> pd.DataFrame:
    """Season calendar (tests excluded)."""
    enable_cache()
    return fastf1.get_event_schedule(year, include_testing=False)


def load_session(year: int, gp: str | int, kind: str = "R",
                 telemetry: bool = False) -> fastf1.core.Session:
    """Load a session: 'R' race, 'Q' qualifying, 'S' sprint, ...
    (only loaded when explicitly requested)."""
    enable_cache()
    session = fastf1.get_session(year, gp, kind)
    session.load(laps=True, telemetry=telemetry, weather=True, messages=True)
    return session