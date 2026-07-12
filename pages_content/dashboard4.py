import streamlit as st
import pandas as pd
import requests
import json
import os
import folium
from streamlit_folium import st_folium
from languages import TEXTS

LAT, LON = 36.6167, 8.9667

SCENARIOS = [
    {"id": "s1", "min": 20, "max": 40, "col": "Niveau de risque (20-40mm)",
     "geojson": "data/geojson/risk_20_40.geojson",
     "label": {"ar": "20-40 ملم", "fr": "20-40 mm", "en": "20-40 mm"}},
    {"id": "s2", "min": 40, "max": 70, "col": "Niveau de risque (40-70mm)",
     "geojson": "data/geojson/risk_40_70.geojson",
     "label": {"ar": "40-70 ملم", "fr": "40-70 mm", "en": "40-70 mm"}},
    {"id": "s3", "min": 70, "max": 100, "col": "Niveau de risque (70-100mm)",
     "geojson": "data/geojson/risk_70_100.geojson",
     "label": {"ar": "70-100 ملم", "fr": "70-100 mm", "en": "70-100 mm"}},
    {"id": "s4", "min": 100, "max": 999999, "col": "Niveau de risque (>100mm)",
     "geojson": "data/geojson/risk_100plus.geojson",
     "label": {"ar": "أكثر من 100 ملم", "fr": "plus de 100 mm", "en": "over 100 mm"}},
]

REAL_PALETTE = ["#91CBA8", "#DDF1B4", "#FEDF99", "#F59053", "#D7191C"]

PRIORITY_KEYWORDS = [
    "tres faible", "très faible", "very low", "faible", "low",
    "moderee", "modérée", "moyen", "moderate",
    "elevee", "élevée", "high", "tres elevee", "très élevée", "very high",
]

CATEGORIES = [
    {"id": "health", "file": "data/reports/health_facilities.csv", "icon": "🏥",
     "title": {"ar": "🏥 المؤسسات الصحية", "fr": "🏥 Établissements de santé", "en": "🏥 Health Facilities"}},
    {"id": "education", "file": "data/reports/education_facilities.csv", "icon": "🎓",
     "title": {"ar": "🎓 المؤسسات التعليمية", "fr": "🎓 Établissements éducatifs", "en": "🎓 Educational Facilities"}},
    {"id": "residential", "file": "data/reports/residential_zones.csv", "icon": "🏘️",
     "title": {"ar": "🏘️ المناطق السكنية", "fr": "🏘️ Zones résidentielles", "en": "🏘️ Residential Areas"}},
    {"id": "infrastructure", "file": "data/reports/infrastructure_networks.csv", "icon": "⚡",
     "title": {"ar": "⚡ الشبكات والمرافق", "fr": "⚡ Réseaux et infrastructures", "en": "⚡ Networks & Infrastructure"}},
    {"id": "roads", "file": "data/reports/main_roads.csv", "icon": "🛣️",
     "title": {"ar": "🛣️ المحاور الطرقية الحيوية", "fr": "🛣️ Axes routiers vitaux", "en": "🛣️ Vital Road Axes"}},
]

