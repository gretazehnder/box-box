import pandas as pd
import streamlit as st

from f1analysis.overview import best_sectors, biggest_gainer, fastest_lap, format_laptime
from f1analysis.plots import driver_colors, team_colors, track_sector_map, track_speed_map
from f1analysis.track import lap_layout

race = st.session_state["race"]
results = race.results
event = race.event
drivers = driver_colors(results)
teams = team_colors(results)

st.title(f"{event['EventName']} {event.year}")
st.caption(f"{event['Location']}, {event['Country']} · {event['EventDate']:%d %B %Y}")


def card(column, label, value, detail, color=None):
    with column.container(border=True):
        st.caption(label)
        style = f"color:{color};" if color else ""
        st.markdown(f"<h3 style='{style}margin:0'>{value}</h3>", unsafe_allow_html=True)
        st.caption(detail)


# --- Key facts ---
winner = results.iloc[0]
fastest = fastest_lap(race.laps)
sectors = best_sectors(race.laps)
gainer = biggest_gainer(results)

columns = st.columns(6)
card(columns[0], "Winner", winner["Abbreviation"], winner["TeamName"],
     drivers.get(winner["Abbreviation"]))
card(columns[1], "Fastest lap", fastest["Driver"],
     f"{format_laptime(fastest['LapTime'].total_seconds())} · L{int(fastest['LapNumber'])}",
     drivers.get(fastest["Driver"]))
for i, sector in sectors.iterrows():
    card(columns[2 + i], f"Best sector {sector['Sector']}", sector["Driver"],
         f"{sector['Time']:.3f} s · L{sector['Lap']}", drivers.get(sector["Driver"]))
card(columns[5], "Biggest gainer", gainer["Abbreviation"],
     f"P{int(gainer['GridPosition'])} → P{int(gainer['Position'])} (+{gainer['PositionsGained']})",
     drivers.get(gainer["Abbreviation"]))

map_column, table_column = st.columns(2, gap="large")

# --- Track map ---
with map_column:
    layout = lap_layout(fastest)
    corners = race.get_circuit_info().corners
    view = st.segmented_control("Track map", ["Speed", "Best sectors"], default="Speed")
    if view == "Best sectors":
        st.caption("Track split into the three timing sectors, coloured by the driver with the best time.")
        fig = track_sector_map(layout, sectors, drivers, corners)
    else:
        st.caption(f"Speed along the fastest lap of the race ({fastest['Driver']}, lap {int(fastest['LapNumber'])}).")
        fig = track_speed_map(layout, corners)
    st.plotly_chart(fig, use_container_width=True)

# --- Classification ---
with table_column:
    table = pd.DataFrame({
        "Pos": results["ClassifiedPosition"],
        "Driver": results["FullName"],
        "Team": results["TeamName"],
        "Grid": results["GridPosition"].astype(int),
        "+/−": (results["GridPosition"] - results["Position"]).astype(int),
        "Status": results["Status"],
        "Points": results["Points"],
    })

    def team_style(team):
        return f"color: {teams.get(team, '')}; font-weight: 600"

    styled = (
        table.style
        .apply(lambda col: [team_style(team) for team in table["Team"]], subset=["Driver", "Team"])
        .format({"+/−": "{:+d}", "Points": "{:g}"})
    )
    st.caption("Final classification")
    st.dataframe(styled, hide_index=True, use_container_width=True, height=(len(table) + 1) * 35 + 3)