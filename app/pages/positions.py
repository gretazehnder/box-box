import streamlit as st

from f1analysis.events import neutralisations                                 
from f1analysis.plots import add_neutralisations, driver_colors, positions_chart   
from f1analysis.positions import lap_positions

race = st.session_state["race"]
results = race.results
finishing_order = results["Abbreviation"].tolist()
teams = dict(zip(results["Abbreviation"], results["TeamName"]))
periods = neutralisations(race.laps, finishing_order[0])                      

st.title("Positions")
st.caption(
    "Position of each driver at the end of every lap, starting from the grid (lap 0). "
    "Highlighted drivers are shown in their team colour, with teammates distinguished by "
    "a dashed line; the rest of the field is shown in grey. Shaded areas mark safety car, "
    "virtual safety car and red flag periods."                                 
)

highlight = st.multiselect("Highlight drivers", finishing_order, default=finishing_order[:3])

fig = positions_chart(lap_positions(race.laps, results), driver_colors(results),
                      highlight, finishing_order, teams)
st.plotly_chart(add_neutralisations(fig, periods), width="stretch")          