MAP_TXT = {
    "ar": {
        "legend_title": "🎨 درجة الخطورة:", "legend_labels": ["ضعيف جدًا", "ضعيف", "متوسط", "مرتفع", "مرتفع جدًا"],
        "risk_axis": "درجة الخطورة", "satellite": "🛰️ صور أقمار صناعية",
        "scenario_caption": "السيناريو الحالي: {label} (كمية الأمطار: {rain} ملم)",
        "report_caption": "درجات الخطورة الخاصة بسيناريو: {label}",
        "auto_rain_info": "🌐 كمية الأمطار المتوقعة اليوم (Open-Meteo): **{rain} ملم**",
        "auto_rain_error": "⚠️ تعذّر جلب بيانات Open-Meteo، جربي الإدخال اليدوي.",
        "col_missing_warning": "⚠️ عمود هذا السيناريو غير موجود بالملف.",
        "kpi_very_high": "مواقع خطر مرتفع جدًا", "kpi_high": "مواقع خطر مرتفع",
        "kpi_moderate": "مواقع خطر متوسط", "kpi_pending": "قيد التحقق الجغرافي",
        "day_today": "📍 اليوم", "day_tomorrow": "📆 غدًا", "day_after": "📆 بعد غد",
        "forecast_rain_info": "🌐 كمية الأمطار المتوقعة (Open-Meteo): **{rain} ملم**",
        "warning_system_title": "🚨 نظام الإنذار المبكر — 3 أيام قادمة",
        "warning_system_sub": "تابعي خطر الفيضان لليوم الحالي وليومين قادمين، بناءً على توقعات الأمطار.",
    },
    "fr": {
        "legend_title": "🎨 Niveau de risque :", "legend_labels": ["Très faible", "Faible", "Modéré", "Élevé", "Très élevé"],
        "risk_axis": "Degré de risque", "satellite": "🛰️ Imagerie satellite",
        "scenario_caption": "Scénario actuel : {label} (quantité de pluie : {rain} mm)",
        "report_caption": "Niveaux de risque pour le scénario : {label}",
        "auto_rain_info": "🌐 Pluie prévue aujourd'hui (Open-Meteo) : **{rain} mm**",
        "auto_rain_error": "⚠️ Impossible de récupérer les données Open-Meteo, essayez la saisie manuelle.",
        "col_missing_warning": "⚠️ La colonne de ce scénario est introuvable dans le fichier.",
        "kpi_very_high": "Sites à risque très élevé", "kpi_high": "Sites à risque élevé",
        "kpi_moderate": "Sites à risque modéré", "kpi_pending": "Vérification géographique en cours",
        "day_today": "📍 Aujourd'hui", "day_tomorrow": "📆 Demain", "day_after": "📆 Après-demain",
        "forecast_rain_info": "🌐 Pluie prévue (Open-Meteo) : **{rain} mm**",
        "warning_system_title": "🚨 Système d'alerte précoce — 3 prochains jours",
        "warning_system_sub": "Suivez le risque d'inondation pour aujourd'hui et les deux prochains jours, selon les prévisions de pluie.",
    },
    "en": {
        "legend_title": "🎨 Risk level:", "legend_labels": ["Very low", "Low", "Moderate", "High", "Very high"],
        "risk_axis": "Risk level", "satellite": "🛰️ Satellite imagery",
        "scenario_caption": "Current scenario: {label} (rainfall: {rain} mm)",
        "report_caption": "Risk levels for scenario: {label}",
        "auto_rain_info": "🌐 Today's expected rainfall (Open-Meteo): **{rain} mm**",
        "auto_rain_error": "⚠️ Unable to fetch Open-Meteo data, try manual entry.",
        "col_missing_warning": "⚠️ This scenario's column was not found in the file.",
        "kpi_very_high": "Very high risk sites", "kpi_high": "High risk sites",
        "kpi_moderate": "Moderate risk sites", "kpi_pending": "Pending geo-verification",
        "day_today": "📍 Today", "day_tomorrow": "📆 Tomorrow", "day_after": "📆 Day after tomorrow",
        "forecast_rain_info": "🌐 Expected rainfall (Open-Meteo): **{rain} mm**",
        "warning_system_title": "🚨 Early Warning System — Next 3 Days",
        "warning_system_sub": "Track flood risk for today and the next two days, based on rainfall forecasts.",
    },
}

