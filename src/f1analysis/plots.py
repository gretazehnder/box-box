"""Shared colours and plot style, used by both the notebooks and the app."""

import fastf1.plotting
import pandas as pd
import plotly.express as px

TEMPLATE = "plotly_dark"
FALLBACK_COLOR = "#888888"


def _hex(color) -> str:
    """FastF1 stores colours without '#', and some sessions have none."""
    return f"#{color}" if isinstance(color, str) and color else FALLBACK_COLOR


def team_colors(results: pd.DataFrame) -> dict[str, str]:
    """Official colour of each team, e.g. {'Ferrari': '#E80020'}."""
    return {team: _hex(color) for team, color in zip(results["TeamName"], results["TeamColor"])}


def driver_colors(results: pd.DataFrame) -> dict[str, str]:
    """Colour of each driver, i.e. their team colour, e.g. {'LEC': '#E80020'}."""
    return {driver: _hex(color) for driver, color in zip(results["Abbreviation"], results["TeamColor"])}


def compound_colors(session) -> dict[str, str]:
    """Pirelli colour of each tyre compound."""
    return fastf1.plotting.get_compound_mapping(session=session)


# --- Track maps ---

def _style_track(fig, corners: pd.DataFrame):
    """Common style for track maps: real proportions, no axes, numbered corners."""
    fig.update_traces(marker_size=5)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False, scaleanchor="x", scaleratio=1)
    fig.update_layout(template=TEMPLATE, margin=dict(l=0, r=0, t=10, b=0),
                      legend=dict(orientation="h", y=-0.02, title=None))
    for _, corner in corners.iterrows():
        fig.add_annotation(x=corner["X"], y=corner["Y"], text=f"{corner['Number']}{corner['Letter']}",
                           showarrow=False, font_size=11, xshift=12, yshift=12)
    return fig


def track_speed_map(layout: pd.DataFrame, corners: pd.DataFrame):
    """Track coloured by speed along a lap."""
    fig = px.scatter(
        layout, x="X", y="Y", color="Speed",
        color_continuous_scale="YlOrRd",
        hover_data={"Speed": ":.0f", "X": False, "Y": False},
        labels={"Speed": "km/h"},
    )
    return _style_track(fig, corners)


def track_sector_map(layout: pd.DataFrame, sectors: pd.DataFrame,
                     colors: dict[str, str], corners: pd.DataFrame):
    """Track split into the three sectors, each coloured by the driver with the best time."""
    labels = {row.Sector: f"S{row.Sector} · {row.Driver} {row.Time:.3f}s" for row in sectors.itertuples()}
    color_map = {labels[row.Sector]: colors.get(row.Driver, FALLBACK_COLOR) for row in sectors.itertuples()}
    data = layout.assign(Best=layout["Sector"].map(labels))
    fig = px.scatter(
        data, x="X", y="Y", color="Best",
        color_discrete_map=color_map,
        category_orders={"Best": list(labels.values())},
        hover_data={"Best": True, "X": False, "Y": False},
    )
    return _style_track(fig, corners)