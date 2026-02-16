import streamlit as st
import pandas as pd
from datetime import datetime

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Argus Pro", page_icon="🛡️", layout="wide")

# --- JİLET GİBİ TEMA (CSS) ---
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
    .stApp { background-color: #0e1117 !important; color: white !important; }
    .metric-card {
        background-color: #1e2130;
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #8A2BE2;
        margin-bottom: 20px;
        text-align: center;
    }
    .strava-link {
        display: block;
        padding: 15px;
        background-color: #FC4C02;
        color: white !important;
        text-decoration: none;
        border-radius: 12px;
        font-weight: bold;
        text-align: center;
        transition: 0.3s;
    }
    .strava-link:hover { background-color: #e34402; }
    h1, h3 { color: #8A2BE2 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- ANA EKRAN ---
st.markdown("<h1><i class='fa-solid fa-shield-halved'></i> ARGUS KONTROL PANELİ</h1>", unsafe_allow_html=True)

# --- STRAVA BAĞLANTI SİSTEMİ ---
with st.sidebar:
    st.markdown("<h3><i class='fa-solid fa-bolt'></i> Veri Kaynağı</h3>", unsafe_allow_html=True)
    
    try:
        c_id = st.secrets["STRAVA_CLIENT_ID"]
        r_uri = st.secrets["REDIRECT_URI"]
        
        # Strava'nın beklediği tam yetki linki
        strava_url = (
            f"https://www.strava.com/oauth/authorize?"
            f"client_id={c_id}&"
            f"response_type=code&"
            f"redirect_uri={r_uri}&"
            f"approval_prompt=force&"
            f"scope=read,activity:read_all"
        )
        
        st.markdown(f'<a href="{strava_url}" target="_self" class="strava-link"><i class="fa-brands fa-strava"></i> Strava Yetkisi Ver</a>', unsafe_allow_html=True)
        st.caption("Butona bastığında Strava onay sayfası açılmalı.")
        
    except Exception as e:
        st.error("Secrets eksik kanka!")

# --- KARTLAR (TEMSİLİ - VERİ BEKLENİYOR) ---
col1, col2, col3 = st.columns(3)

# Sayfa linkinde 'code' varsa bağlantı kurulmuş demektir
if "code" in st.query_params:
    st.success("✅ Yetki yakalandı! Verileriniz işleniyor...")
    dist, hr, cal = "8.2", "138", "540" # Buraya gerçek Strava API çekme kodu gelecek
else:
    dist, hr, cal = "--", "--", "--"

with col1:
    st.markdown(f'<div class="metric-card"><i class="fa-solid fa-route" style="font-size:2em; color:#8A2BE2;"></i><br><small>Son Mesafe</small><br><b style="font-size:1.5em;">{dist} km</b></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><i class="fa-solid fa-heart-pulse" style="font-size:2em; color:#8A2BE2;"></i><br><small>Ort. Nabız</small><br><b style="font-size:1.5em;">{hr} BPM</b></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><i class="fa-solid fa-fire" style="font-size:2em; color:#8A2BE2;"></i><br><small>Kalori</small><br><b style="font-size:1.5em;">{cal} kcal</b></div>', unsafe_allow_html=True)
    
