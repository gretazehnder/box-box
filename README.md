# Box, Box

How are Formula 1 races won (and lost)? This project analyses lap-by-lap race data (pace, tyre strategy and degradation, pit stops, positions and telemetry) and presents it in an interactive Streamlit app.

<img width="2560" height="1242" alt="image" src="https://github.com/user-attachments/assets/d15b204b-d0a2-44e6-9ad9-82dfb28aa3fd" />



## Contents

| Part | What it does |
|---|---|
| `notebooks/01_data_exploration.ipynb` | Explores the data available through FastF1: schedule, sessions, laps, results and telemetry |
| `notebooks/02_race_analysis.ipynb` | Case study of the 2024 Italian Grand Prix (Monza): pace, tyres, pit stops, positions and telemetry |
| `src/f1analysis/` | Reusable analysis code shared by the notebooks and the app |
| `app/` | Streamlit app to explore any race from 2018 onwards |

## Key findings (Monza 2024)

- Leclerc won with a one-stop strategy, while both McLarens stopped twice: track position and low tyre degradation beat raw pace.
- On clean laps, the McLarens were among the fastest cars, but the extra stop cost them more time than their pace advantage could recover.
- The gap chart between Leclerc and Piastri shows where the race was decided: the second McLaren stop handed the lead back to Ferrari.

## The app

The app has five pages. They share a sidebar where the season and the Grand Prix are selected.

| Page | Content |
|---|---|
| **Overview** | Winner, fastest lap, best sectors, biggest gainer, a track map (speed or best sector per driver), the final classification, and the safety car, VSC and red flag periods |
| **Race pace** | Pace of each driver relative to the field on clean laps, and lap times for the selected drivers |
| **Tyre strategy** | Stints and compounds for every driver, and the degradation of each stint in seconds per lap |
| **Pit stops** | Time lost in each pit stop, and the gap between two drivers lap by lap |
| **Positions** | Position of every driver lap by lap, from the starting grid to the flag |

The lap times, gap and positions charts show a coloured strip above the plot for safety car, virtual safety car and red flag periods.

<details>
<summary><b>Other pages</b></summary>

| Screenshots of main plots from the other pages|
|---|
| **Race pace** |
| <img width="1460" height="450" alt="image" src="https://github.com/user-attachments/assets/963ee03c-0d40-4303-8da9-f2ed55eef25e" /> |
| **Tyre strategy** |
| <img width="1460" height="600" alt="image" src="https://github.com/user-attachments/assets/b0752206-f96e-4adc-bbf4-8e54371cb4cd" /> |
| **Pit stops** |
| <img width="1460" height="450" alt="image" src="https://github.com/user-attachments/assets/76f5c8fe-6fc7-4b2c-9f19-1c02527b5d00" /> |
| **Positions** | 
| <img width="1460" height="600" alt="image" src="https://github.com/user-attachments/assets/6f3567ba-d3c8-497c-af9e-47dec342f335" /> |

</details>

## Methods

- **Clean laps**: first laps, in and out laps, laps under yellow flag, safety car or red flag, inaccurate laps, deleted laps and laps without a time are excluded.
- **Relative pace**: each lap is compared with the median of the field on the same lap, so changes in fuel load and track conditions affect every driver in the same way. Drivers with fewer than 10 clean laps are marked with `*`.
- **Tyre degradation**: slope of a linear fit of lap time against tyre age within each stint, in seconds per lap. Stints shorter than 8 laps are left out.
- **Pit loss**: in-lap plus out-lap, minus twice a reference lap (the median of the driver's clean laps within 5 laps of the stop).
- **Neutralisations**: track status codes on each lap of the race winner, grouped into consecutive periods.

## Data

The data comes from [FastF1](https://github.com/theOehrly/Fast-F1), which reads the official F1 live timing service and the [Jolpica](https://github.com/jolpica/jolpica-f1) API (results).

Since October 2026, the F1 live timing service requires an **F1 TV subscription** (F1 TV Access is enough). Without one, FastF1 cannot download lap and telemetry data.

The data is **not included** in this repository, because it belongs to Formula 1. FastF1 stores downloaded data in the `cache/` folder, which is ignored by Git. The notebooks are saved with their outputs, so the analysis can be read without downloading anything.

[TracingInsights](https://github.com/TracingInsights) provides lap-by-lap F1 data for free and is an alternative for anyone without a subscription.

## Installation

Developed and tested with Python 3.14.

```bash
git clone https://github.com/USERNAME/box-box.git
cd box-box
python -m venv f1env
source f1env/bin/activate        # Windows: f1env\Scripts\activate
pip install -e ".[dev]"
```

Log in to F1 TV once (the login lasts a few days):

```bash
python -m fastf1 auth f1tv --authenticate
python -m fastf1 auth f1tv --status
```

## Usage

Start the app:

```bash
streamlit run app/app.py
```

Open the notebooks:

```bash
jupyter notebook notebooks/
```

The first time a race is loaded, the download can take a minute. After that, it is read from the cache.

## Project structure

```
box-box/
├── .streamlit/
│   └── config.toml          # app theme
├── app/
│   ├── app.py               # entrypoint: sidebar, data loading, navigation
│   └── pages/
│       ├── overview.py
│       ├── race_pace.py
│       ├── tyre_strategy.py
│       ├── pit_stops.py
│       └── positions.py
├── docs/
│   └── screenshots/
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   └── 02_race_analysis.ipynb
├── src/
│   └── f1analysis/
│       ├── data.py          # cache, schedule and session loading
│       ├── cleaning.py      # clean lap selection
│       ├── overview.py      # fastest lap, best sectors, biggest gainer
│       ├── track.py         # track layout from telemetry
│       ├── pace.py          # pace relative to the field
│       ├── tyres.py         # stints and degradation
│       ├── pitstops.py      # pit loss and gap between drivers
│       ├── positions.py     # positions lap by lap
│       ├── events.py        # safety car, VSC and red flag periods
│       └── plots.py         # Plotly charts
├── pyproject.toml
├── LICENSE
└── README.md
```

## Limitations

- Lap and telemetry data requires an F1 TV subscription (see [Data](#data)).
- Detailed timing data is available from 2018 onwards.
- Lap times are not corrected for fuel load, so degradation is a net value: tyre wear minus the gain from burning fuel.
- Track status is read once per lap, so neutralisations are shown at lap level, not at the exact moment they start or end.
- Pit loss is an estimate based on the driver's own pace around the stop, and also includes traffic on the in and out laps.

## License

[MIT](LICENSE)

