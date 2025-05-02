import streamlit as st
import pandas as pd
import requests

import os
API_URL = os.getenv("API_URL", "http://localhost:8000")


st.set_page_config(page_title="Transfermarkt Dashboard", layout="wide")
st.title("📊 Football Player Dashboard")

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Get filters from API
leagues = requests.get(f"{API_URL}/leagues").json()
league_names = [l["name"] for l in leagues]
selected_league = st.sidebar.selectbox("League", [""] + league_names)

clubs = requests.get(f"{API_URL}/clubs", params={"league": selected_league}).json() if selected_league else []
club_names = [c["name"] for c in clubs]
selected_club = st.sidebar.selectbox("Club", [""] + club_names)

position = st.sidebar.text_input("Position (e.g., Midfield, Forward)")
age_min = st.sidebar.number_input("Minimum Age", min_value=0, max_value=50, step=1)
age_max = st.sidebar.number_input("Maximum Age", min_value=0, max_value=50, step=1, value=50)

if st.sidebar.button("Apply Filters"):
    params = {
        "league": selected_league or None,
        "club": selected_club or None,
        "position": position or None,
        "age_min": age_min or None,
        "age_max": age_max or None,
        "limit": 500
    }

    response = requests.get(f"{API_URL}/players", params=params)

    if response.status_code == 200:
        players = response.json()
        if "results" in players:
            df = pd.DataFrame(players["results"])
            st.write(f"### Showing {len(df)} players")
            st.dataframe(df)

            # Download button
            csv_url = f"{API_URL}/players/export"
            download_link = requests.get(csv_url, params=params)
            st.download_button("⬇️ Download CSV", data=download_link.content, file_name="players.csv", mime="text/csv")
        else:
            st.warning("No players found for selected filters.")
    else:
        st.error(f"API error: {response.status_code}")

