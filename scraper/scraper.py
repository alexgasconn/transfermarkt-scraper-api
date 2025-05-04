import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed


def scrape_club_players(club_name, club_url, season=2023):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"{club_url}/saison_id/{season}"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    players = []
    table = soup.find("table", {"class": "items"})
    if not table:
        return []

    for row in table.find_all("tr", class_=["odd", "even"]):
        try:
            name = row.find("td", class_="hauptlink").get_text(strip=True)
            position = row.find_all("td")[4].text.strip()
            market_value = row.find_all("td")[-1].text.strip()
            nationality = row.find("img", class_="flaggenrahmen")["title"]
            age = row.find_all("td")[5].text.strip()
            position_detail = row.find_all("td")[4].text.strip()
            position_category = map_position_category(position_detail)

            players.append({
                "club": club_name,
                "name": name,
                "age": age,
                "nationality": nationality,
                "position_detail": position_detail,
                "position_category": position_category,
                "market_value": market_value
            })

        except Exception:
            continue

    return players




def get_club_urls_from_league(league_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(league_url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    clubs = []
    table = soup.find("table", class_="items")

    for row in table.find_all("tr", class_=["odd", "even"]):
        a = row.find("td", class_="hauptlink").find("a")
        club_name = a.text.strip()
        relative_url = a["href"].split("?")[0]  # Clean URL
        full_url = f"https://www.transfermarkt.com{relative_url.replace('/startseite', '/kader')}"
        clubs.append((club_name, full_url))

    return clubs



LEAGUES = [
    {
        "name": "LaLiga",
        "url": "https://www.transfermarkt.com/primera-division/startseite/wettbewerb/ES1"
    },
    {
        "name": "Premier League",
        "url": "https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1"
    },
    {
        "name": "Bundesliga",
        "url": "https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1"
    },
    {
        "name": "Serie A",
        "url": "https://www.transfermarkt.com/serie-a/startseite/wettbewerb/IT1"
    },
    {
        "name": "Ligue 1",
        "url": "https://www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR1"
    },
    {
        "name": "Eredivisie",
        "url": "https://www.transfermarkt.com/eredivisie/startseite/wettbewerb/NL1"
    },
    {
        "name": "Primeira Liga",
        "url": "https://www.transfermarkt.com/primeira-liga/startseite/wettbewerb/PO1"
    },
    {
        "name": "Jupiler Pro League",
        "url": "https://www.transfermarkt.com/jupiler-pro-league/startseite/wettbewerb/BE1"
    }
]

from concurrent.futures import ThreadPoolExecutor, as_completed

def scrape_league_players(league_name, league_url, season=2023):
    all_players = []
    clubs = get_club_urls_from_league(league_url)

    def scrape(club_name, club_url):
        print(f"🔍 Scraping {club_name} ({league_name})...")
        players = scrape_club_players(club_name, club_url, season)
        for p in players:
            p["league"] = league_name
        return players

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(scrape, club_name, club_url) for club_name, club_url in clubs]
        for future in as_completed(futures):
            all_players.extend(future.result())

    return all_players


def map_position_category(detail: str) -> str:
    detail = detail.lower()
    if "keeper" in detail:
        return "Goalkeeper"
    elif "back" in detail or "defender" in detail or "centre-back" in detail:
        return "Defender"
    elif "midfield" in detail:
        return "Midfield"
    elif "winger" in detail or "forward" in detail or "striker" in detail:
        return "Forward"
    else:
        return "Other"
