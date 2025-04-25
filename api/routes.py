from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import Player
from typing import Optional, List

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
    db: Session = Depends(get_db)
):
    query = db.query(Player)
    if name:
        query = query.filter(Player.name.ilike(f"%{name}%"))
    if position:
        query = query.filter(Player.position.ilike(f"%{position}%"))
    if nationality:
        query = query.filter(Player.nationality.ilike(f"%{nationality}%"))
    if club:
        query = query.filter(Player.club.ilike(f"%{club}%"))
    return query.all()


@router.get("/top10")
def get_top_10_players(db: Session = Depends(get_db)):
    players = (
        db.query(Player)
        .filter(Player.market_value_eur > 0)
        .order_by(Player.market_value_eur.desc())
        .limit(10)
        .all()
    )
    return players
