from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class League(Base):
    __tablename__ = "leagues"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)

    clubs = relationship("Club", back_populates="league")


class Club(Base):
    __tablename__ = "clubs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    league_id = Column(Integer, ForeignKey("leagues.id"))

    league = relationship("League", back_populates="clubs")
    players = relationship("Player", back_populates="club")


class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    age = Column(Integer)
    nationality = Column(String)
    position = Column(String)
    market_value = Column(String)
    market_value_eur = Column(Integer)
    club_id = Column(Integer, ForeignKey("clubs.id"))

    club = relationship("Club", back_populates="players")
