from scraper.scraper import scrape_ajax_players
from scraper.utils import parse_market_value
from db.database import init_db, SessionLocal
from db.models import Player

init_db()

df = scrape_ajax_players()
session = SessionLocal()

for _, row in df.iterrows():
    player = Player(
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
print("✅ Jugadores guardados en la base de datos.")
