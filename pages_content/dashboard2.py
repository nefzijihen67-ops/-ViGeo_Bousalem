import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from languages import TEXTS
import os

CLIMATE_TXT = {
    "ar": {
        "months": ["جانفي", "فيفري", "مارس", "أفريل", "ماي", "جوان",
                    "جويلية", "أوت", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"],
        "col_month": "الشهر", "col_precip": "الأمطار (ملم)",
        "col_tmin": "الحرارة الدنيا (°م)", "col_tavg": "الحرارة المعدل (°م)", "col_tmax": "الحرارة القصوى (°م)",
        "legend_max": "القصوى", "legend_avg": "المعدل", "legend_min": "الدنيا",
    },
    "fr": {
        "months": ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"],
        "col_month": "Mois", "col_precip": "Précipitations (mm)",
        "col_tmin": "Temp. minimale (°C)", "col_tavg": "Temp. moyenne (°C)", "col_tmax": "Temp. maximale (°C)",
        "legend_max": "Maximale", "legend_avg": "Moyenne", "legend_min": "Minimale",
    },
    "en": {
        "months": ["January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"],
        "col_month": "Month", "col_precip": "Precipitation (mm)",
        "col_tmin": "Min Temp. (°C)", "col_tavg": "Avg Temp. (°C)", "col_tmax": "Max Temp. (°C)",
        "legend_max": "Maximum", "legend_avg": "Average", "legend_min": "Minimum",
    },
}


def resolve_image(base_path):
    if os.path.exists(base_path):
        return base_path
    root, _ = os.path.splitext(base_path)
    for ext in [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG", ".webp"]:
        candidate = root + ext
        if os.path.exists(candidate):
            return candidate
    return None


def safe_image(base_path, **kwargs):
    real_path = resolve_image(base_path)
    if real_path:
        st.image(real_path, **kwargs)
    else:
        st.info(f"🖼️ ضعي الصورة هنا: {base_path}")


_section_counter = {"i": 0}


def text_image_row(title, text, img_path):
    """عنصر متعرّج: نص نصف الصفحة وصورة النصف الآخر، يتبادلون الجهة تلقائيًا"""
    i = _section_counter["i"]
    _section_counter["i"] += 1

    col_a, col_b = st.columns([1, 1])
    if i % 2 == 0:
        txt_col, img_col = col_a, col_b
    else:
        img_col, txt_col = col_a, col_b

    with txt_col:
        st.subheader(title)
        for paragraph in text.split("\n\n"):
            st.write(paragraph)
    with img_col:
        safe_image(img_path, use_container_width=True)
    st.divider()


def show(lang):
    T = TEXTS[lang]
    CL = CLIMATE_TXT.get(lang, CLIMATE_TXT["ar"])

    _section_counter["i"] = 0

    with st.container(key="card_geo_intro"):
        st.title(T["nav_tab2"])
        st.write(T["tab2_intro"])

    st.write("")

    with st.container(key="card_geo"):
        text_image_row(T["geo_title"], T["geo_text"], "assets/images/bousalem_geo_location.jpg")

    st.write("")

    with st.container(key="card_climate"):
        st.header(T["climate_title"])
        for paragraph in T["climate_text"].split("\n\n"):
            st.write(paragraph)

        climate_df = pd.DataFrame({
            CL["col_month"]: CL["months"],
            CL["col_precip"]: [97, 78, 83, 65, 43, 18, 9, 24, 55, 65, 78, 95],
            CL["col_tmin"]: [3, 4, 6, 9, 13, 17, 20, 20, 16, 11, 7, 4],
            CL["col_tavg"]: [9, 10, 12, 15, 19, 24, 27, 27, 23, 18, 13, 10],
            CL["col_tmax"]: [15, 16, 19, 22, 27, 33, 38, 39, 33, 27, 20, 16],
        })

        st.caption(T["climate_table_caption"])
        st.dataframe(climate_df, use_container_width=True, hide_index=True)

        c1, c2 = st.columns(2)
        with c1:
            fig_precip = go.Figure(go.Bar(
                x=climate_df[CL["col_month"]], y=climate_df[CL["col_precip"]],
                marker_color="#2E7C86",
            ))
            fig_precip.update_layout(
                title=dict(text=T["climate_precip_title"], x=0.5),
                height=340, margin=dict(l=10, r=10, t=50, b=10),
                plot_bgcolor="white", paper_bgcolor="white",
            )
            st.plotly_chart(fig_precip, use_container_width=True, key="chart_precip_bousalem")

        with c2:
            fig_temp = go.Figure()
            fig_temp.add_trace(go.Scatter(x=climate_df[CL["col_month"]], y=climate_df[CL["col_tmax"]],
                                           mode="lines+markers", name=CL["legend_max"], line=dict(color="#E8794A")))
            fig_temp.add_trace(go.Scatter(x=climate_df[CL["col_month"]], y=climate_df[CL["col_tavg"]],
                                           mode="lines+markers", name=CL["legend_avg"], line=dict(color="#16414A")))
            fig_temp.add_trace(go.Scatter(x=climate_df[CL["col_month"]], y=climate_df[CL["col_tmin"]],
                                           mode="lines+markers", name=CL["legend_min"], line=dict(color="#40916C")))
            fig_temp.update_layout(
                title=dict(text=T["climate_temp_title"], x=0.5),
                height=340, margin=dict(l=10, r=10, t=50, b=10),
                plot_bgcolor="white", paper_bgcolor="white",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0.5, xanchor="center"),
            )
            st.plotly_chart(fig_temp, use_container_width=True, key="chart_temp_bousalem")

    st.write("")

    with st.container(key="card_geology"):
        text_image_row(T["geology_title"], T["geology_text"], "assets/images/bousalem_geology.jpg")

    st.write("")

    with st.container(key="card_hydro"):
        text_image_row(T["hydro_title"], T["hydro_text"], "assets/images/bousalem_hydro_network.jpg")

    st.write("")

    with st.container(key="card_landcover"):
        text_image_row(T["landcover_title"], T["landcover_text"], "assets/images/bousalem_land_cover.jpg")

    st.write("")

    with st.container(key="card_historical"):
        st.header(T["hist_title"])
        st.caption(T["hist_subtitle"])
        st.write("")

        text_image_row(T["flood2003_title"], T["flood2003_text"], "assets/images/bousalem_flood_2003.jpg")
        text_image_row(T["flood2015_title"], T["flood2015_text"], "assets/images/bousalem_flood_2015.jpg")

        st.caption(T["video_caption"])
        st.video("https://youtu.be/J3WRrjoePiE?si=afgcaLkkfdZmBE2k")