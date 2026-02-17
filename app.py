import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime
import time

# Sayfa yapılandırması
st.set_page_config(
    page_title="Argus Pro v3 - Sağlık Paneli",
    page_icon="🏥",
    layout="wide"
)

# CSS Düzenlendi (Süslü parantez hatası giderildi kanka)
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
    .stApp {
        background-color: #0e1117;
    }
    .card {
        background: linear-gradient(145deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 20px;
        padding: 1.5rem;
        border-left: 5px solid #8A2BE2;
        box-shadow: 0 10px 30px rgba(138, 43, 226, 0.2);
        color: white;
        margin: 10px 0;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #8A2BE2;
    }
    .progress-bar {
        width: 100%;
        height: 20px;
        background: #1a1a2e;
        border-radius: 10px;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #8A2BE2, #b066fe);
    }
    </style>
    """, unsafe_allow_html=True)

# --- BAŞLIK ---
st.markdown("<h1 style='text-align: center; color: white;'>🛡️ Argus Pro <span style='color: #8A2BE2;'>v3</span></h1>", unsafe_allow_html=True)

# --- SIDEBAR & SESSION STATE ---
if 'water' not in st.session_state: st.session_state.water = 0

with st.sidebar:
    st.markdown("### 🔑 Strava Bağlantısı")
    token = st.text_input("Access Token Gir:", type="password")
    
    st.markdown("### 💧 Su Takibi")
    if st.button("🚰 +250ml İçtim"):
        st.session_state.water = min(st.session_state.water + 250, 3000)
    
    w_percent = (st.session_state.water / 3000) * 100
    st.markdown(f"""
        <div class='progress-bar'><div class='progress-fill' style='width: {w_percent}%;'></div></div>
        <p style='text-align: center; color: white;'>{st.session_state.water}ml / 3000ml</p>
    """, unsafe_allow_html=True)

# --- VERİ ÇEKME & GÖSTERME ---
if token:
    try:
        url = "https://www.strava.com/api/v3/athlete/activities"
        headers = {"Authorization": f"Bearer {token}"}
        res = requests.get(url, headers=headers, params={"per_page": 5})
        
        if res.status_code == 200:
            activities = res.json()
            col1, col2, col3 = st.columns(3)
            
            # Son aktiviteyi alalım
            last = activities[0]
            with col1:
                st.markdown(f"<div class='card'><b>Mesafe</b><div class='metric-value'>{last['distance']/1000:.1f} km</div></div>", unsafe_allow_html=True)
            with col2:
                hr = last.get('average_heartrate', '--')
                st.markdown(f"<div class='card'><b>Nabız</b><div class='metric-value'>{hr} bpm</div></div>", unsafe_allow_html=True)
            with col3:
                cal = last.get('kilojoules', 0) / 4.184
                st.markdown(f"<div class='card'><b>Kalori</b><div class='metric-value'>{int(cal)} kcal</div></div>", unsafe_allow_html=True)
        else:
            st.error("Token geçersiz kanka!")
    except:
        st.error("Bağlantı kurulamadı.")
else:
    st.info("👈 Kanka soldan token'ı gir, dükkanın verileri gelsin.")
    
