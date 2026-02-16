import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Argus | Pro", page_icon="🛡️", layout="wide")

# --- PROFESYONEL STYLE ---
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
    .stMetric { background-color: #1e2130; padding: 25px; border-radius: 20px; border-left: 5px solid #8A2BE2; }
    .metric-icon { font-size: 2.2em; color: #8A2BE2; margin-bottom: 10px; }
    h1, h2, h3 { color: #8A2BE2 !important; font-family: 'Inter', sans-serif; }
    .sidebar .sidebar-content { background-color: #0e1117; }
    </style>
    """, unsafe_allow_html=True)

# --- ANA BAŞLIK ---
st.markdown("<h1><i class='fa-solid fa-shield-halved'></i> ARGUS PRO PANEL</h1>", unsafe_allow_html=True)
st.write(f"📅 Sistem Tarihi: {datetime.now().strftime('%d %B %Y')}")

# --- STRAVA BAĞLANTI BUTONU ---
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/shield.png", width=80)
    st.markdown("### <i class='fa-solid fa-bolt'></i> Veri Kaynağı")
    if st.button("🔗 Strava'yı Bağla"):
        # Strava yetki linki buraya gelecek kanka
        client_id = st.secrets["STRAVA_CLIENT_ID"]
        redirect_uri = "https://argus-stellar-c55hws6gcz6xtvxevctkad.streamlit.app"
        auth_url = f"http://www.strava.com/oauth/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&approval_prompt=force&scope=read,activity:read_all"
        st.markdown(f'<a href="{auth_url}" target="_self" style="color:white; background:#FC4C02; padding:10px; border-radius:5px; text-decoration:none;">Strava Yetkisi Ver</a>', unsafe_allow_html=True)

# --- METRİKLER ---
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""<div class="stMetric"><i class="metric-icon fa-solid fa-person-running"></i>
    <div style="color:gray;">Son Aktivite Mesafe</div>
    <div style="font-size: 2em; font-weight: bold;">-- km</div></div>""", unsafe_allow_html=True)

with c2:
    st.markdown("""<div class="stMetric"><i class="metric-icon fa-solid fa-heart-pulse"></i>
    <div style="color:gray;">Ortalama Nabız</div>
    <div style="font-size: 2em; font-weight: bold;">-- BPM</div></div>""", unsafe_allow_html=True)

with c3:
    st.markdown("""<div class="stMetric"><i class="metric-icon fa-solid fa-fire-flame-curved"></i>
    <div style="color:gray;">Yakılan Kalori</div>
    <div style="font-size: 2em; font-weight: bold;">-- kcal</div></div>""", unsafe_allow_html=True)

st.markdown("---")
st.info("Kanka Strava butonuyla yetkiyi verince, saatinin Strava'ya attığı son veriler buraya dökülecek.")
