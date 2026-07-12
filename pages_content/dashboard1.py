import streamlit as st
from languages import TEXTS
import plotly.graph_objects as go
import os

RISK_COLORS = ["#40916C", "#95D5B2", "#F4C542", "#E8794A", "#C0392B"]
YEARS = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
NO_DATA_COLOR = "#C9C9C9"

# ============================================================
# نصوص الرسوم البيانية المترجمة (عناوين، محاور، Hover) - غير موجودة بـ languages.py
# ============================================================
CHART_TXT = {
    "ar": {
        "cause_chart_titles": ["شدة الأمطار", "الانحدار", "التربة", "كثافة الشبكة المائية", "الجيولوجيا"],
        "soil_labels": ["رملية", "طينية-رملية خفيفة", "طينية متوسطة", "طينية ثقيلة", "أسطح معبّدة"],
        "geo_labels": ["صخور منفذة جدًا", "منفذة", "متوسطة", "غير منفذة", "غير منفذة جدًا"],
        "risk_axis": "درجة الخطورة",
        "legend_no_data": "بدون بيانات دقيقة",
        "legend_low": "ضعيف", "legend_mod": "متوسط", "legend_high": "شديد جدًا",
        "global_title": "🌍 الخسائر عالميًا (2016-2026)",
        "tn_title": "🇹🇳 الخسائر في تونس (2016-2026)",
        "econ_global_y": "مليار دولار", "econ_tn_y": "مؤشر الشدة (0-3)",
        "social_global_y": "عدد الوفيات (تقديري)", "social_tn_y": "عدد الوفيات",
        "env_y": "مؤشر الشدة (0-3)",
        "econ_global_note": "🌍 أرقام حقيقية من المصدر. اللون الرمادي = رقم دقيق غير مذكور بالنص.",
        "econ_tn_note": "🇹🇳 مؤشر وصفي (0-3) لأن أغلب السنوات بدون رقم دولاري دقيق، عدا 2018 (110 مليون $، كارثة نابل).",
        "social_global_note": "🌍 أرقام تقريبية مبنية على أوصاف نصية (مئات/آلاف/عشرات).",
        "social_tn_note": "🇹🇳 أرقام حقيقية مذكورة صراحة بالمصدر لكل سنة.",
        "env_global_note": "🌍 مؤشر وصفي (0-3) مبني على شدة الوصف النصي لكل سنة.",
        "env_tn_note": "🇹🇳 نفس المؤشر الوصفي (0-3) مطبّق على وصف تونس لكل سنة.",
        "econ_global_hover": [
            "فيضانات يانغتسي وأوروبا", "بيانات غير متوفرة بدقة", "فيضانات كيرالا بالهند",
            "الغرب الأوسط الأمريكي", "الصين والسودان وشرق أفريقيا", "غرب أوروبا (ألمانيا وبلجيكا)",
            "فيضانات باكستان", "عاصفة دانيال وإيطاليا", "بيانات غير متوفرة بدقة",
            "عاصفة بوريس وفيضانات أوروبا", "بيانات غير متوفرة بدقة",
        ],
        "econ_tn_hover": [
            "خسائر متوسطة (سيارات ومحلات)", "استقرار اقتصادي، خسائر صيانة طفيفة", "كارثة نابل: 110 مليون دولار",
            "خسائر تجارية محلية محدودة", "تضرر مسالك فلاحية بالوسط", "توقف نشاط الشركات بتونس الكبرى",
            "لا أضرار (سنة جفاف)", "خسائر طفيفة جدًا", "ميزانية طوارئ استثنائية",
            "لا خسائر مباشرة، ارتفاع التأمين +50%", "فيضانات جانفي: تضرر آلاف الهكتارات",
        ],
        "social_global_hover": [
            "تقديري: مئات الوفيات (الصين وأوروبا)", "جنوب آسيا: أكثر من 1200 وفاة", "غير مذكور صراحة",
            "غير مذكور صراحة", "غير مذكور صراحة", "ألمانيا وبلجيكا: أكثر من 200 وفاة",
            "باكستان: 1700 وفاة", "تقديري: آلاف الوفيات (درنة)", "تقديري: عشرات الوفيات (فالنسيا)",
            "غير مذكور صراحة (نزوح فقط)", "35.1 مليون معرّض للخطر عالميًا (وليس وفيات)",
        ],
        "social_tn_hover": [
            "حالتا وفاة غرقًا", "لا خسائر بشرية", "كارثة نابل: 6 وفيات", "لا وفيات مذكورة",
            "6 وفيات (تالة وسيدي بوزيد)", "تعطل الدراسة والمرافق (بدون وفيات)", "لا تداعيات اجتماعية (جفاف)",
            "عزل مؤقت بدون وفيات", "حالة استنفار بدون وفيات مذكورة", "إجلاء استباقي بدون وفيات",
            "فيضانات جانفي: 5-6 وفيات، نزوح 25 ألف شخص",
        ],
        "env_global_hover": [
            "تلوث كثيف بالنفايات الكيميائية شرق آسيا", "تدمير النظم النهرية بالهند وبنغلاديش",
            "تلوث مياه جوفية بمناطق صناعية آسيوية", "تسرب أسمدة لخليج المكسيك",
            "تلوث نهر النيل بمياه الصرف", "تدمير كامل لنظم بيئية نهرية بألمانيا",
            "غمر ثلث باكستان وتدمير التنوع البيولوجي", "انجراف ساحلي ضخم بشرق ليبيا",
            "تلوث بالمحروقات والمعادن الثقيلة غرب أوروبا", "تخثث كيميائي ببحيرات أوروبا",
            "تدهور جودة المياه العذبة بالبحر المتوسط",
        ],
        "env_tn_hover": [
            "تلوث موضعي بالسباخ القريبة من المدن", "ترسبات طفيفة بالسدود الشمالية",
            "تجريف حاد للتربة وتدمير غابات القوارص بالوطن القبلي", "تراكم نفايات بلاستيكية بالأودية",
            "جرف تربة سطحية وتوحل بحيرات جبلية", "تلوث مؤقت لبحيرة تونس",
            "لا أثر بيئي هيدروليكي (جفاف)", "ترسبات طينية عادية بدون تأثير حرج",
            "انجراف موضعي بباجة وجندوبة", "ضغط هيدروليكي وتراكم نفايات بسبخة السيجومي",
            "تجريف واسع وتآكل ساحلي وتوحل سدود مجردة وكساب",
        ],
    },
    "fr": {
        "cause_chart_titles": ["Intensité des précipitations", "Pente", "Type de sol", "Densité hydrographique", "Géologie"],
        "soil_labels": ["Sableux", "Argilo-sableux léger", "Argileux modéré", "Argileux lourd", "Surfaces imperméabilisées"],
        "geo_labels": ["Roches très perméables", "Perméables", "Modérées", "Peu perméables", "Imperméables"],
        "risk_axis": "Degré de risque",
        "legend_no_data": "Données non précises",
        "legend_low": "Faible", "legend_mod": "Modéré", "legend_high": "Très élevé",
        "global_title": "🌍 Pertes mondiales (2016-2026)",
        "tn_title": "🇹🇳 Pertes en Tunisie (2016-2026)",
        "econ_global_y": "Milliards de $", "econ_tn_y": "Indice de sévérité (0-3)",
        "social_global_y": "Nombre de décès (estimé)", "social_tn_y": "Nombre de décès",
        "env_y": "Indice de sévérité (0-3)",
        "econ_global_note": "🌍 Chiffres réels issus de la source. Gris = chiffre précis non mentionné dans le texte.",
        "econ_tn_note": "🇹🇳 Indice descriptif (0-3) : la plupart des années sans montant précis, sauf 2018 (110 M$, catastrophe de Nabeul).",
        "social_global_note": "🌍 Chiffres approximatifs basés sur des descriptions textuelles (centaines/milliers/dizaines).",
        "social_tn_note": "🇹🇳 Chiffres réels explicitement mentionnés dans la source pour chaque année.",
        "env_global_note": "🌍 Indice descriptif (0-3) basé sur l'intensité de la description textuelle de chaque année.",
        "env_tn_note": "🇹🇳 Même indice descriptif (0-3) appliqué à la description de la Tunisie chaque année.",
        "econ_global_hover": [
            "Inondations du Yangtsé et d'Europe", "Données non précises", "Inondations du Kerala (Inde)",
            "Midwest américain", "Chine, Soudan et Afrique de l'Est", "Europe de l'Ouest (Allemagne, Belgique)",
            "Inondations au Pakistan", "Tempête Daniel et Italie", "Données non précises",
            "Tempête Boris et inondations en Europe", "Données non précises",
        ],
        "econ_tn_hover": [
            "Pertes modérées (voitures et commerces)", "Stabilité économique, pertes d'entretien mineures",
            "Catastrophe de Nabeul : 110 millions $", "Pertes commerciales locales limitées",
            "Pistes agricoles endommagées dans le Centre", "Arrêt d'activité des entreprises du Grand Tunis",
            "Aucun dégât (année de sécheresse)", "Pertes très légères", "Budget d'urgence exceptionnel",
            "Aucune perte directe, hausse de l'assurance de +50%", "Inondations de janvier : milliers d'hectares touchés",
        ],
        "social_global_hover": [
            "Estimation : centaines de morts (Chine et Europe)", "Asie du Sud : plus de 1200 morts", "Non précisé",
            "Non précisé", "Non précisé", "Allemagne et Belgique : plus de 200 morts",
            "Pakistan : 1700 morts", "Estimation : milliers de morts (Derna)", "Estimation : dizaines de morts (Valence)",
            "Non précisé (déplacement uniquement)", "35,1 millions de personnes exposées dans le monde (pas des décès)",
        ],
        "social_tn_hover": [
            "Deux décès par noyade", "Aucune perte humaine", "Catastrophe de Nabeul : 6 morts", "Aucun décès rapporté",
            "6 morts (Thala et Sidi Bouzid)", "Perturbation des écoles et services (sans décès)",
            "Aucun impact social (sécheresse)", "Isolement temporaire sans décès", "État d'alerte sans décès rapporté",
            "Évacuation préventive sans décès", "Inondations de janvier : 5-6 morts, déplacement de 25 000 personnes",
        ],
        "env_global_hover": [
            "Pollution chimique intense en Asie de l'Est", "Destruction des écosystèmes fluviaux en Inde et au Bangladesh",
            "Pollution des nappes phréatiques dans les zones industrielles d'Asie", "Fuite d'engrais vers le golfe du Mexique",
            "Pollution du Nil par les eaux usées", "Destruction totale des écosystèmes fluviaux en Allemagne",
            "Un tiers du Pakistan submergé, biodiversité détruite", "Érosion côtière massive dans l'est de la Libye",
            "Pollution aux hydrocarbures et métaux lourds en Europe de l'Ouest", "Eutrophisation chimique des lacs européens",
            "Dégradation de la qualité de l'eau douce en Méditerranée",
        ],
        "env_tn_hover": [
            "Pollution localisée des sebkhas proches des villes", "Légers dépôts dans les barrages du Nord",
            "Érosion sévère des sols et destruction des vergers d'agrumes au Cap Bon",
            "Accumulation de déchets plastiques dans les oueds", "Érosion des sols et envasement des lacs de montagne",
            "Pollution temporaire du lac de Tunis", "Aucun impact hydrologique environnemental (sécheresse)",
            "Dépôts limoneux normaux sans impact critique", "Érosion localisée à Béja et Jendouba",
            "Pression hydraulique et déchets à la sebkhet Sijoumi",
            "Érosion étendue et envasement des barrages de la Medjerda et Kasseb",
        ],
    },
    "en": {
        "cause_chart_titles": ["Rainfall intensity", "Slope", "Soil type", "Drainage density", "Geology"],
        "soil_labels": ["Sandy", "Light sandy-clay", "Moderate clay", "Heavy clay", "Paved surfaces"],
        "geo_labels": ["Very permeable rocks", "Permeable", "Moderate", "Low permeability", "Impermeable"],
        "risk_axis": "Risk level",
        "legend_no_data": "No precise data",
        "legend_low": "Low", "legend_mod": "Moderate", "legend_high": "Very high",
        "global_title": "🌍 Global losses (2016-2026)",
        "tn_title": "🇹🇳 Losses in Tunisia (2016-2026)",
        "econ_global_y": "Billion USD", "econ_tn_y": "Severity index (0-3)",
        "social_global_y": "Deaths (estimated)", "social_tn_y": "Deaths",
        "env_y": "Severity index (0-3)",
        "econ_global_note": "🌍 Real figures from the source. Grey = precise figure not mentioned in the text.",
        "econ_tn_note": "🇹🇳 Descriptive index (0-3): most years have no precise dollar amount, except 2018 ($110M, Nabeul disaster).",
        "social_global_note": "🌍 Approximate figures based on textual descriptions (hundreds/thousands/dozens).",
        "social_tn_note": "🇹🇳 Real figures explicitly stated in the source for each year.",
        "env_global_note": "🌍 Descriptive index (0-3) based on the intensity of the textual description for each year.",
        "env_tn_note": "🇹🇳 Same descriptive index (0-3) applied to Tunisia's description for each year.",
        "econ_global_hover": [
            "Yangtze and Europe floods", "Data not precisely available", "Kerala floods (India)",
            "US Midwest", "China, Sudan and East Africa", "Western Europe (Germany, Belgium)",
            "Pakistan floods", "Storm Daniel and Italy", "Data not precisely available",
            "Storm Boris and Europe floods", "Data not precisely available",
        ],
        "econ_tn_hover": [
            "Moderate losses (cars and shops)", "Economic stability, minor maintenance costs",
            "Nabeul disaster: $110 million", "Limited local commercial losses",
            "Damaged agricultural tracks in central Tunisia", "Business shutdown in Greater Tunis",
            "No damage (drought year)", "Very minor losses", "Exceptional emergency budget",
            "No direct losses, insurance uptake +50%", "January floods: thousands of hectares affected",
        ],
        "social_global_hover": [
            "Estimated: hundreds of deaths (China and Europe)", "South Asia: over 1200 deaths", "Not explicitly stated",
            "Not explicitly stated", "Not explicitly stated", "Germany and Belgium: over 200 deaths",
            "Pakistan: 1700 deaths", "Estimated: thousands of deaths (Derna)", "Estimated: dozens of deaths (Valencia)",
            "Not explicitly stated (displacement only)", "35.1 million people exposed globally (not deaths)",
        ],
        "social_tn_hover": [
            "Two deaths by drowning", "No human losses", "Nabeul disaster: 6 deaths", "No deaths reported",
            "6 deaths (Thala and Sidi Bouzid)", "School and service disruption (no deaths)",
            "No social impact (drought)", "Temporary isolation, no deaths", "Alert status, no deaths reported",
            "Preemptive evacuation, no deaths", "January floods: 5-6 deaths, 25,000 displaced",
        ],
        "env_global_hover": [
            "Intense chemical pollution in East Asia", "Destruction of river ecosystems in India and Bangladesh",
            "Groundwater pollution in Asian industrial areas", "Fertilizer leak into the Gulf of Mexico",
            "Nile pollution from sewage water", "Total destruction of river ecosystems in Germany",
            "A third of Pakistan flooded, biodiversity destroyed", "Massive coastal erosion in eastern Libya",
            "Hydrocarbon and heavy metal pollution in Western Europe", "Chemical eutrophication of European lakes",
            "Degradation of freshwater quality in the Mediterranean",
        ],
        "env_tn_hover": [
            "Localized pollution of sebkhas near cities", "Minor sediment deposits in northern dams",
            "Severe soil erosion and destruction of citrus orchards in Cap Bon",
            "Plastic waste accumulation in wadis", "Surface soil erosion and siltation of mountain lakes",
            "Temporary pollution of Lake of Tunis", "No hydrological environmental impact (drought)",
            "Normal silt deposits without critical impact", "Localized erosion in Béja and Jendouba",
            "Hydraulic pressure and waste at Sebkhet Sijoumi",
            "Extensive erosion and siltation of Medjerda and Kasseb dams",
        ],
    },
}


