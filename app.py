import streamlit as st
import pandas as pd
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import datetime
import os

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Argus", page_icon="🛡️", layout="wide")

# --- STYLE & FONTS ---
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
    .stMetric { background-color: rgba(138, 43, 226, 0.1); padding: 20px; border-radius: 15px; border: 1px solid #8A2BE2; margin-bottom: 10px; }
    .metric-icon { font-size: 2.5em; color: #8A2BE2; margin-right: 15px; }
    h1, h2, h3 { color: #8A2BE2 !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .auth-button { background-color: #8A2BE2; color: white; padding: 10px 20px; border-radius: 10px; text-decoration: none; }
    </style>
    """, unsafe_allow_html=True)

# --- GOOGLE AUTH AYARLARI ---
SCOPES = [
    'https://www.googleapis.com/auth/fitness.activity.read',
    'https://www.googleapis.com/auth/fitness.heart_rate.read',
    'https://www.googleapis.com/auth/fitness.sleep.read'
]

def create_google_flow():
    client_config = {
        "web": {
            "client_id": st.secrets["GOOGLE_CLIENT_ID"],
            "client_secret": st.secrets["GOOGLE_CLIENT_SECRET"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }
    return Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri=st.secrets["REDIRECT_URI"]
    )

# --- ANA PANEL ---
st.markdown("<h1><i class='fa-solid fa-shield-halved'></i> ARGUS KONTROL PANELİ</h1>", unsafe_allow_html=True)
st.markdown(f"<h3><i class='fa-solid fa-user-gear'></i> Merhaba Enes,</h3>", unsafe_allow_html=True)
st.write(f"📅 Bugün: {datetime.datetime.now().strftime('%d %B %Y')}")

# --- GOOGLE FIT YETKİ BUTONU ---
with st.sidebar:
    st.markdown("### <i class='fa-solid fa-plug-circle-check'></i> Veri Kaynağı")
    flow = create_google_flow()
    auth_url, _ = flow.authorization_url(prompt='consent')
    st.markdown(f'<a href="{auth_url}" target="_self" class="auth-button">🔑 Google Fit Yetki Ver</a>', unsafe_allow_html=True)

# --- METRİK KARTLARI ---
col1, col2, col3 = st.columns(3)

with col1:
    # Kalp Atışı (İkonlu)
    st.markdown("""<div class="stMetric"><i class="metric-icon fa-solid fa-heart-pulse"></i>
    <div><div style="font-size: 0.9em; color: gray;">Canlı Nabız</div>
    <div style="font-size: 1.8em; font-weight: bold;">-- BPM</div></div></div>""", unsafe_allow_html=True)

with col2:
    # Adım (İkonlu)
    st.markdown("""<div class="stMetric"><i class="metric-icon fa-solid fa-person-running"></i>
    <div><div style="font-size: 0.9em; color: gray;">Gerçek Adım</div>
    <div style="font-size: 1.8em; font-weight: bold;">-- Adım</div></div></div>""", unsafe_allow_html=True)

with col3:
    # Uyku (İkonlu)
    st.markdown("""<div class="stMetric"><i class="metric-icon fa-solid fa-bed"></i>
    <div><div style="font-size: 0.9em; color: gray;">Uyku Analizi</div>
    <div style="font-size: 1.8em; font-weight: bold;">-- Saat</div></div></div>""", unsafe_allow_html=True)

# --- GOOGLE'DAN DÖNEN YETKİYİ YAKALAMA ---
query_params = st.query_params
if "code" in query_params:
    st.sidebar.success("✅ Yetki alındı! Veriler yükleniyor...")
    # Buraya veriyi çekip '--' olan yerlere yazdıracak fonksiyonu bir sonraki adımda ekleyeceğiz.
    
