import streamlit as st

from f1analysis.cleaning import clean_laps
from f1analysis.pace import MIN_CLEAN_LAPS, relative_pace
from f1analysis.plots import driver_colors, lap_times_chart, pace_chart, team_colors

race = st.session_state["race"]
results = race.results
clean = clean_laps(race.laps)

st.title("Race pace")

# Relative pace
st.subheader("Pace relative to the field")
st.caption(
    "Each clean lap is compared with the median lap time of the whole field on the same lap, "
    "so that fuel load and track evolution affect everyone equally. Bars to the left of zero "
    "mean faster than the field. First laps, pit laps, laps under yellow flag or safety car "
    "and deleted laps are excluded."
)
pace = relative_pace(clean)
st.plotly_chart(pace_chart(pace, team_colors(results), MIN_CLEAN_LAPS), width="stretch")

# Lap times
st.subheader("Lap times")
st.caption("Clean laps only: gaps in the lines correspond to pit stops and excluded laps.")

finishing_order = results["Abbreviation"].tolist()
selected = st.multiselect("Drivers", finishing_order, default=finishing_order[:2])

if selected:
    st.plotly_chart(lap_times_chart(clean.pick_drivers(selected), driver_colors(results)), width="stretch")
else:
    st.info("Select at least one driver.")