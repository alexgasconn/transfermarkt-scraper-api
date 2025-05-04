from scraper.scraper import scrape_league_players, LEAGUES
from scraper.utils import parse_market_value
from db.database import init_db, SessionLocal
from db.models import League, Club, Player

init_db()
session = SessionLocal()

for league_info in LEAGUES:
    league_name = league_info["name"]
    league_url = league_info["url"]

    # Verificar si la liga ya existe
    league = session.query(League).filter_by(name=league_name).first()
    if not league:
        league = League(name=league_name)
        session.add(league)
        session.commit()

    # Scrapea jugadores de todos los clubes de la liga
    players_data = scrape_league_players(league_name, league_url)

    for player_row in players_data:
        club_name = player_row["club"]

        # Verificar si el club ya existe
        club = session.query(Club).filter_by(name=club_name, league_id=league.id).first()
        if not club:
            club = Club(name=club_name, league=league)
            session.add(club)
            session.commit()

        # Crear jugador
        player = Player(
            name=player_row["name"],
            age=int(player_row["age"]) if player_row["age"].isdigit() else None,
            nationality=player_row["nationality"],
            position_detail=player_row["position_detail"],
            position_category=player_row["position_category"],
            market_value=player_row["market_value"],
            market_value_eur=parse_market_value(player_row["market_value"]),
            club=club
        )
        session.add(player)

session.commit()
session.close()
print("✅ All leagues, clubs, and players saved with relational integrity.")
