import streamlit as st
from languages import TEXTS

PAGE_TXT = {
    "ar": {
        "intro": "هذه الصفحة تجمع كل مصادر البيانات والمنهجية العلمية المعتمدة ببناء هذه اللوحة، بالإضافة لمحدوديات الدراسة الحالية وآفاقها المستقبلية، حرصًا على الشفافية والأمانة العلمية.",
        "sources_header": "📚 مصادر البيانات حسب كل تبويبة",
        "biblio_header": "📖 قائمة المراجع العلمية",
    },
    "fr": {
        "intro": "Cette page rassemble toutes les sources de données et la méthodologie scientifique adoptées dans la construction de ce tableau de bord, ainsi que les limites de l'étude actuelle et ses perspectives futures, dans un souci de transparence et de rigueur scientifique.",
        "sources_header": "📚 Sources de données par onglet",
        "biblio_header": "📖 Bibliographie scientifique",
    },
    "en": {
        "intro": "This page brings together all the data sources and scientific methodology used to build this dashboard, along with the current study's limitations and future prospects, in the interest of transparency and scientific integrity.",
        "sources_header": "📚 Data Sources by Tab",
        "biblio_header": "📖 Scientific Bibliography",
    },
}

DATA_SOURCES = {
    "ar": [
        {"tab": "1️⃣ مفهوم الفيضانات وأنواعها", "items": [
            "تعريف الفيضانات وتصنيفها الخماسي: مبني على أدبيات علمية دولية (Tehrany et al., 2014؛ Directive 2007/60/CE للاتحاد الأوروبي؛ Danso, 2026؛ Rahman et al., 2026؛ Shams et al., 2026؛ Dehimi et al., 2026؛ Jayawardane et al., 2026؛ Baccari et al., 2020).",
            "الرسوم التوضيحية الخمسة لأنواع الفيضانات: مقتبسة ومُعدّلة عن منصة Agora التابعة لجامعة UQAR الكندية.",
            "بيانات الخسائر العالمية والتونسية (2016-2026): تجميع أصلي من مصادر متعددة (تقارير إعلامية، بيانات مؤسساتية) لكل سنة على حدة.",
        ]},
        {"tab": "2️⃣ منطقة بوسالم", "items": [
            "البيانات المناخية (أمطار وحرارة): NASA POWER، متوسطات 2001-2020.",
            "الخريطة الجيولوجية: رقمنة عن خريطة المكتب الوطني للمناجم (ONM) التونسي.",
            "خرائط الشبكة الهيدروغرافية والغطاء الأرضي: رقمنة ومعالجة شخصية عبر QGIS، بالاعتماد على بيانات Esri/Sentinel-2 Land Cover وOpenStreetMap.",
            "فيضان جانفي 2003: الاتحاد الدولي لجمعيات الصليب الأحمر (IFRC، 2003).",
            "فيضان فيفري 2015: FloodList (2015)، مؤكَّد بدراسة Khemiri et al. (2024).",
        ]},
        {"tab": "3️⃣ توقعات الطقس  4️⃣ خرائط الخطر", "items": [
            "بيانات الأمطار والطقس الحية: واجهة برمجية مجانية من Open-Meteo (بدون مفتاح تسجيل)، محدّثة تلقائيًا.",
            "الخريطة الأساسية التفاعلية: OpenStreetMap (خريطة الشوارع)، وEsri World Imagery (صور الأقمار الصناعية) كطبقة بديلة.",
            "خرائط الخطر الجغرافية الأربعة (GeoJSON): بناء ذاتي عبر QGIS، بتصنيف خماسي (من ضعيف جدًا إلى مرتفع جدًا) لكل سيناريو مطري.",
            "جداول المؤسسات والمناطق المهددة (صحة، تعليم، سكن، شبكات، طرقات): تصنيف أصلي بالاعتماد على مواقع OpenStreetMap ومطابقتها بخرائط الخطر الأربعة.",
        ]},
    ],
    "fr": [
        {"tab": "1️⃣ Concept et types d'inondations", "items": [
            "Définition des inondations et classification en 5 types : basée sur la littérature scientifique internationale (Tehrany et al., 2014 ; Directive 2007/60/CE de l'UE ; Danso, 2026 ; Rahman et al., 2026 ; Shams et al., 2026 ; Dehimi et al., 2026 ; Jayawardane et al., 2026 ; Baccari et al., 2020).",
            "Les cinq schémas illustrant les types d'inondations : adaptés de la plateforme Agora de l'Université UQAR (Canada).",
            "Données de pertes mondiales et tunisiennes (2016-2026) : compilation originale à partir de sources multiples (rapports médiatiques, données institutionnelles) pour chaque année.",
        ]},
        {"tab": "2️⃣ Région de Bousalem", "items": [
            "Données climatiques (pluie et température) : NASA POWER, moyennes 2001-2020.",
            "Carte géologique : numérisée à partir de la carte de l'Office National des Mines (ONM) de Tunisie.",
            "Cartes du réseau hydrographique et de l'occupation du sol : numérisation et traitement personnels via QGIS, à partir des données Esri/Sentinel-2 Land Cover et OpenStreetMap.",
            "Inondation de janvier 2003 : Fédération Internationale des Sociétés de la Croix-Rouge (IFRC, 2003).",
            "Inondation de février 2015 : FloodList (2015), corroborée par l'étude Khemiri et al. (2024).",
        ]},
        {"tab": "3️⃣ Prévisions météo  4️⃣ Cartes de risque", "items": [
            "Données météo et pluviométriques en direct : API gratuite Open-Meteo (sans clé requise), mise à jour automatique.",
            "Fond de carte interactif : OpenStreetMap (carte des rues), et Esri World Imagery (imagerie satellite) comme couche alternative.",
            "Les quatre cartes de risque géographiques (GeoJSON) : construites personnellement via QGIS, avec une classification en 5 niveaux (de très faible à très élevé) pour chaque scénario pluviométrique.",
            "Tableaux des établissements et zones menacées (santé, éducation, logement, réseaux, routes) : classification originale basée sur les emplacements OpenStreetMap croisés avec les quatre cartes de risque.",
        ]},
    ],
    "en": [
        {"tab": "1️⃣ Flood Concept and Types", "items": [
            "Flood definition and five-tier classification: based on international scientific literature (Tehrany et al., 2014; EU Directive 2007/60/EC; Danso, 2026; Rahman et al., 2026; Shams et al., 2026; Dehimi et al., 2026; Jayawardane et al., 2026; Baccari et al., 2020).",
            "The five illustrative diagrams of flood types: adapted from the Agora platform of UQAR University (Canada).",
            "Global and Tunisian loss data (2016-2026): original compilation from multiple sources (media reports, institutional data) for each year.",
        ]},
        {"tab": "2️⃣ Bousalem Region", "items": [
            "Climate data (rainfall and temperature): NASA POWER, 2001-2020 averages.",
            "Geological map: digitized from the map of Tunisia's National Office of Mines (ONM).",
            "Hydrographic network and land cover maps: personal digitization and processing via QGIS, based on Esri/Sentinel-2 Land Cover and OpenStreetMap data.",
            "January 2003 flood: International Federation of Red Cross and Red Crescent Societies (IFRC, 2003).",
            "February 2015 flood: FloodList (2015), corroborated by the Khemiri et al. (2024) study.",
        ]},
        {"tab": "3️⃣ Weather Forecast  4️⃣ Risk Maps", "items": [
            "Live rainfall and weather data: free Open-Meteo API (no registration key), automatically updated.",
            "Interactive base map: OpenStreetMap (street map), and Esri World Imagery (satellite imagery) as an alternative layer.",
            "The four geographic risk maps (GeoJSON): personally built via QGIS, with a five-tier classification (from very low to very high) for each rainfall scenario.",
            "Threatened facilities and zones tables (health, education, housing, networks, roads): original classification based on OpenStreetMap locations cross-referenced with the four risk maps.",
        ]},
    ],
}

