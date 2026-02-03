📌 Title

NBA Player Stats Visualizer

📖 Description

A Streamlit web application for comparing NBA player statistics across seasons.
Users can compare up to four players using per-game averages, season totals, or cumulative career totals for both regular season and playoff data.

✨ Features

Compare up to 4 NBA players simultaneously

Supports:

Per-game averages

Season totals

Career cumulative totals

Regular season and playoff statistics

Interactive visualizations:

Line charts

Grouped bar charts

Tabular view

Built with live data from nba_api

🛠️ Tech Stack

Python

Streamlit

Plotly

pandas

nba_api

🚀 How to Run Locally
git clone <your-repo-url>
cd <project-folder>
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py

🧠 Design Decisions

Player lookup optimized using a dictionary for O(1) name resolution

Player data combined into a single DataFrame for flexible plotting

Plotting and data-fetching logic kept separate for maintainability

Table view generated via pivoting for readability

⚠️ Known Limitations

Players who played for multiple teams in one season may appear multiple times

Requires full player names for accurate matching

Relies on nba_api availability

📌 Future Improvements

Autocomplete player selection

Download data as CSV

Per-team season breakdowns

Player name disambiguation