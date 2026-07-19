import streamlit as st
import pandas as pd
import numpy as np
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
SAFE_COLOR = "#B9C7C2"

PRIORITY_KEYWORDS = [
    "tres faible", "très faible", "very low", "faible", "low",
    "moderee", "modérée", "moyen", "moderate",
    "elevee", "élevée", "high", "tres elevee", "très élevée", "very high",
]

AREA_DATA = {
    "s1": {0: 247.656, 5: 31.382},
    "s2": {0: 88.372, 4: 158.964, 5: 31.382},
    "s3": {0: 18.122, 3: 70.250, 4: 158.964, 5: 31.382},
    "s4": {0: 5.284, 2: 12.838, 3: 70.250, 4: 158.964, 5: 31.382},
}

AREA_VALUE_LABELS_IDX = {2: 1, 3: 2, 4: 3, 5: 4}

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
        "day_today": "📍 اليوم", "day_tomorrow": "📆 غدًا", "day_after": "📆 بعد غد",
        "forecast_rain_info": "🌐 كمية الأمطار المتوقعة (Open-Meteo): **{rain} ملم**",
        "warning_system_sub": "تابعي خطر الفيضان لليوم الحالي وليومين قادمين، بناءً على توقعات الأمطار.",
        "area_col_level": "درجة الخطورة", "area_col_km2": "المساحة (كم²)", "area_col_pct": "النسبة",
        "unit_km2": "كم²",
        "search_label": "🔍 ابحثي عن مكان (مدرسة، حي، شارع...)",
        "search_placeholder": "مثال: المعهد الثانوي ببوسالم",
        "search_button": "بحث",
        "search_not_found": "⚠️ لم يتم العثور على هذا المكان. جربي كتابة اسم أدق، أو أضيفي كلمة 'بوسالم' لتحسين الدقة.",
        "risk_found_prefix": "📍 نتيجة البحث",
        "risk_at_location": "درجة الخطر بهذا الموقع",
        "risk_unknown": "⚠️ الموقع خارج نطاق خريطة الخطر الحالية، أو تعذّر تحديد درجة الخطورة بدقة.",
        "indexing_msg": "⏳ يتم تجهيز بيانات الموقع الجغرافية لأول مرة (قد يستغرق بضع ثوانٍ)...",
    },
    "fr": {
        "legend_title": "🎨 Niveau de risque :", "legend_labels": ["Très faible", "Faible", "Modéré", "Élevé", "Très élevé"],
        "risk_axis": "Degré de risque", "satellite": "🛰️ Imagerie satellite",
        "scenario_caption": "Scénario actuel : {label} (quantité de pluie : {rain} mm)",
        "report_caption": "Niveaux de risque pour le scénario : {label}",
        "auto_rain_info": "🌐 Pluie prévue aujourd'hui (Open-Meteo) : **{rain} mm**",
        "auto_rain_error": "⚠️ Impossible de récupérer les données Open-Meteo, essayez la saisie manuelle.",
        "col_missing_warning": "⚠️ La colonne de ce scénario est introuvable dans le fichier.",
        "day_today": "📍 Aujourd'hui", "day_tomorrow": "📆 Demain", "day_after": "📆 Après-demain",
        "forecast_rain_info": "🌐 Pluie prévue (Open-Meteo) : **{rain} mm**",
        "warning_system_sub": "Suivez le risque d'inondation pour aujourd'hui et les deux prochains jours, selon les prévisions de pluie.",
        "area_col_level": "Niveau de risque", "area_col_km2": "Superficie (km²)", "area_col_pct": "Pourcentage",
        "unit_km2": "km²",
        "search_label": "🔍 Rechercher un lieu (école, quartier, rue...)",
        "search_placeholder": "Exemple : Lycée de Bousalem",
        "search_button": "Rechercher",
        "search_not_found": "⚠️ Lieu introuvable. Essayez un nom plus précis, ou ajoutez 'Bousalem' pour améliorer la précision.",
        "risk_found_prefix": "📍 Résultat de la recherche",
        "risk_at_location": "Niveau de risque à cet endroit",
        "risk_unknown": "⚠️ Le lieu est hors de la carte de risque actuelle, ou le niveau n'a pas pu être déterminé avec précision.",
        "indexing_msg": "⏳ Préparation des données géographiques pour la première fois (quelques secondes)...",
    },
    "en": {
        "legend_title": "🎨 Risk level:", "legend_labels": ["Very low", "Low", "Moderate", "High", "Very high"],
        "risk_axis": "Risk level", "satellite": "🛰️ Satellite imagery",
        "scenario_caption": "Current scenario: {label} (rainfall: {rain} mm)",
        "report_caption": "Risk levels for scenario: {label}",
        "auto_rain_info": "🌐 Today's expected rainfall (Open-Meteo): **{rain} mm**",
        "auto_rain_error": "⚠️ Unable to fetch Open-Meteo data, try manual entry.",
        "col_missing_warning": "⚠️ This scenario's column was not found in the file.",
        "day_today": "📍 Today", "day_tomorrow": "📆 Tomorrow", "day_after": "📆 Day after tomorrow",
        "forecast_rain_info": "🌐 Expected rainfall (Open-Meteo): **{rain} mm**",
        "warning_system_sub": "Track flood risk for today and the next two days, based on rainfall forecasts.",
        "area_col_level": "Risk level", "area_col_km2": "Area (km²)", "area_col_pct": "Percentage",
        "unit_km2": "km²",
        "search_label": "🔍 Search a place (school, neighborhood, street...)",
        "search_placeholder": "Example: Bousalem High School",
        "search_button": "Search",
        "search_not_found": "⚠️ Place not found. Try a more precise name, or add 'Bousalem' to improve accuracy.",
        "risk_found_prefix": "📍 Search result",
        "risk_at_location": "Risk level at this location",
        "risk_unknown": "⚠️ Location is outside the current risk map, or the risk level could not be determined precisely.",
        "indexing_msg": "⏳ Preparing geographic data for the first time (a few seconds)...",
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


def get_scenario_index(rain_mm):
    if rain_mm < 20:
        return None
    for i, s in enumerate(SCENARIOS):
        if s["min"] <= rain_mm < s["max"]:
            return i
    return len(SCENARIOS) - 1


def get_scenario(rain_mm, bump=0):
    idx = get_scenario_index(rain_mm)
    if idx is None:
        return None
    idx = min(idx + bump, len(SCENARIOS) - 1)
    return SCENARIOS[idx]


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


def area_stat_card(icon, label, value_text, color):
    st.markdown(f"""
    <div style='background:white; border-radius:14px; padding:20px 14px; text-align:center;
                border-top:5px solid {color}; box-shadow:0 3px 12px rgba(0,0,0,0.08); height:100%;'>
        <div style='font-size:30px; line-height:1;'>{icon}</div>
        <div style='font-size:12.5px; color:#666; margin-top:8px;'>{label}</div>
        <div style='font-size:26px; font-weight:800; color:{color}; margin-top:4px;'>{value_text}</div>
    </div>
    """, unsafe_allow_html=True)


def area_section(scenario_id, lang, T, M, key):
    """قسم احترافي: بطاقات إحصائية + رسم دائري بعرض كامل + جدول أسفله بعرض كامل"""
    import plotly.graph_objects as go
    data = AREA_DATA.get(scenario_id, {})
    if not data:
        return

    unit = M["unit_km2"]
    rows = []
    for val in sorted(data.keys()):
        area = data[val]
        if val == 0:
            label = T["area_safe_label"]
            color = SAFE_COLOR
        else:
            idx = AREA_VALUE_LABELS_IDX.get(val, 0)
            label = M["legend_labels"][idx]
            color = REAL_PALETTE[idx]
        rows.append({"label": label, "area": area, "color": color})

    total_area = sum(r["area"] for r in rows)
    flooded_area = sum(r["area"] for r in rows if r["label"] != T["area_safe_label"])

    c1, c2 = st.columns(2)
    with c1:
        area_stat_card("🗺️", T["area_total_metric"], f"{total_area:.1f} {unit}", "#16414A")
    with c2:
        area_stat_card("🌊", T["area_flooded_metric"], f"{flooded_area:.1f} {unit}", "#D7191C")

    st.write("")

    fig = go.Figure(data=[go.Pie(
        labels=[r["label"] for r in rows],
        values=[r["area"] for r in rows],
        hole=0.55,
        marker=dict(colors=[r["color"] for r in rows], line=dict(color="white", width=2)),
        textinfo="percent", textposition="outside",
        showlegend=False,
    )])
    fig.update_layout(
        title=dict(text=T["area_chart_title"], x=0.5, font=dict(size=16)),
        height=420, margin=dict(l=10, r=10, t=60, b=10),
    )
    st.plotly_chart(fig, use_container_width=True, key=key)

    st.markdown(f"<div style='font-weight:700; color:#16414A; margin:10px 0; text-align:center;'>{M['area_col_level']} — {M['area_col_km2']} — {M['area_col_pct']}</div>", unsafe_allow_html=True)

    cols = st.columns(len(rows))
    for col, r in zip(cols, rows):
        pct = (r["area"] / total_area * 100) if total_area else 0
        with col:
            st.markdown(f"""
            <div style='background:#FBFAF7; border-radius:10px; padding:14px 8px; text-align:center;
                        border-top:4px solid {r["color"]};'>
                <div style='font-size:12.5px; font-weight:700; color:#333; min-height:34px;'>{r["label"]}</div>
                <div style='font-size:16px; font-weight:800; color:{r["color"]}; margin-top:6px;'>{r["area"]:.2f}</div>
                <div style='font-size:11px; color:#888;'>{unit} &nbsp;·&nbsp; {pct:.1f}%</div>
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


# ============================================================
# البحث الجغرافي (Geocoding) + تحديد الخطر عند نقطة (Point-in-Polygon)
# ============================================================
def geocode_place(query):
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": f"{query}, Bousalem, Tunisia",
            "format": "json",
            "limit": 1,
            "viewbox": "8.75,36.70,9.15,36.45",
            "bounded": 0,
        }
        headers = {"User-Agent": "ViGeo-Bousalem-FloodDashboard/1.0"}
        r = requests.get(url, params=params, headers=headers, timeout=8)
        r.raise_for_status()
        results = r.json()
        if results:
            return float(results[0]["lat"]), float(results[0]["lon"]), results[0].get("display_name", query)
    except Exception:
        pass
    return None


def _geom_bbox(geom):
    xs, ys = [], []

    def walk(c):
        if not c:
            return
        if isinstance(c[0], (int, float)):
            xs.append(c[0])
            ys.append(c[1])
        else:
            for sub in c:
                walk(sub)
    try:
        walk(geom.get("coordinates"))
    except Exception:
        return None
    if not xs:
        return None
    return min(xs), min(ys), max(xs), max(ys)


def _point_in_ring(x, y, ring):
    inside = False
    n = len(ring)
    j = n - 1
    for i in range(n):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-15) + xi):
            inside = not inside
        j = i
    return inside


def _point_in_geom(x, y, geom):
    gtype = geom.get("type")
    coords = geom.get("coordinates")
    if gtype == "Polygon":
        if not coords or not _point_in_ring(x, y, coords[0]):
            return False
        for hole in coords[1:]:
            if _point_in_ring(x, y, hole):
                return False
        return True
    if gtype == "MultiPolygon":
        for poly in coords:
            if not poly or not _point_in_ring(x, y, poly[0]):
                continue
            in_hole = any(_point_in_ring(x, y, h) for h in poly[1:])
            if not in_hole:
                return True
        return False
    return False


@st.cache_data(ttl=3600, show_spinner=False)
def build_spatial_lookup(geojson_path):
    geo = load_geojson_raw(geojson_path)
    if not geo:
        return None
    field = detect_class_field(geo)
    if not field:
        return None
    bboxes, values, geoms = [], [], []
    for f in geo.get("features", []):
        geom = f.get("geometry") or {}
        bbox = _geom_bbox(geom)
        if bbox is None:
            continue
        bboxes.append(bbox)
        values.append((f.get("properties") or {}).get(field))
        geoms.append(geom)
    if not bboxes:
        return None
    return {"arr": np.array(bboxes, dtype=float), "values": values, "geoms": geoms}


def get_risk_value_at_point(lookup, lon, lat):
    if lookup is None:
        return None
    arr = lookup["arr"]
    mask = (arr[:, 0] <= lon) & (lon <= arr[:, 2]) & (arr[:, 1] <= lat) & (lat <= arr[:, 3])
    idxs = np.nonzero(mask)[0]
    for i in idxs:
        if _point_in_geom(lon, lat, lookup["geoms"][i]):
            return lookup["values"][i]
    if len(idxs) > 0:
        return lookup["values"][idxs[0]]
    return None


def render_search_box(day_id, T, M, geo, geojson_path):
    """خانة البحث عن مكان + النتيجة: إحداثيات + درجة الخطر عند تلك النقطة"""
    with st.container(key=f"card_search_{day_id}"):
        col_input, col_btn = st.columns([4, 1])
        with col_input:
            query = st.text_input(M["search_label"], key=f"search_input_{day_id}",
                                   placeholder=M["search_placeholder"], label_visibility="visible")
        with col_btn:
            st.write("")
            clicked = st.button(M["search_button"], key=f"search_btn_{day_id}", use_container_width=True)

    result_key = f"search_result_{day_id}"
    if clicked:
        if query and query.strip():
            geo_result = geocode_place(query.strip())
            if geo_result:
                st.session_state[result_key] = geo_result
            else:
                st.session_state[result_key] = None
                st.error(M["search_not_found"])
        else:
            st.session_state[result_key] = None

    search_result = st.session_state.get(result_key)

    risk_label_html = ""
    if search_result:
        slat, slon, sname = search_result
        with st.spinner(M["indexing_msg"]):
            lookup = build_spatial_lookup(geojson_path)
            val = get_risk_value_at_point(lookup, slon, slat) if lookup else None

        legend_labels = M["legend_labels"]
        if val is not None:
            try:
                ordered = order_values(set(lookup["values"]))
                idx = ordered.index(val)
                n = len(ordered)
                label_idx = int(idx * (len(legend_labels) - 1) / max(n - 1, 1))
                risk_text = legend_labels[label_idx]
                risk_color_hex = REAL_PALETTE[label_idx]
            except Exception:
                risk_text = None
                risk_color_hex = "#9e9e9e"
        else:
            risk_text = None
            risk_color_hex = "#9e9e9e"

        if risk_text:
            risk_label_html = f"""
            <div style='background:{risk_color_hex}18; border-right:5px solid {risk_color_hex};
                        border-radius:10px; padding:14px 18px; margin-top:10px;'>
                <div style='font-weight:700; color:#16414A; font-size:14px;'>{M["risk_found_prefix"]}: {sname}</div>
                <div style='font-size:15px; margin-top:4px;'>{M["risk_at_location"]}: 
                    <span style='color:{risk_color_hex}; font-weight:800;'>{risk_text}</span>
                </div>
            </div>
            """
        else:
            risk_label_html = f"""
            <div style='background:#F0F0F0; border-right:5px solid #9e9e9e;
                        border-radius:10px; padding:14px 18px; margin-top:10px;'>
                <div style='font-weight:700; color:#16414A; font-size:14px;'>{M["risk_found_prefix"]}: {sname}</div>
                <div style='font-size:13.5px; margin-top:4px; color:#666;'>{M["risk_unknown"]}</div>
            </div>
            """
        st.markdown(risk_label_html, unsafe_allow_html=True)

    return search_result


def render_day_section(day_id, day_title, rain_mm, lang, T, M, bump=0):
    st.subheader(day_title)

    scenario = get_scenario(rain_mm, bump=bump)

    if scenario is None:
        with st.container(key=f"card_risk_result_{day_id}"):
            st.success(f"### {T['no_risk_title']}")
            st.write(T["no_risk_text"])
        return

    scenario_label = scenario["label"][lang]
    geo = load_geojson_raw(scenario["geojson"])

    search_result = render_search_box(day_id, T, M, geo, scenario["geojson"])

    with st.container(key=f"card_risk_map_{day_id}"):
        st.caption(M["scenario_caption"].format(label=scenario_label, rain=rain_mm))
        if bump > 0:
            st.warning(T["dam_release_active_badge"])

        opacity = st.slider(T["opacity_label"], 0.1, 0.9, 0.65, 0.05, key=f"opacity_{day_id}")

        map_center = [LAT, LON]
        zoom = 13
        if search_result:
            map_center = [search_result[0], search_result[1]]
            zoom = 17

        m = folium.Map(location=map_center, zoom_start=zoom, tiles="OpenStreetMap", prefer_canvas=True)
        folium.TileLayer(
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr="Esri World Imagery", name=M["satellite"], overlay=False,
        ).add_to(m)

        if geo:
            style_fn = make_style_function(geo, opacity)
            folium.GeoJson(geo, name=T["risk_map_title"], style_function=style_fn).add_to(m)
        else:
            st.info(f"🗺️ {scenario['geojson']}")

        if search_result:
            slat, slon, sname = search_result
            folium.Marker(
                [slat, slon], tooltip=sname,
                icon=folium.Icon(color="black", icon="map-marker", prefix="fa"),
            ).add_to(m)

        folium.LayerControl().add_to(m)
        st_folium(
            m, use_container_width=True, height=650,
            key=f"map_{day_id}_{scenario['id']}_{'s' if search_result else 'n'}",
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

    with st.container(key=f"card_risk_area_{day_id}"):
        area_section(scenario["id"], lang, T, M, key=f"area_chart_{day_id}")

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

    st.markdown(f"""
    <div style='background:#FDEDEC; border-right:5px solid #C0392B; border-radius:10px;
                padding:16px 20px; margin-top:14px;'>
        <div style='font-weight:800; color:#C0392B; font-size:15px;'>{T["disclaimer_title"]}</div>
        <div style='font-size:13.5px; color:#7B241C; margin-top:6px; line-height:1.6;'>{T["disclaimer_text"]}</div>
    </div>
    """, unsafe_allow_html=True)

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
        dam_release = st.checkbox(T["dam_release_label"], value=False)
        st.caption(T["dam_release_note"])

    st.write("")

    render_day_section("today", M["day_today"], rain_today, lang, T, M, bump=1 if dam_release else 0)

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