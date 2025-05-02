from fastapi import APIRouter, Depends, Query
from db.database import SessionLocal
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from db.models import Player, Club, League
from fastapi.responses import StreamingResponse
import io
import csv

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/players")
def get_players(
    name: Optional[str] = Query(None),
    position: Optional[str] = Query(None),
    nationality: Optional[str] = Query(None),
    club: Optional[str] = Query(None),
    league: Optional[str] = Query(None),
    age: Optional[int] = Query(None, ge=0),
    age_min: Optional[int] = Query(None, ge=0),
    age_max: Optional[int] = Query(None, ge=0),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(Player).options(joinedload(Player.club).joinedload(Club.league))

    if name:
        query = query.filter(Player.name.ilike(f"%{name}%"))
    if position:
        query = query.filter(Player.position.ilike(f"%{position}%"))
    if nationality:
        query = query.filter(Player.nationality.ilike(f"%{nationality}%"))
    if club:
        query = query.join(Player.club).filter(Club.name.ilike(f"%{club}%"))
    if league:
        query = query.join(Player.club).join(Club.league).filter(League.name.ilike(f"%{league}%"))
    if age is not None:
        query = query.filter(Player.age == age)
    if age_min is not None:
        query = query.filter(Player.age >= age_min)
    if age_max is not None:
        query = query.filter(Player.age <= age_max)


    total = query.count()
    players = query.offset(offset).limit(limit).all()

    results = [{
        "name": p.name,
        "age": p.age,
        "nationality": p.nationality,
        "position": p.position,
        "market_value": p.market_value,
        "market_value_eur": p.market_value_eur,
        "club": p.club.name,
        "league": p.club.league.name
    } for p in players]

    return {
        "total": total,
        "count": len(results),
        "limit": limit,
        "offset": offset,
        "results": results
    }





# 📌 GET /leagues
@router.get("/leagues")
def get_leagues(db: Session = Depends(get_db)):
    leagues = db.query(League).all()
    return [{"id": l.id, "name": l.name} for l in leagues]

# 📌 GET /clubs
@router.get("/clubs")
def get_clubs(league: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Club).options(joinedload(Club.league))
    if league:
        query = query.join(Club.league).filter(League.name.ilike(f"%{league}%"))
    clubs = query.all()
    return [{"id": c.id, "name": c.name, "league": c.league.name} for c in clubs]

# 📌 GET /top10
@router.get("/top10")
def get_top10_players(league: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Player).options(joinedload(Player.club).joinedload(Club.league))
    if league:
        query = query.join(Player.club).join(Club.league).filter(League.name.ilike(f"%{league}%"))
    top_players = (
        query.filter(Player.market_value_eur.isnot(None))
             .order_by(Player.market_value_eur.desc())
             .limit(10)
             .all()
    )
    return [{
        "name": p.name,
        "market_value_eur": p.market_value_eur,
        "club": p.club.name,
        "league": p.club.league.name
    } for p in top_players]




@router.get("/players/export")
def export_players(
    name: Optional[str] = Query(None),
    position: Optional[str] = Query(None),
    nationality: Optional[str] = Query(None),
    club: Optional[str] = Query(None),
    league: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Player).options(joinedload(Player.club).joinedload(Club.league))

    if name:
        query = query.filter(Player.name.ilike(f"%{name}%"))
    if position:
        query = query.filter(Player.position.ilike(f"%{position}%"))
    if nationality:
        query = query.filter(Player.nationality.ilike(f"%{nationality}%"))
    if club:
        query = query.join(Player.club).filter(Club.name.ilike(f"%{club}%"))
    if league:
        query = query.join(Player.club).join(Club.league).filter(League.name.ilike(f"%{league}%"))

    players = query.all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["name", "age", "nationality", "position", "market_value", "market_value_eur", "club", "league"])
    for p in players:
        writer.writerow([
            p.name,
            p.age,
            p.nationality,
            p.position,
            p.market_value,
            p.market_value_eur,
            p.club.name,
            p.club.league.name
        ])

    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=players_export.csv"
    })