NAME_AR = {
    "Hopital local de Bousalem": "المستشفى المحلي ببوسالم",
    "Centre local CNAM de Bousalem": "المكتب المحلي للصندوق الوطني للتأمين على المرض ببوسالم",
    "Lycee de Bousalem": "المعهد الثانوي ببوسالم",
    "Internat du Lycee de Bousalem": "المبيت الداخلي للمعهد الثانوي ببوسالم",
    "ecole primaire El Hana": "المدرسة الابتدائية الهناء",
    "Douar Mastour": "دوار مسطور",
    "Quartiers Fatouma": "أحياء فاطمة",
    "Quartier populaire 1/2/3": "الحي الشعبي 1/2/3",
    "Bourguiba": "حي بورقيبة",
    "El Achaichia": "العشايشية",
    "Ard El Fawha": "أرض الفوهة",
    "Quartier Hedi Khalil": "حي الهادي خليل",
    "Quartier Hachad": "حي حشاد",
    "El Hay El Kabir": "الحي الكبير",
    "Quartier Ennozha": "حي النزهة",
    "Quartier El Feissalia": "حي الفيصالية",
    "Rue Omar Ibn Abdelaziz": "نهج عمر بن عبد العزيز",
    "Rue du 18 Janvier (centre-ville)": "نهج 18 جانفي (وسط المدينة)",
    "Bousalem Nord": "بوسالم الشمالية",
    "Bousalem Sud": "بوسالم الجنوبية",
    "Romaini": "الرماني",
    "Brahem": "إبراهم",
    "El Marja": "المرجة",
    "Bir El Akhdar": "بئر الأخضر",
    "El Kodia": "الكدية",
    "El Mangouche": "المنقوشة",
    "Sidi Abid": "سيدي عبيد",
    "STEG - Agence de Bousalem": "الشركة التونسية للكهرباء والغاز - وكالة بوسالم",
    "SONEDE (service eau - Bousalem)": "الشركة الوطنية لاستغلال وتوزيع المياه - بوسالم",
    "Municipalite de Bousalem": "بلدية بوسالم",
    "Recette municipale de Bousalem": "القباضة البلدية ببوسالم",
    "Protection civile": "الحماية المدنية",
    "Autoroute A3 Tunis-Bousalem": "الطريق السيار A3 تونس-بوسالم",
    "Route Regionale 75 Bousalem-Tabarka": "الطريق الجهوية 75 بوسالم-طبرقة",
    "Routes locales principales (centre-ville, Place Farhat Hachad, Rue 18 Janvier)":
        "الطرقات المحلية الرئيسية (وسط المدينة، ساحة فرحات حشاد، نهج 18 جانفي)",
}


@st.cache_data(ttl=1800)
def fetch_3day_rain():
    url = (f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}"
           "&daily=precipitation_sum&timezone=Africa%2FTunis&forecast_days=3")
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()["daily"]["precipitation_sum"]


def get_scenario(rain_mm):
    if rain_mm < 20:
        return None
    for s in SCENARIOS:
        if s["min"] <= rain_mm < s["max"]:
            return s
    return SCENARIOS[-1]


