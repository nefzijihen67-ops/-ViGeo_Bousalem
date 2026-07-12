import streamlit as st
from languages import TEXTS

CITIZEN = "#2874A6"
MUNICIPALITY = "#7D3C98"
CIVIL_PROTECTION = "#C0392B"

PHASE_LABELS = {
    "ar": {"before": "🛡️ قبل", "during": "⚠️ أثناء", "after": "🔧 بعد"},
    "fr": {"before": "🛡️ Avant", "during": "⚠️ Pendant", "after": "🔧 Après"},
    "en": {"before": "🛡️ Before", "during": "⚠️ During", "after": "🔧 After"},
}

MATRIX = {
    "ar": {
        "citizen": {"title": "👤 المواطن", "color": CITIZEN, "phases": {
            "before": [
                ("🎒", "تجهيز حقيبة طوارئ: ماء، أدوية، مصباح يدوي وبطاريات، وثائق مهمة في كيس مقاوم للماء، شاحن هاتف احتياطي."),
                ("🔼", "رفع الأجهزة الكهربائية والأثاث القيّم عن الأرض إذا كان السكن في منطقة منخفضة."),
                ("🗺️", "معرفة أقرب مركز إيواء ومسار الإخلاء مسبقًا."),
                ("🧹", "تنظيف الأخاديد والمزاريب أمام المنزل لتفادي انسداد مجاري الصرف."),
                ("📲", "الانضمام لمجموعة تواصل مع الجيران للإنذار السريع المحلي."),
                ("🛌", "تجنب التخزين أو النوم في الطابق الأرضي في المناطق المعرضة للخطر."),
            ],
            "during": [
                ("⛔", "عدم عبور الوديان أو الجسور الغارقة سيرًا أو بالسيارة مهما بدا الأمر آمنًا."),
                ("🔌", "قطع التيار الكهربائي الرئيسي بالمنزل فور دخول الماء."),
                ("🏠", "الانتقال فورًا لطابق أعلى أو نقطة مرتفعة والاتصال بالحماية المدنية إذا تعذّر الخروج."),
                ("📢", "اتباع تعليمات الإخلاء الرسمية فورًا دون تأخير أو محاولة إنقاذ الممتلكات أولًا."),
                ("⚡", "الابتعاد عن أعمدة الكهرباء وخطوطها الساقطة."),
            ],
            "after": [
                ("🚧", "عدم العودة للمنزل إلا بعد تصريح رسمي بأن المبنى آمن هيكليًا."),
                ("🔧", "فحص التمديدات الكهربائية والغازية من طرف مختص قبل إعادة التشغيل."),
                ("📸", "توثيق الأضرار بالصور لتقديم ملف تعويض."),
                ("🧼", "تنظيف وتعقيم المنزل جيدًا لأن مياه الفيضان غالبًا ملوثة."),
                ("🦟", "الانتباه للمخاطر الصحية بعد الفيضان (أمراض منقولة بالمياه، لدغات حشرات وزواحف)."),
            ],
        }},
        "municipality": {"title": "🏢 الدولة والبلدية", "color": MUNICIPALITY, "phases": {
            "before": [
                ("🚰", "صيانة دورية لمجاري التصريف قبل موسم الأمطار."),
                ("🗺️", "توزيع خريطة مناطق الخطر رسميًا على السكان."),
                ("🏃", "تنظيم تمارين إخلاء سنوية للأحياء المهددة بالتنسيق مع الحماية المدنية."),
                ("🏫", "تجهيز مراكز إيواء دائمة بمخزون بطانيات ومواد غذائية."),
                ("🏗️", "متابعة مشاريع الحماية الهيكلية (سدود، جدران وقائية) والضغط لتسريع إنجازها."),
            ],
            "during": [
                ("🎛️", "تفعيل غرفة أزمة محلية بحضور دائم لمسؤول الحماية المدنية."),
                ("📢", "إصدار بلاغات تحذير فورية ومحدّثة تحدد الأحياء المهددة بالاسم."),
                ("🚧", "قطع الطرقات والجسور الخطرة ونشر حواجز وإشارات تحذير."),
                ("🏫", "فتح مراكز الإيواء فورًا واستقبال العائلات."),
            ],
            "after": [
                ("💰", "تقييم سريع للأضرار وفتح ملفات التعويض."),
                ("🛠️", "إصلاح عاجل للبنية التحتية الحيوية (كهرباء، ماء صالح للشرب، طرقات)."),
                ("🧴", "تنظيم حملات تعقيم ومكافحة الأوبئة في المناطق المتضررة."),
                ("📋", "مراجعة الأداء لتحديث خطة الوقاية للموسم القادم."),
            ],
        }},
        "civil_protection": {"title": "🚨 الحماية المدنية", "color": CIVIL_PROTECTION, "phases": {
            "before": [
                ("👁️", "تشكيل فرق يقظة ميدانية عند بداية موسم الأمطار لمراقبة النقاط الحساسة."),
                ("🚤", "التأكد الدوري من جاهزية معدات الإنقاذ (زوارق، حبال، سترات نجاة)."),
                ("🤝", "التنسيق المسبق مع الجيش والسلطات المحلية لخطة إخلاء موحّدة."),
                ("♿", "تحديد الأسر الأكثر هشاشة (مسنون، ذوو إعاقة) لإعطائها أولوية إخلاء عند الحاجة."),
            ],
            "during": [
                ("🚑", "تنفيذ عمليات إجلاء ميدانية مباشرة للأحياء المهددة."),
                ("🚁", "استعمال الزوارق (وعند الحاجة المروحيات) للوصول للمناطق المعزولة."),
                ("📊", "تحديث منسوب المياه ميدانيًا بشكل مستمر."),
                ("📍", "إعطاء الأولوية للمناطق منخفضة المنسوب المعروفة مسبقًا بالخطورة."),
            ],
            "after": [
                ("🔍", "إجراء عمليات بحث نهائية للتأكد من عدم وجود مفقودين."),
                ("❤️‍🩹", "تقديم دعم إسعافي أولي ونفسي للمتضررين."),
                ("📄", "إعطاء تقرير رسمي عن سير العملية لتحسين زمن الاستجابة مستقبلاً."),
            ],
        }},
    },
    "fr": {
        "citizen": {"title": "👤 Le citoyen", "color": CITIZEN, "phases": {
            "before": [
                ("🎒", "Préparer un sac d'urgence : eau, médicaments, lampe torche et piles, documents importants dans un sac étanche, chargeur de téléphone de secours."),
                ("🔼", "Surélever les appareils électriques et les meubles de valeur si le logement est en zone basse."),
                ("🗺️", "Connaître à l'avance le centre d'hébergement le plus proche et l'itinéraire d'évacuation."),
                ("🧹", "Nettoyer les caniveaux et gouttières devant la maison pour éviter l'obstruction des égouts."),
                ("📲", "Rejoindre un groupe de communication avec les voisins pour une alerte rapide locale."),
                ("🛌", "Éviter de stocker des biens ou de dormir au rez-de-chaussée dans les zones à risque."),
            ],
            "during": [
                ("⛔", "Ne jamais traverser un oued ou un pont submergé, à pied ou en voiture, même si cela semble sûr."),
                ("🔌", "Couper le courant électrique principal dès que l'eau pénètre dans la maison."),
                ("🏠", "Monter immédiatement à un étage supérieur ou un point élevé et appeler la protection civile si la sortie est impossible."),
                ("📢", "Suivre immédiatement les consignes officielles d'évacuation, sans délai ni tentative de sauver des biens."),
                ("⚡", "S'éloigner des poteaux électriques et des câbles tombés."),
            ],
            "after": [
                ("🚧", "Ne pas rentrer chez soi avant une autorisation officielle confirmant que le bâtiment est sûr."),
                ("🔧", "Faire vérifier les installations électriques et de gaz par un professionnel avant de les remettre en service."),
                ("📸", "Documenter les dégâts en photos pour le dossier d'indemnisation."),
                ("🧼", "Bien nettoyer et désinfecter la maison, car l'eau de crue est souvent contaminée."),
                ("🦟", "Faire attention aux risques sanitaires après l'inondation (maladies hydriques, piqûres d'insectes)."),
            ],
        }},
        "municipality": {"title": "🏢 L'État et la municipalité", "color": MUNICIPALITY, "phases": {
            "before": [
                ("🚰", "Entretien régulier des canaux de drainage avant la saison des pluies."),
                ("🗺️", "Distribuer officiellement la carte des zones à risque aux habitants."),
                ("🏃", "Organiser des exercices d'évacuation annuels pour les quartiers menacés avec la protection civile."),
                ("🏫", "Équiper des centres d'hébergement permanents avec des stocks de couvertures et de vivres."),
                ("🏗️", "Suivre les projets de protection structurelle (barrages, murs) et accélérer leur réalisation."),
            ],
            "during": [
                ("🎛️", "Activer une cellule de crise locale avec présence permanente du responsable de la protection civile."),
                ("📢", "Émettre des alertes immédiates et actualisées désignant nommément les quartiers menacés."),
                ("🚧", "Fermer les routes et ponts dangereux et installer des barrières et panneaux d'avertissement."),
                ("🏫", "Ouvrir immédiatement les centres d'hébergement et accueillir les familles."),
            ],
            "after": [
                ("💰", "Évaluation rapide des dégâts et ouverture des dossiers d'indemnisation."),
                ("🛠️", "Réparation urgente des infrastructures vitales (électricité, eau potable, routes)."),
                ("🧴", "Organiser des campagnes de désinfection et de lutte contre les épidémies."),
                ("📋", "Réviser les performances pour mettre à jour le plan de prévention pour la saison prochaine."),
            ],
        }},
        "civil_protection": {"title": "🚨 La protection civile", "color": CIVIL_PROTECTION, "phases": {
            "before": [
                ("👁️", "Constituer des équipes de veille sur le terrain dès le début de la saison des pluies."),
                ("🚤", "Vérifier régulièrement la disponibilité du matériel de sauvetage (bateaux, cordes, gilets)."),
                ("🤝", "Coordination préalable avec l'armée et les autorités locales pour un plan d'évacuation unifié."),
                ("♿", "Identifier les familles les plus vulnérables (âgées, handicapées) pour leur priorité d'évacuation."),
            ],
            "during": [
                ("🚑", "Mener des opérations d'évacuation directes sur le terrain pour les quartiers menacés."),
                ("🚁", "Utiliser des bateaux (et hélicoptères si nécessaire) pour atteindre les zones isolées."),
                ("📊", "Mettre à jour en continu le niveau de l'eau sur le terrain."),
                ("📍", "Donner la priorité aux zones basses déjà connues comme à risque."),
            ],
            "after": [
                ("🔍", "Mener des opérations de recherche finales pour s'assurer qu'il n'y a pas de disparus."),
                ("❤️‍🩹", "Fournir un soutien de premiers secours et psychologique aux sinistrés."),
                ("📄", "Remettre un rapport officiel sur le déroulement de l'opération."),
            ],
        }},
    },
    "en": {
        "citizen": {"title": "👤 The Citizen", "color": CITIZEN, "phases": {
            "before": [
                ("🎒", "Prepare an emergency bag: water, medicine, flashlight and batteries, important documents in a waterproof bag, spare phone charger."),
                ("🔼", "Raise electrical appliances and valuable furniture off the ground if the home is in a low-lying area."),
                ("🗺️", "Know the nearest shelter and evacuation route in advance."),
                ("🧹", "Clean gutters and drains in front of the house to prevent sewer blockage."),
                ("📲", "Join a neighborhood communication group for rapid local alerts."),
                ("🛌", "Avoid storing belongings or sleeping on the ground floor in at-risk areas."),
            ],
            "during": [
                ("⛔", "Never cross a flooded wadi or bridge on foot or by car, no matter how safe it seems."),
                ("🔌", "Cut the main electrical power as soon as water enters the house."),
                ("🏠", "Move immediately to a higher floor or elevated point and call civil protection if unable to leave."),
                ("📢", "Follow official evacuation instructions immediately, without delay or trying to save belongings first."),
                ("⚡", "Stay away from power poles and fallen power lines."),
            ],
            "after": [
                ("🚧", "Do not return home until officially authorized that the building is structurally safe."),
                ("🔧", "Have electrical and gas systems checked by a professional before restarting them."),
                ("📸", "Document damage with photos for the compensation file."),
                ("🧼", "Thoroughly clean and disinfect the home, as floodwater is often contaminated."),
                ("🦟", "Watch for health risks after the flood (waterborne diseases, insect and reptile bites)."),
            ],
        }},
        "municipality": {"title": "🏢 The State and Municipality", "color": MUNICIPALITY, "phases": {
            "before": [
                ("🚰", "Regular maintenance of drainage channels before the rainy season."),
                ("🗺️", "Officially distribute the risk zone map to residents."),
                ("🏃", "Organize annual evacuation drills for threatened neighborhoods with civil protection."),
                ("🏫", "Equip permanent shelters with stocks of blankets and food supplies."),
                ("🏗️", "Follow up on structural protection projects (dams, protective walls) and push to speed completion."),
            ],
            "during": [
                ("🎛️", "Activate a local crisis room with permanent presence of the civil protection officer."),
                ("📢", "Issue immediate, updated warnings naming the specifically threatened neighborhoods."),
                ("🚧", "Close dangerous roads and bridges and deploy barriers and warning signs."),
                ("🏫", "Immediately open shelters and receive families."),
            ],
            "after": [
                ("💰", "Rapid damage assessment and opening of compensation files."),
                ("🛠️", "Urgent repair of vital infrastructure (electricity, drinking water, roads)."),
                ("🧴", "Organize disinfection and epidemic prevention campaigns in affected areas."),
                ("📋", "Review performance to update the prevention plan for the next season."),
            ],
        }},
        "civil_protection": {"title": "🚨 Civil Protection", "color": CIVIL_PROTECTION, "phases": {
            "before": [
                ("👁️", "Form field watch teams at the start of the rainy season to monitor sensitive points."),
                ("🚤", "Regularly verify the readiness of rescue equipment (boats, ropes, life jackets)."),
                ("🤝", "Prior coordination with the army and local authorities for a unified evacuation plan."),
                ("♿", "Identify the most vulnerable families (elderly, disabled) to give them evacuation priority."),
            ],
            "during": [
                ("🚑", "Conduct direct field evacuation operations for threatened neighborhoods."),
                ("🚁", "Use boats (and helicopters if needed) to reach isolated areas."),
                ("📊", "Continuously update water levels on the ground."),
                ("📍", "Prioritize low-lying areas already known to be at risk."),
            ],
            "after": [
                ("🔍", "Conduct final search operations to ensure no one is missing."),
                ("❤️‍🩹", "Provide first-aid and psychological support to victims."),
                ("📄", "Submit an official report on the operation to improve future response time."),
            ],
        }},
    },
}

