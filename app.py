import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
import os

# --- GOOGLE YETKİ AYARLARI ---
# Bu kapsamlar (scopes) kalp atışı ve adım verisi için şart kanka
SCOPES = [
    'https://www.googleapis.com/auth/fitness.activity.read',
    'https://www.googleapis.com/auth/fitness.body.read',
    'https://www.googleapis.com/auth/fitness.heart_rate.read',
    'https://www.googleapis.com/auth/fitness.sleep.read'
]

def get_google_fit_data():
    # Streamlit Cloud üzerindeki Secrets'tan bilgileri çekiyoruz
    client_config = {
        "web": {
            "client_id": st.secrets["GOOGLE_CLIENT_ID"],
            "client_secret": st.secrets["GOOGLE_CLIENT_SECRET"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [st.secrets.get("REDIRECT_URI", "http://localhost")]
        }
    }
    
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    # Bu satır seni Google'ın izin sayfasına fırlatır kanka
    credentials = flow.run_local_server(port=0)
    return build('fitness', 'v1', credentials=credentials)

# --- ANA TASARIM ---
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
    .stMetric { background-color: rgba(138, 43, 226, 0.1); padding: 15px; border-radius: 15px; border: 1px solid #8A2BE2; }
    .metric-icon { font-size: 2em; color: #8A2BE2; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Argus Canlı Veri Paneli")

with st.sidebar:
    st.markdown("### <i class='fa-solid fa-link'></i> Bağlantı")
    if st.button("🔌 Google Fit'i Şimdi Yetkilendir"):
        try:
            service = get_google_fit_data()
            st.success("Yetki alındı! Veriler akmaya başlıyor...")
            # Burada 'service' üzerinden nabız ve adım verilerini çekeceğiz
        except Exception as e:
            st.error(f"Hata oluştu kanka: {e}")

# --- KARTLAR (İÇİ ŞİMDİLİK BOŞ, YETKİ BEKLİYOR) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""<div class="stMetric"><i class="metric-icon fa-solid fa-heart-pulse"></i> 
    <div style="font-size: 0.8em; color: gray;">Canlı Nabız</div>
    <div style="font-size: 1.5em; font-weight: bold;">-- BPM</div></div>""", unsafe_allow_html=True)

with col2:
    st.markdown("""<div class="stMetric"><i class="metric-icon fa-solid fa-person-walking"></i> 
    <div style="font-size: 0.8em; color: gray;">Gerçek Adım</div>
    <div style="font-size: 1.5em; font-weight: bold;">-- Adım</div></div>""", unsafe_allow_html=True)

with col3:
    st.markdown("""<div class="stMetric"><i class="metric-icon fa-solid fa-bed"></i> 
    <div style="font-size: 0.8em; color: gray;">Uyku Verisi</div>
    <div style="font-size: 1.5em; font-weight: bold;">-- Saat</div></div>""", unsafe_allow_html=True)
        
