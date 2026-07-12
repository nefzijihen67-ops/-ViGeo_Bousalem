import streamlit as st
import requests
from datetime import datetime
from languages import TEXTS

LAT, LON = 36.6167, 8.9667

WEATHER_TXT = {
    "ar": {
        "days": ["الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"],
        "codes": {
            0: ("☀️", "صحو"), 1: ("🌤️", "صحو غالبًا"), 2: ("⛅", "غائم جزئيًا"), 3: ("☁️", "غائم"),
            45: ("🌫️", "ضباب"), 48: ("🌫️", "ضباب متجمد"),
            51: ("🌦️", "رذاذ خفيف"), 53: ("🌦️", "رذاذ متوسط"), 55: ("🌦️", "رذاذ كثيف"),
            61: ("🌧️", "أمطار خفيفة"), 63: ("🌧️", "أمطار متوسطة"), 65: ("🌧️", "أمطار غزيرة"),
            71: ("❄️", "ثلوج خفيفة"), 73: ("❄️", "ثلوج متوسطة"), 75: ("❄️", "ثلوج كثيفة"),
            80: ("🌦️", "زخات مطر خفيفة"), 81: ("🌧️", "زخات مطر متوسطة"), 82: ("⛈️", "زخات مطر غزيرة"),
            95: ("⛈️", "عاصفة رعدية"), 96: ("⛈️", "عاصفة رعدية مع برد"), 99: ("⛈️", "عاصفة رعدية شديدة"),
        },
        "unknown": ("🌡️", "غير معروف"),
    },
    "fr": {
        "days": ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"],
        "codes": {
            0: ("☀️", "Ciel dégagé"), 1: ("🌤️", "Plutôt dégagé"), 2: ("⛅", "Partiellement nuageux"), 3: ("☁️", "Nuageux"),
            45: ("🌫️", "Brouillard"), 48: ("🌫️", "Brouillard givrant"),
            51: ("🌦️", "Bruine légère"), 53: ("🌦️", "Bruine modérée"), 55: ("🌦️", "Bruine dense"),
            61: ("🌧️", "Pluie légère"), 63: ("🌧️", "Pluie modérée"), 65: ("🌧️", "Pluie forte"),
            71: ("❄️", "Neige légère"), 73: ("❄️", "Neige modérée"), 75: ("❄️", "Neige forte"),
            80: ("🌦️", "Averses légères"), 81: ("🌧️", "Averses modérées"), 82: ("⛈️", "Averses fortes"),
            95: ("⛈️", "Orage"), 96: ("⛈️", "Orage avec grêle"), 99: ("⛈️", "Orage violent"),
        },
        "unknown": ("🌡️", "Inconnu"),
    },
    "en": {
        "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "codes": {
            0: ("☀️", "Clear sky"), 1: ("🌤️", "Mostly clear"), 2: ("⛅", "Partly cloudy"), 3: ("☁️", "Cloudy"),
            45: ("🌫️", "Fog"), 48: ("🌫️", "Freezing fog"),
            51: ("🌦️", "Light drizzle"), 53: ("🌦️", "Moderate drizzle"), 55: ("🌦️", "Dense drizzle"),
            61: ("🌧️", "Light rain"), 63: ("🌧️", "Moderate rain"), 65: ("🌧️", "Heavy rain"),
            71: ("❄️", "Light snow"), 73: ("❄️", "Moderate snow"), 75: ("❄️", "Heavy snow"),
            80: ("🌦️", "Light rain showers"), 81: ("🌧️", "Moderate rain showers"), 82: ("⛈️", "Heavy rain showers"),
            95: ("⛈️", "Thunderstorm"), 96: ("⛈️", "Thunderstorm with hail"), 99: ("⛈️", "Severe thunderstorm"),
        },
        "unknown": ("🌡️", "Unknown"),
    },
}


def weather_desc(code, W):
    return W["codes"].get(code, W["unknown"])


def stat_card(icon, label, value, big=False):
    icon_size = "64px" if big else "40px"
    st.markdown(f"""
    <div style='background:#F8F9FA; border-radius:12px; padding:16px 8px;
                text-align:center; border:1px solid #E5DFD0; height:100%;'>
        <div style='font-size:{icon_size}; line-height:1.1;'>{icon}</div>
        <div style='font-size:13px; color:#666; margin-top:6px;'>{label}</div>
        <div style='font-size:20px; font-weight:700; color:#16414A; margin-top:2px;'>{value}</div>
    </div>
    """, unsafe_allow_html=True)


