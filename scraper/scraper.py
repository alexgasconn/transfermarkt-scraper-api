import requests
from bs4 import BeautifulSoup
import pandas as pd

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
            players.append({
                "club": club_name,
                "name": name,
                "age": age,
                "position": position,
                "nationality": nationality,
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
