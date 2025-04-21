import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_ajax_players():
    url = "https://www.transfermarkt.com/ajax-amsterdam/kader/verein/610/saison_id/2023"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    players = []
    table = soup.find("table", {"class": "items"})

    for row in table.find_all("tr", class_=["odd", "even"]):
        name = row.find("td", class_="hauptlink").get_text(strip=True)
        position = row.find_all("td")[4].text.strip()
        market_value = row.find_all("td")[-1].text.strip()
        nationality = row.find("img", class_="flaggenrahmen")["title"]
        age = row.find_all("td")[5].text.strip()

        players.append({
            "name": name,
            "position": position,
            "market_value": market_value,
            "age": age,
            "nationality": nationality
        })

    return pd.DataFrame(players)
