import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Argus Pro", page_icon="🛡️", layout="wide")

# --- TEMAYI KURTARMA OPERASYONU (CSS) ---
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
    /* Ana Arka Plan */
    .stApp {
        background-color: #0e1117 !important;
        color: white !important;
    }
    /* Kartların Görünümü */
    .metric-card {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #8A2BE2;
        margin-bottom: 20px;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.5);
    }
    .icon-style {
        font-size: 2em;
        color: #8A2BE2;
        margin-bottom: 10px;
    }
    h1, h2, h3 {
        color: #8A2BE2 !important;
    }
    /* Strava Butonu Düzenleme */
    .strava-link {
        display: inline-block;
        padding: 12px 20px;
        background-color: #FC4C02;
        color: white !important;
        text-decoration: none;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ANA EKRAN ---
st.markdown("<h1><i class='fa-solid fa-shield-halved'></i> ARGUS KONTROL PANELİ</h1>", unsafe_allow_html=True)
st.markdown(f"<h3>Merhaba Enes,</h3>", unsafe_allow_html=True)

# --- SIDEBAR & BUTON TAMİRİ ---
with st.sidebar:
    st.markdown("### <i class='fa-solid fa-gear'></i> Bağlantılar")
    
    # Secrets kontrolü
    try:
        c_id = st.secrets["STRAVA_CLIENT_ID"]
        r_uri = st.secrets["REDIRECT_URI"]
        
        # Buton yerine doğrudan tıklanabilir şık bir link (Basılmama ihtimali yok)
        strava_url = f"https://www.strava.com/oauth/authorize?client_id={c_id}&response_type=code&redirect_uri={r_uri}&approval_prompt=force&scope=read,activity:read_all"
        
        st.markdown(f'<a href="{strava_url}" target="_self" class="strava-link"><i class="fa-brands fa-strava"></i> Strava Yetkisi Ver</a>', unsafe_allow_html=True)
    except:
        st.error("Kanka Secrets kısmında ID veya Link eksik!")

# --- KARTLAR ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="metric-card"><i class="fa-solid fa-route icon-style"></i><br><small>Mesafe</small><br><b>-- km</b></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card"><i class="fa-solid fa-heart-pulse icon-style"></i><br><small>Nabız</small><br><b>-- BPM</b></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card"><i class="fa-solid fa-fire icon-style"></i><br><small>Kalori</small><br><b>-- kcal</b></div>', unsafe_allow_html=True)

# --- ALT BİLGİ ---
st.markdown("---")
st.write(f"📅 Son Güncelleme: {datetime.now().strftime('%d/%m/%Y')}")
    
