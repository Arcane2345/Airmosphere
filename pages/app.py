import streamlit as st
import requests
import json
import plotly.express as px
from argon2 import PasswordHasher
import pandas as pd

st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}

[data-testid="collapsedControl"] {
    display: none;
}
.stApp {
    background:
        radial-gradient(circle at 15% 20%, rgba(0, 229, 255, 0.12), transparent 30%),
        radial-gradient(circle at 85% 75%, rgba(36, 123, 255, 0.13), transparent 35%),
        linear-gradient(135deg, #030712, #071525, #020617);

    background-attachment: fixed;
}
</style>
""", unsafe_allow_html=True)
st.set_page_config(
    page_title="Airmosphere",
    page_icon="🌍",
    layout="wide"
)
st.title("🌍 Airmosphere")
st.caption("Explore the air and the atmosphere around the world.")
st.divider()
city = st.text_input("Enter a city", placeholder="e.g. Tokyo, London, New York")
if st.button("Search"):
    if city:
        st.write(f"Searching for {city}...")
        response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        })
        data = response.json()
        if "results" in data:
            location = data["results"][0]
            latitude = location["latitude"]
            longitude = location["longitude"]
            st.success(f"Location found: {location['name']}")
            st.write("Latitude:", latitude)
            st.write("Longitude:", longitude)
            air_response = requests.get(
                "https://air-quality-api.open-meteo.com/v1/air-quality",
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": "us_aqi,pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,ozone",
                    "hourly": "us_aqi",
                    "forecast_days": 5,
                    "timezone": "auto"
                })
            air_data = air_response.json()
            if "error" in air_data:
                st.error(air_data["reason"])
            else:
                current = air_data["current"]
                hourly = air_data["hourly"]
            aqi = current["us_aqi"]
            if aqi <= 50:
                category = "Good"
            elif aqi <= 100:
                category = "Moderate"
            elif aqi <= 150:
                category = "Unhealthy for Sensitive Groups"
            elif aqi <= 200:
                category = "Unhealthy"
            elif aqi <= 300:
                category = "Very Unhealthy"
            else:
                category = "Hazardous"
            st.subheader("Air Quality Overview")
            col1, col2, col3 = st.columns(3)
            col1.metric("US AQI", current["us_aqi"], f"({category})")
            col2.metric("PM2.5", f'{current["pm2_5"]} µg/m³')
            col3.metric("PM10", f'{current["pm10"]} µg/m³')
            col4, col5, col6 = st.columns(3)
            col4.metric("Carbon Monoxide", f'{current["carbon_monoxide"]} µg/m³')
            col5.metric("Nitrogen Dioxide", f'{current["nitrogen_dioxide"]} µg/m³')
            col6.metric("Ozone", f'{current["ozone"]} µg/m³')
            forecast_df = pd.DataFrame({
                "Time": hourly["time"],
                "AQI": hourly["us_aqi"]
            })
            forecast_df["Date"] = pd.to_datetime(
                forecast_df["Time"]
            ).dt.date
            daily_forecast = forecast_df.groupby("Date")["AQI"].max().reset_index()
            fig = px.line(
                daily_forecast,
                x="Date",
                y="AQI",
                title="5-Day Air Quality Forecast",
                markers=True
            )
            fig.update_yaxes(range=[0, 500])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("City not found.")
    else:
        st.warning("Please enter a city.")