METHODOLOGY = {
    "ar": {
        "title": "🧭 المنهجية المتّبعة",
        "paragraphs": [
            "**تصنيف سيناريوهات الأمطار (4 مستويات):** اعتمدنا عتبات 20، 40، 70، و100 ملم/24 ساعة، بالاستناد إلى الأدبيات العلمية التي تشير إلى إن العتبة الحرجة لتجاوز قدرة التربة على الامتصاص تتراوح عمومًا بين 10 و50 ملم/ساعة حسب طبيعة التربة والانحدار وحالة الرطوبة المسبقة (Jayawardane et al., 2026).",
            "**بناء خرائط الخطر (5 درجات):** لكل سيناريو مطري، أُنتجت خريطة خطر مستقلة عبر QGIS، بتصنيف خماسي (ضعيف جدًا → مرتفع جدًا) يعكس تفاعل عوامل متعددة (الانحدار، نوع التربة، القرب من مجاري المياه، الغطاء الأرضي) المفصّلة بالتبويبة الأولى.",
            "**مؤشرات الشدة الوصفية (0-3):** في الحالات التي لا تتوفر فيها أرقام مالية أو إحصائية دقيقة بالمصدر (خصوصًا الخسائر الاقتصادية والبيئية ببعض السنوات)، استُخدم مؤشر وصفي تقديري (0=لا أثر، 3=كارثي) مبني على شدة الوصف النصي بالمصدر، وليس قياسًا رقميًا حقيقيًا — وهذا موضّح بوضوح أسفل كل رسم بياني معني بالموقع.",
        ],
    },
    "fr": {
        "title": "🧭 Méthodologie adoptée",
        "paragraphs": [
            "**Classification des scénarios pluviométriques (4 niveaux) :** nous avons retenu les seuils de 20, 40, 70 et 100 mm/24h, en nous appuyant sur la littérature scientifique indiquant que le seuil critique de dépassement de la capacité d'absorption du sol se situe généralement entre 10 et 50 mm/h selon la nature du sol, la pente et l'humidité antécédente (Jayawardane et al., 2026).",
            "**Construction des cartes de risque (5 niveaux) :** pour chaque scénario pluviométrique, une carte de risque distincte a été produite via QGIS, avec une classification en 5 niveaux (très faible → très élevé) reflétant l'interaction de plusieurs facteurs (pente, type de sol, proximité des cours d'eau, occupation du sol) détaillés dans le premier onglet.",
            "**Indices de sévérité descriptifs (0-3) :** lorsque des chiffres financiers ou statistiques précis n'étaient pas disponibles dans la source (notamment certaines pertes économiques et environnementales pour certaines années), un indice descriptif estimatif (0=aucun impact, 3=catastrophique) a été utilisé, basé sur l'intensité de la description textuelle de la source, et non sur une mesure numérique réelle — ceci est clairement indiqué sous chaque graphique concerné du site.",
        ],
    },
    "en": {
        "title": "🧭 Methodology Used",
        "paragraphs": [
            "**Rainfall scenario classification (4 levels):** We adopted thresholds of 20, 40, 70, and 100 mm/24h, based on scientific literature indicating that the critical threshold for exceeding soil absorption capacity generally ranges between 10 and 50 mm/h depending on soil type, slope, and antecedent moisture conditions (Jayawardane et al., 2026).",
            "**Building the risk maps (5 levels):** For each rainfall scenario, a distinct risk map was produced via QGIS, with a five-tier classification (very low → very high) reflecting the interaction of multiple factors (slope, soil type, proximity to watercourses, land cover) detailed in the first tab.",
            "**Descriptive severity indices (0-3):** In cases where precise financial or statistical figures were not available in the source (particularly certain economic and environmental losses for some years), an estimated descriptive index (0=no impact, 3=catastrophic) was used, based on the intensity of the source's textual description rather than an actual numerical measurement — this is clearly indicated below every relevant chart on the site.",
        ],
    },
}

