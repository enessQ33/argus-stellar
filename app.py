import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Argus Pro", page_icon="🛡️", layout="wide")

# --- JİLET GİBİ TEMA ---
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
    .stApp { background-color: #0e1117 !important; color: white !important; }
    .metric-card {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #8A2BE2;
        margin-bottom: 20px;
    }
    .strava-link {
        display: block;
        padding: 15px;
        background-color: #FC4C02;
        color: white !important;
        text-decoration: none;
        border-radius: 10px;
        font-weight: bold;
        text-align: center;
    }
    h1, h3 { color: #8A2BE2 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- ANA EKRAN ---
st.markdown("<h1><i class='fa-solid fa-shield-halved'></i> ARGUS PRO</h1>", unsafe_allow_html=True)

# --- STRAVA TOKEN MOTORU ---
def get_strava_data(auth_code):
    payload = {
        'client_id': st.secrets["STRAVA_CLIENT_ID"],
        'client_secret': st.secrets["STRAVA_CLIENT_SECRET"],
        'code': auth_code,
        'grant_type': 'authorization_code'
    }
    # Strava'dan geçiş izni istiyoruz
    res = requests.post("https://www.strava.com/oauth/token", data=payload)
    return res.json()

# --- SIDEBAR BAĞLANTI ---
with st.sidebar:
    st.markdown("### <i class='fa-solid fa-link'></i> Bağlantı")
    c_id = st.secrets["STRAVA_CLIENT_ID"]
    r_uri = st.secrets["REDIRECT_URI"]
    
    # Linkin sonuna kanka mutlaka "/" koyduğundan emin ol
    strava_url = f"https://www.strava.com/oauth/authorize?client_id={c_id}&response_type=code&redirect_uri={r_uri}&approval_prompt=force&scope=read,activity:read_all"
    
    st.markdown(f'<a href="{strava_url}" target="_self" class="strava-link">Strava Giriş Yap</a>', unsafe_allow_html=True)

# --- VERİ YAKALAMA ---
query_params = st.query_params
if "code" in query_params:
    auth_code = query_params["code"]
    with st.spinner('Veriler Strava\'dan çekiliyor...'):
        data = get_strava_data(auth_code)
        if "access_token" in data:
            st.success("🎯 Bağlantı Başarılı! Enes, verilerin artık Argus'ta.")
            # Burada 'data' içinden nabız vs. yazdıracağız kanka
        else:
            st.error("Kanka giriş yapılamadı, Strava izin vermedi.")

# --- KARTLAR ---
st.info("Kanka yukarıdaki butona basıp 'Authorize' (Yetkilendir) dedikten sonra burası dolacak.")
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="metric-card"><h3><i class="fa-solid fa-route"></i> Yol</h3>-- km</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card"><h3><i class="fa-solid fa-heart-pulse"></i> Nabız</h3>-- BPM</div>', unsafe_allow_html=True)
    
