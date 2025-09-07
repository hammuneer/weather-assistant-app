# weatherbot/app.py
import streamlit as st
import pandas as pd
import asyncio


from services.weather_service import get_weather
from agents_user.location_agent import extract_location_async
from utils.formatting import extract_core_metrics
from config import settings

st.set_page_config(
    page_title="WeatherBot",
    page_icon="⛅",
    layout="wide",
)

# --- Simple CSS accents for colorful tabs & cards ---
st.markdown(
    """
    <style>
    .metric-card {
        background: linear-gradient(135deg, #f0f4ff 0%, #f8fffb 100%);
        padding: 14px 16px;
        border-radius: 16px;
        box-shadow: 0 1px 6px rgba(0,0,0,0.06);
        border: 1px solid rgba(0,0,0,0.05);
    }
    .section-title {
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.4rem;
    }
    .cond {
        display: flex; align-items: center; gap: 8px;
        padding: 8px 10px; border-radius: 12px;
        background: #fffdf5; border: 1px solid #ffe8a3;
        width: fit-content;
    }
    .small-note { color: #6b7280; font-size: 0.9rem; }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Session state for chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("⛅ WeatherBot")
st.caption("Ask about the weather anywhere — I’ll extract the location, fetch live data, and show the essentials.")

# --- Chat history display ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- Chat input ---
query = st.chat_input("Ask e.g. 'What's the weather in Lahore right now?'")
if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.write(query)

    # 1) Extract location
    location = asyncio.run(extract_location_async(query))
    if not location:
        location = settings.DEFAULT_LOCATION


    st.toast(f"Detected location: {location}", icon="🌍")

    # 2) Fetch weather
    data = get_weather(location)

    # 3) Display assistant turn (concise)
    with st.chat_message("assistant"):
        if "error" in data:
            st.error(f"Error fetching weather: {data['error']}")
        else:
            core = extract_core_metrics(data)

            # Header line
            place = ", ".join([x for x in [core.get("name"), core.get("region"), core.get("country")] if x])
            st.markdown(f"**Location:** {place}  \n*Local time:* {core.get('localtime') or '—'}")

            # Tabs: Overview | Wind | Air & Sun | Map | Raw JSON
            tab1, tab2, tab3, tab4, tab5 = st.tabs(
                ["🌤️ Overview", "🍃 Wind", "🌞 Air & Sun", "🗺️ Map", "🧩 Raw JSON"]
            )

            with tab1:
                # Condition & temp
                cols = st.columns(4)
                with cols[0]:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">Temperature</div>', unsafe_allow_html=True)
                    st.metric(label="Now (°C)", value=core.get("temp_c", "—"), delta=None)
                    st.metric(label="Feels like (°C)", value=core.get("feelslike_c", "—"))
                    st.markdown('</div>', unsafe_allow_html=True)
                with cols[1]:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">Humidity</div>', unsafe_allow_html=True)
                    st.metric(label="Relative Humidity (%)", value=core.get("humidity", "—"))
                    st.markdown('</div>', unsafe_allow_html=True)
                with cols[2]:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">Visibility</div>', unsafe_allow_html=True)
                    st.metric(label="Vis (km)", value=core.get("vis_km", "—"))
                    st.markdown('</div>', unsafe_allow_html=True)
                with cols[3]:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">Updated</div>', unsafe_allow_html=True)
                    st.metric(label="Last Updated", value=core.get("last_updated", "—"))
                    st.markdown('</div>', unsafe_allow_html=True)

                # Condition badge
                cond = core.get("condition_text") or "—"
                icon = core.get("icon")
                if icon:
                    st.markdown(
                        f'<div class="cond"><img src="{icon}" width="28"/><span>{cond}</span></div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(f"**Condition:** {cond}")

            with tab2:
                cols = st.columns(3)
                with cols[0]:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">Wind</div>', unsafe_allow_html=True)
                    st.metric("Wind (kph)", core.get("wind_kph", "—"))
                    st.metric("Direction", core.get("wind_dir", "—"))
                    st.markdown('</div>', unsafe_allow_html=True)
                with cols[1]:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">Gusts</div>', unsafe_allow_html=True)
                    st.metric("Gust (kph)", core.get("gust_kph", "—"))
                    st.markdown('</div>', unsafe_allow_html=True)
                with cols[2]:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">Pressure</div>', unsafe_allow_html=True)
                    st.metric("Pressure (mb)", core.get("pressure_mb", "—"))
                    st.markdown('</div>', unsafe_allow_html=True)

            with tab3:
                cols = st.columns(4)
                with cols[0]:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">UV Index</div>', unsafe_allow_html=True)
                    st.metric("UV", core.get("uv", "—"))
                    st.markdown('</div>', unsafe_allow_html=True)
                with cols[1]:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">Cloud</div>', unsafe_allow_html=True)
                    st.metric("Cloud (%)", core.get("cloud", "—"))
                    st.markdown('</div>', unsafe_allow_html=True)
                with cols[2]:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">Dew Point</div>', unsafe_allow_html=True)
                    st.metric("Dew (°C)", core.get("dewpoint_c", "—"))
                    st.markdown('</div>', unsafe_allow_html=True)
                with cols[3]:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">Feels Like</div>', unsafe_allow_html=True)
                    st.metric("Feels (°C)", core.get("feelslike_c", "—"))
                    st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<span class="small-note">Only key indicators shown. See the JSON tab for the full payload.</span>', unsafe_allow_html=True)

            with tab4:
                # Map requires lat/lon in a DataFrame
                lat, lon = core.get("lat"), core.get("lon")
                if lat is not None and lon is not None:
                    df = pd.DataFrame([{"lat": lat, "lon": lon, "place": place}])
                    st.map(df, size=15)
                else:
                    st.info("No coordinates available to render the map.")

            with tab5:
                st.json(data)

# Footer
st.caption("Built with Streamlit • Weather data by WeatherAPI.com")