BUDGET_TIPS = {
    "ar": [
        ("📱", "مجموعة تواصل رقمية بين الجيران", "تكلفة صفرية وفعالية عالية للإنذار السريع المحلي."),
        ("📏", "علامة قياس منسوب يدوية", "خط مرسوم على عمود قريب من مجرى المياه، بدل أجهزة استشعار مكلفة."),
        ("🛍️", "أكياس رمل محلية الصنع", "لحماية عتبات المنازل من دخول المياه بتكلفة رمزية."),
        ("🎒", "حقيبة طوارئ منزلية بسيطة", "بتكلفة زهيدة، تحتوي الأساسيات فقط دون مبالغة."),
        ("🤝", "تمرين إخلاء مجتمعي سنوي", "بالتعاون مع جمعيات الحي، بدون أي تكلفة تُذكر."),
        ("🏫", "استعمال المدارس كمراكز إيواء", "مع تخزين بطانيات ومواد إسعاف أولية فقط داخلها."),
    ],
    "fr": [
        ("📱", "Groupe de communication numérique entre voisins", "Coût nul et grande efficacité pour une alerte rapide locale."),
        ("📏", "Repère de niveau d'eau manuel", "Un trait tracé sur un poteau proche du cours d'eau, au lieu de capteurs coûteux."),
        ("🛍️", "Sacs de sable faits maison", "Pour protéger les seuils des maisons contre l'entrée de l'eau à coût symbolique."),
        ("🎒", "Sac d'urgence familial simple", "À faible coût, contenant seulement l'essentiel sans excès."),
        ("🤝", "Exercice d'évacuation communautaire annuel", "En partenariat avec les associations de quartier, sans aucun coût notable."),
        ("🏫", "Utilisation des écoles comme centres d'hébergement", "Avec un simple stock de couvertures et de matériel de premiers secours."),
    ],
    "en": [
        ("📱", "Digital neighbor communication group", "Zero cost and highly effective for rapid local alerts."),
        ("📏", "Manual water level marker", "A line drawn on a pole near the watercourse, instead of costly sensors."),
        ("🛍️", "Homemade sandbags", "To protect doorsteps from water entry at symbolic cost."),
        ("🎒", "Simple household emergency bag", "Low cost, containing only the essentials without excess."),
        ("🤝", "Annual community evacuation drill", "In partnership with neighborhood associations, at virtually no cost."),
        ("🏫", "Using schools as shelters", "With just a stock of blankets and first-aid supplies."),
    ],
}