LIMITATIONS = {
    "ar": {
        "title": "⚠️ محدوديات الدراسة والآفاق المستقبلية",
        "items": [
            "**تصريف السدود:** النموذج الحالي يعتمد على كمية الأمطار المحلية فقط (عبر Open-Meteo)، ولا يملك بيانات حية عن تصريف السدود الثلاثة المؤثرة بالمنطقة (كسّاب، بوهرتمة، ملاق)، رغم أن فيضان جانفي 2003 أثبت أن تصريف سد ملاق فاقم الخطر بشكل ملحوظ. أُضيفت خانة تصحيح يدوي اختيارية بداشبورد الخرائط لمحاكاة هذا الأثر جزئيًا، بانتظار توفر واجهة برمجية عامة لبيانات السدود مستقبلًا.",
            "**عدم التحقق التاريخي الكمي (Backtesting):** لم يُجرَ اختبار رجعي يقارن مباشرة بين توقعات النموذج وكمية الأمطار الفعلية المسجّلة أثناء فيضاني 2003 و2015، لعدم توفر بيانات رصد مطري بدقة يومية لتلك الفترات بمحطة قريبة من بوسالم تحديدًا.",
            "**عدم وجود نظام تنبيه فعلي (Push/SMS):** الموقع أداة استعلام سلبية (يحتاج الزائر لفتحها بنفسه)، وليس نظام إنذار فعّال يرسل تنبيهات مباشرة للسكان المهددين، وهو تطوير مستقبلي يتطلب خدمة رسائل مدفوعة وربطًا مؤسساتيًا رسميًا.",
            "**دقة إحداثيات بعض المرافق:** تتفاوت دقة تموضع بعض المنشآت (خصوصًا بجداول التقارير) بين High/Medium/Low حسب توفر بيانات OpenStreetMap لكل موقع بعينه.",
        ],
    },
    "fr": {
        "title": "⚠️ Limites de l'étude et perspectives futures",
        "items": [
            "**Lâchers de barrages :** le modèle actuel repose uniquement sur la quantité de pluie locale (via Open-Meteo), et ne dispose pas de données en direct sur les lâchers des trois barrages influents de la région (Kasseb, Bou Hertma, Mellègue), bien que l'inondation de janvier 2003 ait démontré que les lâchers du barrage Mellègue avaient significativement aggravé le risque. Une case de correction manuelle optionnelle a été ajoutée au tableau de bord des cartes pour simuler partiellement cet effet, en attendant la disponibilité future d'une API publique pour les données des barrages.",
            "**Absence de validation historique quantitative (Backtesting) :** aucun test rétrospectif comparant directement les prévisions du modèle aux quantités de pluie réellement enregistrées lors des inondations de 2003 et 2015 n'a été réalisé, faute de données pluviométriques journalières précises disponibles pour ces périodes à une station proche de Bousalem.",
            "**Absence de système d'alerte actif (Push/SMS) :** le site est un outil de consultation passif (l'utilisateur doit l'ouvrir lui-même), et non un système d'alerte actif envoyant des notifications directes aux populations menacées ; il s'agit d'un développement futur nécessitant un service de messagerie payant et un partenariat institutionnel officiel.",
            "**Précision des coordonnées de certains équipements :** la précision de localisation de certaines installations (notamment dans les tableaux de rapport) varie entre High/Medium/Low selon la disponibilité des données OpenStreetMap pour chaque site.",
        ],
    },
    "en": {
        "title": "⚠️ Study Limitations and Future Prospects",
        "items": [
            "**Dam releases:** the current model relies solely on local rainfall data (via Open-Meteo), and has no live data on releases from the three influential dams in the region (Kasseb, Bou Hertma, Mellègue), even though the January 2003 flood demonstrated that Mellègue Dam releases significantly worsened the risk. An optional manual correction checkbox was added to the risk maps dashboard to partially simulate this effect, pending the future availability of a public API for dam data.",
            "**No quantitative historical validation (Backtesting):** no retrospective test directly comparing the model's predictions to the actual rainfall recorded during the 2003 and 2015 floods was conducted, due to the lack of precise daily rainfall monitoring data for those periods at a station near Bousalem specifically.",
            "**No active warning system (Push/SMS):** the site is a passive query tool (the visitor must open it themselves), not an active warning system sending direct notifications to threatened populations; this is a future development requiring a paid messaging service and an official institutional partnership.",
            "**Coordinate accuracy for some facilities:** the location accuracy of certain facilities (especially in the report tables) varies between High/Medium/Low depending on the availability of OpenStreetMap data for each specific site.",
        ],
    },
}

