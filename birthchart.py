import streamlit as st
import requests
import datetime

# Streamlit page setup
st.set_page_config(page_title="🪐 Astro Reports", layout="centered")
st.title("🪐 Daily Astro Transit Report")

# Date selector
selected_date = st.date_input("Select Date", datetime.date.today())
formatted_date = selected_date.strftime('%Y-%m-%d')

st.markdown(f"### 📅 Report for {formatted_date}")

# Try primary data source (Swiss Ephemeris - if available locally)
astro_data = None

try:
    import swisseph as swe

    def get_planet_data(date):
        jd = swe.julday(date.year, date.month, date.day)
        planets = {
            "Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY,
            "Venus": swe.VENUS, "Mars": swe.MARS, "Jupiter": swe.JUPITER,
            "Saturn": swe.SATURN, "Rahu": swe.MEAN_NODE, "Ketu": swe.TRUE_NODE
        }
        planet_positions = {}
        for name, id in planets.items():
            lon, _, _ = swe.calc_ut(jd, id)
            planet_positions[name] = round(lon, 2)
        return planet_positions

    astro_data = get_planet_data(selected_date)

except ModuleNotFoundError:
    st.warning("⚠️ Swiss Ephemeris not found. Fetching from backup online API...")

    # Fallback API from astronomics.ai
    try:
        url = f"https://data.astronomics.ai/almanac?date={formatted_date}&tz=Asia/Kolkata"
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()

        # Sample expected format from astronomics.ai
        astro_data = {
            planet['name']: planet.get('longitude_deg', '?')
            for planet in json_data.get("planets", [])
        }

    except requests.exceptions.RequestException as e:
        st.error(f"🔴 Failed to fetch astro data: {str(e)}")

    except requests.exceptions.JSONDecodeError:
        st.error("🔴 Error decoding JSON response. API may be down or returned invalid data.")

# Show results if available
if astro_data:
    st.subheader("🪐 Planetary Positions")
    st.table(pd.DataFrame(astro_data.items(), columns=["Planet", "Longitude (°)"]))

else:
    st.error("🚫 No planetary data available for the selected date.")
