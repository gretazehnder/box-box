import streamlit as st

from f1analysis.cleaning import clean_laps
from f1analysis.pitstops import gap, pit_stops
from f1analysis.plots import driver_colors, gap_chart

race = st.session_state["race"]
finishing_order = race.results["Abbreviation"].tolist()

st.title("Pit stops")

# Time lost
st.subheader("Time lost in the pits")
st.caption(
    "Time lost in each stop: in-lap and out-lap compared with the driver's typical lap "
    "around the stop. It includes the whole pit lane, not only the time stationary."
)
stops = pit_stops(race.laps, clean_laps(race.laps))
st.dataframe(
    stops.sort_values("PitLoss")[["Driver", "Team", "LapNumber", "PitLoss"]]
    .rename(columns={"LapNumber": "Lap", "PitLoss": "Time lost (s)"})
    .style.format({"Lap": "{:.0f}", "Time lost (s)": "{:.1f}"}),
    hide_index=True,
    width="stretch",
)

# Gap
st.subheader("Gap between two drivers")
st.caption("Gap at the end of each lap: positive values mean the second driver is behind. "
           "Shaded areas mark the pit stops.")
col_a, col_b = st.columns(2)
driver_a = col_a.selectbox("Driver", finishing_order, index=0)
driver_b = col_b.selectbox("Compared with", finishing_order, index=1)

if driver_a == driver_b:
    st.info("Select two different drivers.")
else:
    st.plotly_chart(
        gap_chart(gap(race.laps, driver_a, driver_b), stops, driver_a, driver_b, driver_colors(race.results)),
        width="stretch",
    )