REFERENCES = [
    "Baccari, N. et al. (2020).",
    "Danso, A. (2026).",
    "Dehimi, S. et al. (2026).",
    "Directive 2007/60/CE du Parlement Européen et du Conseil relative à l'évaluation et à la gestion des risques d'inondation.",
    "Jayawardane, K. et al. (2026).",
    "Khemiri, R. et al. (2024).",
    "NRCS – Natural Resources Conservation Service (2009). National Engineering Handbook, Table 7-1, Hydrologic Soil Groups.",
    "Rahman, M. et al. (2026).",
    "Shams, A. et al. (2026).",
    "Tehrany, M. S. et al. (2014).",
    "Fédération Internationale des Sociétés de la Croix-Rouge et du Croissant-Rouge (IFRC) (2003).",
    "FloodList (2015).",
    "NASA POWER Project – Prediction Of Worldwide Energy Resources.",
    "Open-Meteo API (open-meteo.com).",
    "Office National des Mines de Tunisie (ONM) – Carte géologique de la Tunisie.",
    "OpenStreetMap Contributors.",
    "Esri – World Imagery Basemap.",
]


def show(lang):
    T = TEXTS[lang]
    P = PAGE_TXT.get(lang, PAGE_TXT["ar"])
    sources = DATA_SOURCES.get(lang, DATA_SOURCES["ar"])
    method = METHODOLOGY.get(lang, METHODOLOGY["ar"])
    limits = LIMITATIONS.get(lang, LIMITATIONS["ar"])

    with st.container(key="card_ref_intro"):
        st.title(T["nav_tab6"])
        st.write(P["intro"])

    st.write("")

    with st.container(key="card_ref_sources"):
        st.header(P["sources_header"])
        for section in sources:
            st.subheader(section["tab"])
            for item in section["items"]:
                st.markdown(f"- {item}")
            st.write("")

    st.write("")

    with st.container(key="card_ref_method"):
        st.header(method["title"])
        for p in method["paragraphs"]:
            st.markdown(p)

    st.write("")

    with st.container(key="card_ref_limits"):
        st.header(limits["title"])
        for item in limits["items"]:
            st.markdown(f"- {item}")

    st.write("")

    with st.container(key="card_ref_biblio"):
        st.header(P["biblio_header"])
        for ref in REFERENCES:
            st.markdown(f"- {ref}")