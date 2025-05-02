# ⚽ Transfermarkt Scraper & Dashboard

A full-stack football analytics pipeline that scrapes player data from [Transfermarkt](https://www.transfermarkt.com/), stores it in a relational database, serves it through a FastAPI REST API, and displays it in an interactive dashboard built with Streamlit.

---

## 🔍 What it does

- Scrapes all players from the top 8 European leagues (LaLiga, Premier League, Bundesliga, Serie A, Ligue 1, Eredivisie, Primeira Liga, Jupiler Pro League)
- Converts fuzzy market values (e.g., `€1.2m`, `€500k`) to numeric format
- Stores data in a normalized relational database (`leagues`, `clubs`, `players`)
- Exposes a complete REST API with filters, pagination, CSV export, and ranking
- Builds an interactive dashboard with filters and CSV export using Streamlit
- Dockerized setup to run the full pipeline in seconds

---

## 🧱 Architecture Overview

[Transfermarkt.com] --> [Scraper] --> [SQLite DB]
|
+--> [FastAPI API] --> [Streamlit Dashboard]


- **Scraper:** Parallel scraping of each club using `requests` + `BeautifulSoup`
- **Database:** SQLAlchemy ORM with 3 relational tables (`leagues`, `clubs`, `players`)
- **API:** Built with FastAPI, includes powerful filtering and export options
- **Dashboard:** Built with Streamlit, uses API to display and filter players in real time
- **Docker:** Compose setup for launching everything with a single command

---

## 🚀 Quick Start (with Docker)

### ✅ Prerequisites

- Docker & Docker Compose installed

### ⚙️ Steps

1. **Clone the repo:**

git clone https://github.com/alexgasconn/transfermarkt-scraper-api.git
cd transfermarkt-scraper-api

2. **Build the services:**

docker compose build


3. **Launch the app:**

docker compose up

4. **Visit in browser:**

API: http://localhost:8000/docs
Dashboard: http://localhost:8501

5. **Stop everything:**

docker compose down

## 🌐 REST API Endpoints
| Endpoint          | Description                                 |
| ----------------- | ------------------------------------------- |
| `/players`        | Returns filtered players with pagination    |
| `/players/export` | Downloads filtered player list as CSV       |
| `/leagues`        | Lists all scraped leagues                   |
| `/clubs`          | Lists clubs (optionally filtered by league) |
| `/top10`          | Top 10 players by market value              |


Filters supported in /players: name, position, nationality, club, league, age, age_min, age_max, limit, offset

## 📊 Dashboard Features (Streamlit)
- Select filters (league, club, position, age range)

- View results in an interactive table

- Download data directly as CSV

- Fast and responsive via API-backed queries

## 📁 Project Structure
.
├── api/                  # FastAPI logic
│   ├── main.py
│   └── routes.py
├── db/                   # SQLAlchemy models and session
│   ├── database.py
│   └── models.py
├── scraper/              # Scraping logic and utilities
│   ├── scraper.py
│   └── utils.py
├── dashboard.py          # Streamlit dashboard app
├── main_multi_relational.py  # Entry point for scraping & DB insertion
├── requirements.txt
├── Dockerfile.api
├── Dockerfile.dashboard
├── docker-compose.yml
└── README.md

## 🧠 How it works — Step-by-step
1. Scraping:

- main_multi_relational.py scrapes clubs from each league

- Parses player data and inserts it into a SQLite database

- Uses a relational schema with foreign keys (league → club → player)

2. API:

- FastAPI reads from the same SQLite DB

- Provides powerful filtering and a /players/export CSV route

- Returns paginated, structured data for any frontend or analysis

3. Dashboard:

- Streamlit UI with filters

- Makes live requests to the FastAPI backend

- Can be expanded with charts, rankings, trends, etc.

4. Dockerized Stack:

- 2 containers: api (FastAPI) + dashboard (Streamlit)

- Both share the same data/ volume for DB persistence

- Ready to run anywhere with docker compose up

## 📄 License
MIT License