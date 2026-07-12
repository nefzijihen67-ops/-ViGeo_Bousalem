import streamlit as st
from streamlit_option_menu import option_menu
from languages import TEXTS
from pages_content import dashboard1, dashboard2, dashboard3, dashboard4, dashboard5

st.set_page_config(page_title="ViGeo | Bou Salem", page_icon="🌊", layout="wide")

DARK_TEAL = "#16414A"
DARK_TEAL_2 = "#0F2E34"
TABS_BG = "#2E7C86"
TAB_SELECTED = "#3F97A2"
ACCENT_GOLD = "#C9A468"
CREAM_BG = "#F4EEE3"

if "lang" not in st.session_state:
    st.session_state.lang = "ar"

lang = st.session_state.lang
T = TEXTS[lang]

text_direction = "rtl" if lang == "ar" else "ltr"
text_align = "right" if lang == "ar" else "left"
title_align = "right" if lang == "ar" else "left"
title_justify = "flex-end" if lang == "ar" else "flex-start"

title_parts = T["app_title"].split("|")
brand = title_parts[0].strip()
place = title_parts[1].strip() if len(title_parts) > 1 else ""

st.markdown(f"""
<style>
#MainMenu, header, footer {{visibility: hidden;}}
.stApp {{ background-color: {CREAM_BG}; }}

.st-key-header_bar {{
    background: linear-gradient(135deg, {DARK_TEAL} 0%, {DARK_TEAL_2} 100%);
    padding: 16px 34px;
    border-radius: 0;
}}
.st-key-header_bar h3 {{ color: white !important; margin: 0; }}

.st-key-header_bar [data-testid="stHorizontalBlock"] {{
    display: flex !important;
    flex-direction: row !important;
    justify-content: space-between !important;
    align-items: center !important;
    width: 100% !important;
}}
.st-key-header_bar [data-testid="stColumn"],
.st-key-header_bar [data-testid="column"] {{
    width: auto !important;
    min-width: 0 !important;
    flex: 0 0 auto !important;
}}

.st-key-lang_buttons {{
    display: flex;
    flex-direction: column;
    gap: 6px;
}}
.st-key-lang_buttons button {{
    border-radius: 16px !important;
    border: 1px solid rgba(255,255,255,0.6) !important;
    background-color: transparent !important;
    color: white !important;
    padding: 3px 16px !important;
    font-size: 12px !important;
    min-height: 26px !important;
    width: 100% !important;
}}
.st-key-lang_buttons button[kind="primary"] {{
    background-color: white !important;
    color: {DARK_TEAL} !important;
}}

.logo-badge {{
    width: 50px; height: 50px; min-width: 50px; border-radius: 14px;
    background: linear-gradient(145deg, {ACCENT_GOLD}, #A9834C);
    display: flex; align-items: center; justify-content: center;
    font-size: 25px; box-shadow: 0 6px 14px rgba(201,164,104,0.3);
}}
.brand-title {{
    font-size: 39px; font-weight: 800; line-height: 1.15; letter-spacing: 0.2px;
}}
.brand-subtitle {{
    font-size: 18px; color: #C9E0DD; margin-top: 7px; font-weight: 500; letter-spacing: 0.2px;
}}
.brand-underline {{
    height: 3px; width: 90px;
    background: linear-gradient(90deg, {ACCENT_GOLD}, transparent);
    border-radius: 3px; margin-top: 10px;
}}

[class*="st-key-card_"] {{
    background-color: white;
    padding: 26px;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    margin-top: 20px;
}}

h1, h2, h3 {{ color: #1B2E33 !important; }}

[class*="st-key-card_"] [data-testid="stImage"] {{
    display: flex;
    justify-content: center;
    margin-left: auto;
    margin-right: auto;
}}

[class*="st-key-card_"] [data-testid="stMarkdownContainer"],
[class*="st-key-card_"] h1,
[class*="st-key-card_"] h2,
[class*="st-key-card_"] h3,
[class*="st-key-card_"] [data-testid="stCaptionContainer"] {{
    direction: {text_direction};
    text-align: {text_align};
}}

[class*="st-key-card_"] [data-testid="stHorizontalBlock"] {{
    align-items: center !important;
}}
</style>
""", unsafe_allow_html=True)

with st.container(key="header_bar"):
    if lang == "ar":
        col_lang, col_title = st.columns([0.6, 4])
    else:
        col_title, col_lang = st.columns([4, 0.6])
    with col_lang:
        with st.container(key="lang_buttons"):
            if st.button("English", type="primary" if lang == "en" else "secondary", use_container_width=True):
                st.session_state.lang = "en"
                st.rerun()
            if st.button("Français", type="primary" if lang == "fr" else "secondary", use_container_width=True):
                st.session_state.lang = "fr"
                st.rerun()
            if st.button("العربية", type="primary" if lang == "ar" else "secondary", use_container_width=True):
                st.session_state.lang = "ar"
                st.rerun()
    with col_title:
        margin_side = "right" if lang == "ar" else "left"
        st.markdown(f"""
        <div style='text-align:{title_align};'>
            <div style='display:flex; align-items:center; justify-content:{title_justify}; gap:16px;'>
                <div class='logo-badge'>🌊</div>
                <div class='brand-title'>
                    <span style='color:{ACCENT_GOLD};'>{brand}</span>
                    <span style='color:rgba(255,255,255,0.35); font-weight:300; margin:0 10px;'>|</span>
                    <span style='color:white;'>{place}</span>
                </div>
            </div>
            <div class='brand-subtitle'>{T['app_subtitle']}</div>
            <div class='brand-underline' style='margin-{margin_side}:66px;'></div>
        </div>
        """, unsafe_allow_html=True)

selected = option_menu(
    menu_title=None,
    options=[T["nav_tab1"], T["nav_tab2"], T["nav_tab3"], T["nav_tab4"], T["nav_tab5"]],
    icons=["info-circle", "geo-alt", "cloud-sun", "exclamation-triangle", "shield-check"],
    orientation="horizontal",
    styles={
        "container": {"padding": "0", "background-color": TABS_BG},
        "icon": {"color": "white"},
        "nav-link": {"color": "white", "font-size": "15px", "text-align": "center", "padding": "14px 10px", "margin": "0px"},
        "nav-link-selected": {"background-color": TAB_SELECTED, "border-bottom": f"3px solid {ACCENT_GOLD}"},
    },
)

if selected == T["nav_tab1"]:
    dashboard1.show(lang)
elif selected == T["nav_tab2"]:
    dashboard2.show(lang)
elif selected == T["nav_tab3"]:
    dashboard3.show(lang)
elif selected == T["nav_tab4"]:
    dashboard4.show(lang)
elif selected == T["nav_tab5"]:
    dashboard5.show(lang)