@st.cache_data(ttl=3600)
def load_geojson_raw(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data(ttl=3600)
def load_csv(path):
    if not os.path.exists(path):
        return None

    raw = None
    for enc in ["utf-8", "utf-8-sig", "cp1252", "latin-1"]:
        try:
            with open(path, "r", encoding=enc) as f:
                raw = f.read()
            break
        except UnicodeDecodeError:
            continue
    if raw is None:
        return None

    lines = [l for l in raw.splitlines() if l.strip()]
    if not lines:
        return None

    header = [h.strip().strip('"') for h in lines[0].split(",")]
    name_col = header[0]
    risk_cols = header[1:5]

    rows = []
    for line in lines[1:]:
        parts = line.rsplit(",", 4)
        if len(parts) != 5:
            continue
        name = parts[0].strip().strip('"')
        try:
            values = [float(p.strip()) for p in parts[1:]]
        except ValueError:
            continue
        rows.append([name] + values)

    if not rows:
        return None

    return pd.DataFrame(rows, columns=[name_col] + risk_cols)


def detect_class_field(geo):
    features = geo.get("features", [])
    if not features:
        return None
    field_values = {}
    for f in features[:500]:
        for k, v in (f.get("properties") or {}).items():
            field_values.setdefault(k, set()).add(v)
    candidates = {k: v for k, v in field_values.items() if 2 <= len(v) <= 6}
    if not candidates:
        return None
    for k in candidates:
        kl = k.lower()
        if any(w in kl for w in ["risk", "risque", "niveau", "class", "value", "id", "dn", "gridcode"]):
            return k
    return list(candidates.keys())[0]


def order_values(values):
    try:
        return sorted(values, key=lambda x: float(x))
    except (ValueError, TypeError):
        def keyfun(v):
            s = str(v).lower()
            for i, p in enumerate(PRIORITY_KEYWORDS):
                if p in s:
                    return i
            return len(PRIORITY_KEYWORDS)
        return sorted(values, key=keyfun)


def build_real_color_map(geo, field):
    values = set()
    for f in geo.get("features", []):
        v = (f.get("properties") or {}).get(field)
        if v is not None:
            values.add(v)
    ordered = order_values(values)
    n = len(ordered)
    color_map = {}
    for i, v in enumerate(ordered):
        idx = int(i * (len(REAL_PALETTE) - 1) / max(n - 1, 1))
        color_map[v] = REAL_PALETTE[idx]
    return color_map


def make_style_function(geo, opacity):
    field = detect_class_field(geo)
    if field is None:
        def fallback_style(feature):
            return {"fillColor": "#F59053", "color": "#F59053", "weight": 1, "fillOpacity": opacity}
        return fallback_style

    color_map = build_real_color_map(geo, field)

    def style_function(feature):
        props = feature.get("properties", {}) or {}
        val = props.get(field)
        fill_color = color_map.get(val, "#9e9e9e")
        return {"fillColor": fill_color, "color": fill_color, "weight": 0.5, "fillOpacity": opacity}
    return style_function


def risk_color(value):
    idx = max(0, min(4, int(value) - 1))
    return REAL_PALETTE[idx]


def kpi_card(icon, title, avg_value):
    color = risk_color(round(avg_value))
    st.markdown(f"""
    <div style='background:white; border-radius:14px; padding:18px 10px; text-align:center;
                border-top:5px solid {color}; box-shadow:0 3px 12px rgba(0,0,0,0.08);'>
        <div style='font-size:28px;'>{icon}</div>
        <div style='font-size:11.5px; color:#666; margin-top:6px; min-height:32px;'>{title}</div>
        <div style='font-size:30px; font-weight:800; color:{color}; margin-top:4px;'>{avg_value:.1f}<span style="font-size:15px; color:#999;">/5</span></div>
    </div>
    """, unsafe_allow_html=True)


def category_bar_chart(df, name_col, risk_col, key, lang, axis_title):
    import plotly.graph_objects as go
    d = df[[name_col, risk_col]].dropna().copy()
    d[risk_col] = d[risk_col].astype(int)

    if lang == "ar":
        d[name_col] = d[name_col].apply(lambda n: NAME_AR.get(n, n))

    d = d.sort_values(risk_col, ascending=True)

    colors = [risk_color(v) for v in d[risk_col]]
    fig = go.Figure(go.Bar(
        x=d[risk_col], y=d[name_col], orientation="h",
        marker_color=colors,
        text=d[risk_col].astype(str) + " / 5", textposition="outside",
    ))
    fig.update_layout(
        height=max(280, 42 * len(d)),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(title=axis_title, range=[0, 6], dtick=1),
        plot_bgcolor="white", paper_bgcolor="white",
    )
    st.plotly_chart(fig, use_container_width=True, key=key)


def render_report(scenario, lang, M, day_id):
    dataframes = {}
    for cat in CATEGORIES:
        df = load_csv(cat["file"])
        dataframes[cat["id"]] = df

    kpi_cols = st.columns(len(CATEGORIES))
    for i, cat in enumerate(CATEGORIES):
        df = dataframes[cat["id"]]
        title = cat["title"][lang]
        with kpi_cols[i]:
            if df is not None and scenario["col"] in df.columns:
                avg_val = df[scenario["col"]].astype(float).mean()
                kpi_card(cat["icon"], title, avg_val)
            else:
                st.info(f"📄 {cat['file']}")

    st.write("")

    tabs = st.tabs([c["title"][lang] for c in CATEGORIES])
    for tab, cat in zip(tabs, CATEGORIES):
        with tab:
            df = dataframes[cat["id"]]
            if df is None:
                st.info(f"📄 {cat['file']}")
                continue
            name_col = df.columns[0]
            if scenario["col"] not in df.columns:
                st.warning(M["col_missing_warning"])
                continue
            category_bar_chart(df, name_col, scenario["col"], f"chart_{cat['id']}_{day_id}", lang, M["risk_axis"])


def render_day_section(day_id, day_title, rain_mm, lang, T, M):
    """يعرض قسمًا كاملاً (خريطة + Legend + تقرير) ليوم واحد"""
    st.subheader(day_title)

    scenario = get_scenario(rain_mm)

    if scenario is None:
        with st.container(key=f"card_risk_result_{day_id}"):
            st.success(f"### {T['no_risk_title']}")
            st.write(T["no_risk_text"])
        return

    scenario_label = scenario["label"][lang]

    with st.container(key=f"card_risk_map_{day_id}"):
        st.caption(M["scenario_caption"].format(label=scenario_label, rain=rain_mm))

        opacity = st.slider(T["opacity_label"], 0.1, 0.9, 0.65, 0.05, key=f"opacity_{day_id}")

        geo = load_geojson_raw(scenario["geojson"])
        m = folium.Map(location=[LAT, LON], zoom_start=13, tiles="OpenStreetMap", prefer_canvas=True)
        folium.TileLayer(
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr="Esri World Imagery", name=M["satellite"], overlay=False,
        ).add_to(m)

        if geo:
            style_fn = make_style_function(geo, opacity)
            folium.GeoJson(geo, name=T["risk_map_title"], style_function=style_fn).add_to(m)
        else:
            st.info(f"🗺️ {scenario['geojson']}")

        folium.LayerControl().add_to(m)
        st_folium(
            m, use_container_width=True, height=650,
            key=f"map_{day_id}_{scenario['id']}",
            returned_objects=[],
        )

        legend_html = "".join([
            f"<div style='display:flex; align-items:center; gap:8px; margin:0 14px;'>"
            f"<span style='width:22px; height:22px; background:{c}; border-radius:5px; "
            f"border:1px solid rgba(0,0,0,0.15); display:inline-block;'></span>"
            f"<span style='font-size:14px; font-weight:600; color:#333;'>{lbl}</span></div>"
            for c, lbl in zip(REAL_PALETTE, M["legend_labels"])
        ])
        st.markdown(f"""
        <div style='display:flex; justify-content:center; align-items:center; flex-wrap:wrap;
                    background:#FBFAF7; border:1px solid #E5DFD0; border-radius:10px;
                    padding:14px; margin-top:14px;'>
            <span style='font-weight:700; color:#16414A; margin-left:10px;'>{M["legend_title"]}</span>
            {legend_html}
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    with st.container(key=f"card_risk_report_{day_id}"):
        st.markdown(f"**{T['risk_report_title']}**")
        st.caption(M["report_caption"].format(label=scenario_label))
        render_report(scenario, lang, M, day_id)


def show(lang):
    T = TEXTS[lang]
    M = MAP_TXT.get(lang, MAP_TXT["ar"])

    with st.container(key="card_risk_intro"):
        st.title(T["nav_tab4"])
        st.write(M["warning_system_sub"])

    st.write("")

    try:
        rain_3days = fetch_3day_rain()
    except Exception:
        rain_3days = None

    with st.container(key="card_risk_input"):
        source = st.radio(T["rain_source_label"],
                           [T["rain_source_auto"], T["rain_source_manual"]], horizontal=True)

        if source == T["rain_source_auto"]:
            if rain_3days:
                rain_today = rain_3days[0]
                st.info(M["auto_rain_info"].format(rain=rain_today))
            else:
                st.error(M["auto_rain_error"])
                rain_today = 0
        else:
            rain_today = st.number_input(T["manual_rain_label"], min_value=0, max_value=300, value=50, step=5)

    st.write("")

    render_day_section("today", M["day_today"], rain_today, lang, T, M)

    st.write("---")

    if rain_3days and len(rain_3days) >= 3:
        rain_tomorrow = rain_3days[1]
        rain_after = rain_3days[2]

        st.info(M["forecast_rain_info"].format(rain=rain_tomorrow))
        render_day_section("tomorrow", M["day_tomorrow"], rain_tomorrow, lang, T, M)

        st.write("---")

        st.info(M["forecast_rain_info"].format(rain=rain_after))
        render_day_section("after", M["day_after"], rain_after, lang, T, M)
    else:
        st.error(M["auto_rain_error"])