PAGE_TXT = {
    "ar": {
        "subtitle": "دليل شامل للتصرف الصحيح قبل الفيضان وأثناءه وبعده، موزّع حسب الجهة المسؤولة.",
        "legend_title": "🗂️ دليل الألوان:",
        "legend_citizen": "المواطن", "legend_muni": "الدولة والبلدية", "legend_civil": "الحماية المدنية",
        "legend_phases": "🛡️ قبل &nbsp; ➡️ &nbsp; ⚠️ أثناء &nbsp; ➡️ &nbsp; 🔧 بعد",
        "budget_title": "💡 إجراءات وقائية بميزانية معقولة جدًا",
        "budget_caption": "حلول بسيطة وفعّالة لا تحتاج تجهيزات مكلفة",
    },
    "fr": {
        "subtitle": "Guide complet pour adopter la bonne conduite avant, pendant et après l'inondation, réparti selon la partie responsable.",
        "legend_title": "🗂️ Légende des couleurs :",
        "legend_citizen": "Citoyen", "legend_muni": "État et municipalité", "legend_civil": "Protection civile",
        "legend_phases": "🛡️ Avant &nbsp; ➡️ &nbsp; ⚠️ Pendant &nbsp; ➡️ &nbsp; 🔧 Après",
        "budget_title": "💡 Mesures préventives à budget très raisonnable",
        "budget_caption": "Des solutions simples et efficaces ne nécessitant pas d'équipements coûteux",
    },
    "en": {
        "subtitle": "A comprehensive guide to proper conduct before, during, and after a flood, organized by responsible party.",
        "legend_title": "🗂️ Color legend:",
        "legend_citizen": "Citizen", "legend_muni": "State and Municipality", "legend_civil": "Civil Protection",
        "legend_phases": "🛡️ Before &nbsp; ➡️ &nbsp; ⚠️ During &nbsp; ➡️ &nbsp; 🔧 After",
        "budget_title": "💡 Preventive Measures on a Very Reasonable Budget",
        "budget_caption": "Simple and effective solutions that don't require costly equipment",
    },
}