def safe_image(base_path, **kwargs):
    real_path = None
    if os.path.exists(base_path):
        real_path = base_path
    else:
        root, _ = os.path.splitext(base_path)
        for ext in [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG", ".webp"]:
            candidate = root + ext
            if os.path.exists(candidate):
                real_path = candidate
                break
    if real_path:
        st.image(real_path, **kwargs)
    else:
        st.info(f"🖼️ ضعي الصورة هنا: {base_path}")


def risk_chart(labels, values_text, title, key, colors=None):
    colors = colors or RISK_COLORS
    fig = go.Figure()
    for i, (lbl, val) in enumerate(zip(labels, values_text)):
        fig.add_trace(go.Bar(
            y=[title], x=[1],
            orientation="h",
            marker_color=colors[i],
            name=lbl,
            text=f"{lbl}<br>{val}",
            textposition="inside",
            insidetextanchor="middle",
            hoverinfo="text",
            showlegend=False,
        ))
    fig.update_layout(
        barmode="stack",
        height=110,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    st.plotly_chart(fig, use_container_width=True, key=key)


def scale_colors(values):
    vmax = max(values) if max(values) > 0 else 1
    colors = []
    for v in values:
        if v == 0:
            colors.append(NO_DATA_COLOR)
        else:
            ratio = v / vmax
            if ratio <= 0.2:
                colors.append(RISK_COLORS[0])
            elif ratio <= 0.4:
                colors.append(RISK_COLORS[1])
            elif ratio <= 0.6:
                colors.append(RISK_COLORS[2])
            elif ratio <= 0.8:
                colors.append(RISK_COLORS[3])
            else:
                colors.append(RISK_COLORS[4])
    return colors


def severity_colors(values):
    mapping = {0: NO_DATA_COLOR, 1: RISK_COLORS[0], 2: RISK_COLORS[2], 3: RISK_COLORS[4]}
    return [mapping.get(v, NO_DATA_COLOR) for v in values]


def year_bar_chart(values, title, y_title, key, hover_notes=None, is_severity=False):
    hover = hover_notes or [""] * len(YEARS)
    colors = severity_colors(values) if is_severity else scale_colors(values)

    fig = go.Figure(go.Bar(
        x=[str(y) for y in YEARS],
        y=values,
        marker_color=colors,
        text=[f"{v}" if v else "" for v in values],
        textposition="outside",
        customdata=hover,
        hovertemplate="%{x}: %{y}<br>%{customdata}<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=15)),
        yaxis_title=y_title,
        height=340,
        margin=dict(l=10, r=10, t=50, b=10),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    st.plotly_chart(fig, use_container_width=True, key=key)


def color_legend(C):
    items = [
        (NO_DATA_COLOR, C["legend_no_data"]),
        (RISK_COLORS[0], C["legend_low"]),
        (RISK_COLORS[2], C["legend_mod"]),
        (RISK_COLORS[4], C["legend_high"]),
    ]
    html = "".join([
        f"<span style='display:inline-flex; align-items:center; margin:4px 10px; font-size:12.5px;'>"
        f"<span style='width:12px; height:12px; background:{c}; border-radius:3px; margin-left:6px; display:inline-block;'></span>{lbl}</span>"
        for c, lbl in items
    ])
    st.markdown(f"<div style='text-align:center; margin-bottom:6px;'>{html}</div>", unsafe_allow_html=True)


def impact_section(key, image_path, title, text, tags, accent,
                    global_values, global_ytitle, global_note, global_hover,
                    tn_values, tn_ytitle, tn_note, tn_hover, C, is_severity=False):
    with st.container(key=key):
        col_img, col_txt = st.columns([1.4, 1])
        with col_img:
            safe_image(image_path, use_container_width=True)
        with col_txt:
            st.markdown(f"<h3 style='color:{accent}; margin-top:0;'>{title}</h3>", unsafe_allow_html=True)
            st.write(text)

        tags_html = "".join([
            f"<span style='display:inline-block; background:{accent}22; color:{accent}; "
            f"border:1px solid {accent}; padding:6px 14px; border-radius:20px; "
            f"margin:4px; font-size:13px; font-weight:600;'>{t}</span>"
            for t in tags
        ])
        st.markdown(f"<div style='margin:10px 0 6px 0; text-align:center;'>{tags_html}</div>", unsafe_allow_html=True)

        color_legend(C)

        c1, c2 = st.columns(2)
        with c1:
            year_bar_chart(global_values, C["global_title"], global_ytitle, f"{key}_global", global_hover, is_severity)
            st.caption(global_note)
        with c2:
            year_bar_chart(tn_values, C["tn_title"], tn_ytitle, f"{key}_tn", tn_hover, is_severity)
            st.caption(tn_note)


def show(lang):
    T = TEXTS[lang]
    C = CHART_TXT.get(lang, CHART_TXT["ar"])

    # ---------- 1) مفهوم الفيضان ----------
    with st.container(key="card_main"):
        st.title(T["tab1_title"])
        st.write(T["tab1_intro"])
        st.caption(T["tab1_video_caption"])
        st.video("https://youtu.be/9hQZCiZ21fk?si=phRjw9MTnzEiIlmr")

    st.write("")

    # ---------- 2) أنواع الفيضانات ----------
    with st.container(key="card_types"):
        st.header(T["types_title"])
        st.caption(T["types_subtitle"])

        types_data = [
            ("type1_name", "type1_text", "assets/images/fig1_crue_fluviale.png"),
            ("type2_name", "type2_text", "assets/images/fig2_crue_eclair.png"),
            ("type3_name", "type3_text", "assets/images/fig3_ruissellement.png"),
            ("type4_name", "type4_text", "assets/images/fig4_nappe_phreatique.png"),
            ("type5_name", "type5_text", "assets/images/fig5_submersion_marine.png"),
        ]

        for i, (name_key, text_key, img_path) in enumerate(types_data):
            col_a, col_b = st.columns([1, 1])
            if i % 2 == 0:
                img_col, txt_col = col_a, col_b
            else:
                img_col, txt_col = col_b, col_a
            with img_col:
                safe_image(img_path, use_container_width=True)
            with txt_col:
                st.subheader(T[name_key])
                st.write(T[text_key])
            st.divider()

    st.write("")

    # ---------- 3) العناصر المسببة ----------
    with st.container(key="card_causes"):
        st.header(T["causes_title"])
        st.caption(T["causes_subtitle"])

        levels = [T["risk_very_low"], T["risk_low"], T["risk_moderate"], T["risk_high"], T["risk_very_high"]]
        levels_rev = list(reversed(levels))
        colors_rev = list(reversed(RISK_COLORS))
        ct = C["cause_chart_titles"]

        st.subheader(T["cause1_title"])
        st.write(T["cause1_explain"])
        risk_chart(levels, ["< 2 mm/h", "2-10 mm/h", "10-30 mm/h", "30-50 mm/h", "> 50 mm/h"], ct[0], "chart_precip")

        st.subheader(T["cause2_title"])
        st.write(T["cause2_explain"])
        risk_chart(levels_rev, ["0-2°", "2-6.5°", "6.5-14°", "14-25°", "> 25°"], ct[1], "chart_slope", colors=colors_rev)

        st.subheader(T["cause3_title"])
        st.write(T["cause3_explain"])
        risk_chart(levels, C["soil_labels"], ct[2], "chart_soil")

        st.subheader(T["cause4_title"])
        st.write(T["cause4_explain"])
        risk_chart(levels, ["< 0.5 km/km²", "0.5-1.5", "1.5-3", "3-4.5", "> 4.5"], ct[3], "chart_drainage")

        st.subheader(T["cause5_title"])
        st.write(T["cause5_explain"])
        risk_chart(levels, C["geo_labels"], ct[4], "chart_geo")

    st.write("")

    # ---------- 4) النتائج ----------
    with st.container(key="card_results"):
        st.header(T["results_title"])
        st.caption(T["results_subtitle"])

        econ_global = [30, 0, 3.7, 10.8, 32, 54, 30, 10, 0, 380, 0]
        econ_tn = [2, 0, 3, 1, 2, 2, 0, 1, 2, 0, 3]
        impact_section(
            key="impact_econ",
            image_path="assets/images/impact_economic.jpg",
            title=T["result_econ_title"],
            text=T["result_econ_text"],
            tags=[T["result_econ_direct"], T["result_econ_indirect"]],
            accent="#E8794A",
            global_values=econ_global, global_ytitle=C["econ_global_y"], global_hover=C["econ_global_hover"],
            global_note=C["econ_global_note"],
            tn_values=econ_tn, tn_ytitle=C["econ_tn_y"], tn_hover=C["econ_tn_hover"],
            tn_note=C["econ_tn_note"],
            C=C, is_severity=False,
        )
        st.divider()

        social_global = [300, 1200, 0, 0, 0, 200, 1700, 4000, 50, 0, 0]
        social_tn = [2, 0, 6, 0, 6, 0, 0, 0, 0, 0, 6]
        impact_section(
            key="impact_social",
            image_path="assets/images/impact_social.jpg",
            title=T["result_social_title"],
            text=T["result_social_text"],
            tags=[T["result_social_c1"], T["result_social_c2"], T["result_social_c3"], T["result_social_c4"]],
            accent="#16414A",
            global_values=social_global, global_ytitle=C["social_global_y"], global_hover=C["social_global_hover"],
            global_note=C["social_global_note"],
            tn_values=social_tn, tn_ytitle=C["social_tn_y"], tn_hover=C["social_tn_hover"],
            tn_note=C["social_tn_note"],
            C=C, is_severity=False,
        )
        st.divider()

        env_global = [2, 2, 3, 3, 2, 3, 3, 3, 2, 2, 2]
        env_tn = [1, 0, 3, 1, 2, 1, 0, 0, 1, 2, 3]
        impact_section(
            key="impact_env",
            image_path="assets/images/impact_environmental.jpg",
            title=T["result_env_title"],
            text=T["result_env_text"],
            tags=[T["result_env_c1"], T["result_env_c2"], T["result_env_c3"]],
            accent="#40916C",
            global_values=env_global, global_ytitle=C["env_y"], global_hover=C["env_global_hover"],
            global_note=C["env_global_note"],
            tn_values=env_tn, tn_ytitle=C["env_y"], tn_hover=C["env_tn_hover"],
            tn_note=C["env_tn_note"],
            C=C, is_severity=True,
        )