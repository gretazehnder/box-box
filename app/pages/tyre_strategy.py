import pandas as pd
import streamlit as st

from f1analysis.cleaning import clean_laps
from f1analysis.plots import compound_colors, strategy_chart
from f1analysis.tyres import MIN_STINT_LAPS, degradation, stints

race = st.session_state["race"]
finishing_order = race.results["Abbreviation"].tolist()

st.title("Tyre strategy")

# Strategies
st.subheader("Strategies")
st.caption(
    "Each bar is a stint, coloured by tyre compound. Drivers are listed in finishing order; "
    "the number of segments in a row is the number of stops plus one."
)
race_stints = stints(race.laps, finishing_order)
st.plotly_chart(strategy_chart(race_stints, compound_colors(race), finishing_order), width="stretch")

# Degradation
st.subheader("Tyre degradation")
st.caption(
    "Seconds gained or lost per additional lap on the same tyres, from a straight line fitted "
    "to clean lap times. As the car also gets lighter while burning fuel, this is net degradation "
    f"and can be negative. Only stints with at least {MIN_STINT_LAPS} clean laps are shown."
)
deg = degradation(clean_laps(race.laps))
deg["Driver"] = pd.Categorical(deg["Driver"], categories=finishing_order, ordered=True)
table = (
    deg.sort_values(["Driver", "Stint"])
    .rename(columns={"SlopePerLap": "Seconds per lap"})
    [["Driver", "Team", "Stint", "Compound", "Laps", "Seconds per lap"]]
)
st.dataframe(
    table.style.format({"Stint": "{:.0f}", "Laps": "{:.0f}", "Seconds per lap": "{:+.3f}"}),
    hide_index=True,
    width="stretch",
)