MATRIX_CSS = """
<style>
.action-card {
    display: flex; align-items: center; gap: 12px;
    background: white; border-radius: 12px; padding: 12px 14px;
    margin-bottom: 10px; box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    transition: all 0.22s ease; border-right: 3px solid transparent;
}
.action-card:hover {
    transform: translateX(-6px) scale(1.015);
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}
.icon-badge {
    min-width: 40px; height: 40px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 19px; flex-shrink: 0;
}
.action-text { font-size: 13.5px; line-height: 1.55; color: #2c2c2c; }
.budget-card {
    background: white; border: 1px solid #E5DFD0; border-radius: 12px;
    padding: 18px; text-align: center; transition: all 0.25s ease; height: 100%;
}
.budget-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 10px 24px rgba(22, 65, 74, 0.18);
    border-color: #2E7C86;
}
</style>
"""


def render_column(key, data, phase_labels):
    with st.container(key=f"card_matrix_{key}"):
        st.markdown(f"""
        <div style='background:linear-gradient(135deg, {data["color"]}22, {data["color"]}08);
                    border-radius:12px; padding:16px; margin-bottom:14px; text-align:center;
                    border:1px solid {data["color"]}33;'>
            <div style='font-size:20px; font-weight:800; color:{data["color"]};'>{data["title"]}</div>
        </div>
        """, unsafe_allow_html=True)

        tabs = st.tabs([phase_labels["before"], phase_labels["during"], phase_labels["after"]])
        for tab, phase_key in zip(tabs, ["before", "during", "after"]):
            with tab:
                for icon, text in data["phases"][phase_key]:
                    st.markdown(f"""
                    <div class="action-card" style="border-right-color:{data["color"]};">
                        <span class="icon-badge" style="background:{data["color"]}18;">{icon}</span>
                        <span class="action-text">{text}</span>
                    </div>
                    """, unsafe_allow_html=True)


