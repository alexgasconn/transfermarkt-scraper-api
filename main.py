from scraper.scraper import scrape_league_players, LEAGUES
from scraper.utils import parse_market_value
from db.database import init_db, SessionLocal
from db.models import Player

init_db()
session = SessionLocal()

for league in LEAGUES:
    players = scrape_league_players(league["name"], league["url"])
    for row in players:
        player = Player(
            name=row["name"],
            age=int(row["age"]) if row["age"].isdigit() else None,
            nationality=row["nationality"],
            position=row["position"],
            market_value=row["market_value"],
            market_value_eur=parse_market_value(row["market_value"]),
            club=row["club"],
            league=row["league"]
        )
        session.add(player)

session.commit()
session.close()
print("✅ All players from all leagues saved to the database.")