@st.cache_data(ttl=1800)
def fetch_weather():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}&longitude={LON}"
        "&current_weather=true"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,"
        "precipitation_probability_max,weathercode,windspeed_10m_max"
        "&timezone=Africa%2FTunis&forecast_days=7"
    )
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def show(lang):
    T = TEXTS[lang]
    W = WEATHER_TXT.get(lang, WEATHER_TXT["ar"])

    with st.container(key="card_weather_intro"):
        st.title(T["nav_tab3"])
        st.write(T["tab3_intro"])

    st.write("")

    try:
        with st.spinner(T["loading_weather"]):
            data = fetch_weather()
    except Exception:
        st.error(T["weather_error"])
        return

    current = data["current_weather"]
    daily = data["daily"]
    emoji, desc = weather_desc(current["weathercode"], W)

    # ترتيب الأيام: عادي (0→6) لكل اللغات، معكوس (6→0) للعربي فقط
    day_indexes = list(range(6, -1, -1)) if lang == "ar" else list(range(7))

    with st.container(key="card_weather_now"):
        st.header(T["weather_current_title"])
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            stat_card(emoji, desc, "", big=True)
        with c2:
            stat_card("🌡️", "الحرارة" if lang == "ar" else ("Température" if lang == "fr" else "Temperature"),
                       f"{current['temperature']}°")
        with c3:
            stat_card("💨", T["wind_label"], f"{current['windspeed']} km/h")
        with c4:
            today_rain = daily["precipitation_sum"][0]
            label_today = {"ar": f"{T['rain_qty_label']} اليوم", "fr": f"{T['rain_qty_label']} aujourd'hui",
                           "en": f"Today's {T['rain_qty_label']}"}[lang]
            stat_card("🌧️", label_today, f"{today_rain} mm")

    st.write("")

    with st.container(key="card_weather_week"):
        st.header(T["weather_forecast_title"])
        cols = st.columns(7)
        for pos, i in enumerate(day_indexes):
            date_obj = datetime.strptime(daily["time"][i], "%Y-%m-%d")
            day_name = W["days"][date_obj.weekday()]
            e, d = weather_desc(daily["weathercode"][i], W)
            tmax = daily["temperature_2m_max"][i]
            tmin = daily["temperature_2m_min"][i]
            rain = daily["precipitation_sum"][i]
            rain_prob = daily["precipitation_probability_max"][i]

            with cols[pos]:
                st.markdown(f"""
                <div style='background:#F8F9FA; border-radius:12px; padding:14px 6px;
                            text-align:center; border:1px solid #E5DFD0;'>
                    <div style='font-weight:700; font-size:13px; color:#16414A;'>{day_name}</div>
                    <div style='font-size:32px; margin:6px 0;'>{e}</div>
                    <div style='font-size:12px; color:#666; margin-bottom:6px;'>{d}</div>
                    <div style='font-size:14px; font-weight:600;'>{tmax}° / {tmin}°</div>
                    <div style='font-size:12px; color:#2E7C86; margin-top:4px;'>💧 {rain_prob}%</div>
                    <div style='font-size:11px; color:#888;'>{rain} mm</div>
                </div>
                """, unsafe_allow_html=True)

    st.write("")

    with st.container(key="card_weather_charts"):
        import plotly.graph_objects as go

        day_labels = [W["days"][datetime.strptime(daily["time"][i], "%Y-%m-%d").weekday()] for i in day_indexes]
        precip_ordered = [daily["precipitation_sum"][i] for i in day_indexes]
        tmax_ordered = [daily["temperature_2m_max"][i] for i in day_indexes]
        tmin_ordered = [daily["temperature_2m_min"][i] for i in day_indexes]

        legend_max = {"ar": "القصوى", "fr": "Maximale", "en": "Max"}[lang]
        legend_min = {"ar": "الدنيا", "fr": "Minimale", "en": "Min"}[lang]

        c1, c2 = st.columns(2)
        with c1:
            fig_rain = go.Figure(go.Bar(
                x=day_labels, y=precip_ordered,
                marker_color="#2E7C86",
                text=precip_ordered, textposition="outside",
            ))
            fig_rain.update_layout(
                title=dict(text=T["precip_forecast_title"], x=0.5),
                height=340, margin=dict(l=10, r=10, t=50, b=10),
                plot_bgcolor="white", paper_bgcolor="white",
            )
            st.plotly_chart(fig_rain, use_container_width=True, key="chart_precip_forecast")

        with c2:
            fig_temp = go.Figure()
            fig_temp.add_trace(go.Scatter(x=day_labels, y=tmax_ordered,
                                           mode="lines+markers", name=legend_max, line=dict(color="#E8794A")))
            fig_temp.add_trace(go.Scatter(x=day_labels, y=tmin_ordered,
                                           mode="lines+markers", name=legend_min, line=dict(color="#16414A")))
            fig_temp.update_layout(
                title=dict(text=T["temp_forecast_title"], x=0.5),
                height=340, margin=dict(l=10, r=10, t=50, b=10),
                plot_bgcolor="white", paper_bgcolor="white",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0.5, xanchor="center"),
            )
            st.plotly_chart(fig_temp, use_container_width=True, key="chart_temp_forecast")

        st.caption("📡 Open-Meteo API")