from scraper.scraper import get_club_urls_from_league, scrape_club_players
from scraper.utils import parse_market_value
from db.database import init_db, SessionLocal
from db.models import Player
import pandas as pd

init_db()
session = SessionLocal()

clubs = get_club_urls_from_league("https://www.transfermarkt.com/eredivisie/startseite/wettbewerb/NL1")

for club_name, club_url in clubs:
    print(f"* Scraping {club_name}...")
    players = scrape_club_players(club_name, club_url)

    for row in players:
        player = Player(
            club=row["club"],
            name=row["name"],
            age=int(row["age"]) if row["age"].isdigit() else None,
            nationality=row["nationality"],
            position=row["position"],
            market_value=row["market_value"],
            market_value_eur=parse_market_value(row["market_value"])
        )
        session.add(player)

session.commit()
session.close()
print("✅ Todos los jugadores de la liga guardados!")
