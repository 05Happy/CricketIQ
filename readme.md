# 🏏 CricketIQ — Cricket Player Performance Analyzer

CricketIQ is a cricket analytics dashboard built with Python, Pandas, and Streamlit. It analyzes ball-by-ball cricket data to calculate player statistics and compare batting performances through interactive charts and tables.

## Features

- **Player Comparison:** Compare two batters using their statistics.
- **Visual Analytics:** View separate charts for runs, batting average, and strike rate.
- **Player Leaderboard:** Explore the top 10 players ranked by selected statistics.
- **Player Profiles:** View an individual player's batting performance.
- **Data Analysis:** Process ball-by-ball cricket data and calculate player statistics.

## Tech Stack

- Python
- Pandas
- Streamlit
- CSV and Glob (Python standard library)

## Statistics Calculated

- **Runs:** Total batter runs recorded in the dataset.
- **Matches Batted:** Number of distinct matches in which a batter appeared.
- **Balls Faced:** Deliveries faced, excluding wides.
- **Dismissals:** Dismissals counted according to the project's calculation rules.
- **Batting Average:** Runs divided by dismissals.
- **Strike Rate:** Runs scored per 100 balls faced.

## Dataset

The project processes ball-by-ball cricket data stored in the `data/` directory. The current dataset contains 1,243 dated match files spanning 2008–2026.

Statistics are calculated from the included data and may differ from official career records depending on dataset coverage and scoring conventions.

## Installation and Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/05Happy/CricketIQ.git
   cd CricketIQ
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the dashboard:

   ```bash
   python -m streamlit run app.py
   ```

4. Open the local URL shown in the terminal, usually `http://localhost:8501`.

The dashboard expects `player_stats.csv` to be present in the project directory. To regenerate it, run the data-processing script:

```bash
python main.py
```

## Project Structure

```text
CricketIQ/
├── data/              # Ball-by-ball match data
├── main.py            # Data processing and statistic calculations
├── app.py             # Streamlit dashboard
├── player_stats.csv   # Calculated player statistics
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

## Future Improvements

- Add more batting and bowling statistics.
- Improve data validation and statistical visualizations.
- Add filters for seasons and teams.
- Expand player performance analysis.

---

Built as a hands-on project to learn Python data analysis and dashboard development.