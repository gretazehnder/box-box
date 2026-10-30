import datetime

import streamlit as st

from f1analysis.data import FIRST_YEAR, available_events, load_session

st.set_page_config(page_title="Box Box", page_icon="🏁", layout="wide")


@st.cache_resource(show_spinner="Loading race data (the first time can take a minute)...")
def get_race(year: int, round_number: int):
    return load_session(year, round_number, telemetry=True)

# Race selection (sidebar, shared by all pages)
st.sidebar.title("🏁 Box Box")

years = list(range(datetime.date.today().year, FIRST_YEAR - 1, -1))
year = st.sidebar.selectbox("Season", years, index=years.index(2024))

events = available_events(year)
if events.empty:
    st.sidebar.warning("No races available yet for this season.")
    st.stop()

event_names = dict(zip(events["RoundNumber"], events["EventName"]))
rounds = list(event_names)
default_round = 16 if year == 2024 else rounds[-1]
round_number = st.sidebar.selectbox(
    "Grand Prix", rounds, index=rounds.index(default_round), format_func=event_names.get
)

try:
    st.session_state["race"] = get_race(year, round_number)
except RuntimeError as error:
    st.error(str(error))
    st.stop()

# Navigation (top bar) 
pages = [
    st.Page("pages/overview.py", title="Overview", icon=":material/flag:"),
    st.Page("pages/race_pace.py", title="Race pace", icon=":material/speed:"),
    st.Page("pages/tyre_strategy.py", title="Tyre strategy", icon=":material/tire_repair:"),
    st.Page("pages/pit_stops.py", title="Pit stops", icon=":material/timer:"),
    st.Page("pages/positions.py", title="Positions", icon=":material/leaderboard:"),
]
st.navigation(pages, position="top").run()