# 🏀 NBA Player Stats Visualizer

A Streamlit web application for comparing NBA player statistics across seasons.  
Users can compare up to four players using per-game averages, season totals, or cumulative career totals for both regular season and playoff data.

---

## ✨ Features

- Compare up to **4 NBA players** at once
- Stat types:
  - Per-game averages
  - Season totals
  - Career cumulative totals
- Supports **regular season** and **playoff** data
- Interactive visualizations:
  - Line charts
  - Grouped bar charts
  - Tabular view
- Live data powered by `nba_api`

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **Plotly**
- **pandas**
- **nba_api**

---

## 🚀 Getting Started

### Run Locally

```bash
git clone <your-repo-url>
cd <project-folder>

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
