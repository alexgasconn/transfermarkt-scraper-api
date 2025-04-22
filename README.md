
# Transfermarkt Scraper API

A Python project to scrape football player data from [Transfermarkt](https://www.transfermarkt.com/), store it in a local SQLite database, and expose the data through a FastAPI REST API.

## ⚽ Features

- Scrapes player data (name, age, nationality, position, market value) for all Eredivisie clubs  
- Converts market values (e.g., `€1.20m`, `€500k`) to numeric format  
- Stores data in SQLite using SQLAlchemy ORM  
- Exposes a `/players` API endpoint with FastAPI  
- Clean structure ready for extension, testing and deployment  

## 🛠 Setup

```bash
git clone https://github.com/alexgasconn/transfermarkt-scraper-api.git
cd transfermarkt-scraper-api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 📦 Run the Scraper

This command scrapes all Eredivisie teams and stores the players in `data/players.db`:

```bash
python main.py
```

## 🌐 Run the API

Start the FastAPI server:

```bash
uvicorn api.main:app --reload
```

Then visit:

```
http://127.0.0.1:8000/docs
```

to explore the interactive API via Swagger UI.

## 🔍 Example Endpoint

- `GET /players`: Returns all players in the database

## 📁 Project Structure

```
.
├── api/                # FastAPI routes
│   ├── main.py
│   └── routes.py
├── db/                 # SQLAlchemy models and session
│   ├── database.py
│   └── models.py
├── scraper/            # Scraping logic and utilities
│   ├── scraper.py
│   └── utils.py
├── data/               # Contains players.db (SQLite)
├── main.py             # Runs scraper and saves data
├── requirements.txt
└── README.md
```

## ✅ To Do

- Add filters by club, position, nationality  
- Add top 10 by market value endpoint  
- Dockerize the full pipeline  
- Add CI with GitHub Actions  
- Optional: deploy to cloud with Terraform / Ansible  

## 📄 License

MIT