def show(lang):
    T = TEXTS[lang]
    M = MATRIX.get(lang, MATRIX["ar"])
    BT = BUDGET_TIPS.get(lang, BUDGET_TIPS["ar"])
    P = PAGE_TXT.get(lang, PAGE_TXT["ar"])
    PL = PHASE_LABELS.get(lang, PHASE_LABELS["ar"])

    st.markdown(MATRIX_CSS, unsafe_allow_html=True)

    with st.container(key="card_guidelines_intro"):
        st.title(T["nav_tab5"])
        st.write(P["subtitle"])

    st.markdown(f"""
    <div style='background:#FDEDEC; border-right:5px solid #C0392B; border-radius:10px;
                padding:16px 20px; margin-top:14px;'>
        <div style='font-weight:800; color:#C0392B; font-size:15px;'>{T["disclaimer_title"]}</div>
        <div style='font-size:13.5px; color:#7B241C; margin-top:6px; line-height:1.6;'>{T["disclaimer_text"]}</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    with st.container(key="card_matrix_legend"):
        st.markdown(f"""
        <div style='display:flex; justify-content:center; flex-wrap:wrap; gap:22px; align-items:center;'>
            <span style='font-weight:700; color:#16414A;'>{P["legend_title"]}</span>
            <span style='display:flex; align-items:center; gap:6px;'>
                <span style='width:16px; height:16px; background:{CITIZEN}; border-radius:4px; display:inline-block;'></span>
                <span style='font-size:14px;'>{P["legend_citizen"]}</span>
            </span>
            <span style='display:flex; align-items:center; gap:6px;'>
                <span style='width:16px; height:16px; background:{MUNICIPALITY}; border-radius:4px; display:inline-block;'></span>
                <span style='font-size:14px;'>{P["legend_muni"]}</span>
            </span>
            <span style='display:flex; align-items:center; gap:6px;'>
                <span style='width:16px; height:16px; background:{CIVIL_PROTECTION}; border-radius:4px; display:inline-block;'></span>
                <span style='font-size:14px;'>{P["legend_civil"]}</span>
            </span>
            <span style='color:#999;'>|</span>
            <span style='font-size:14px;'>{P["legend_phases"]}</span>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns(3)
    with col1:
        render_column("citizen", M["citizen"], PL)
    with col2:
        render_column("municipality", M["municipality"], PL)
    with col3:
        render_column("civil_protection", M["civil_protection"], PL)

    st.write("")

    with st.container(key="card_budget_tips"):
        st.header(P["budget_title"])
        st.caption(P["budget_caption"])

        cols = st.columns(3)
        for i, (icon, title, desc) in enumerate(BT):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="budget-card">
                    <div style='font-size:36px;'>{icon}</div>
                    <div style='font-size:15px; font-weight:700; color:#16414A; margin-top:8px;'>{title}</div>
                    <div style='font-size:12.5px; color:#666; margin-top:6px;'>{desc}</div>
                </div>
                """, unsafe_allow_html=True)
                st.write("")