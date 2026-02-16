import streamlit as st
from datetime import datetime

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Argus Pro", page_icon="🛡️", layout="wide")

st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
    .stApp { background-color: #0e1117 !important; color: white !important; }
    .strava-link {
        display: inline-block;
        padding: 15px;
        background-color: #FC4C02;
        color: white !important;
        text-decoration: none;
        border-radius: 10px;
        font-weight: bold;
        width: 100%;
        text-align: center;
    }
    .metric-card {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #8A2BE2;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1><i class='fa-solid fa-shield-halved'></i> ARGUS PRO</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### <i class='fa-solid fa-link'></i> Bağlantı Merkezi")
    
    try:
        # Secrets'tan verileri çek
        c_id = st.secrets["STRAVA_CLIENT_ID"]
        r_uri = st.secrets["REDIRECT_URI"]
        
        # Linki oluştur
        strava_url = f"https://www.strava.com/oauth/authorize?client_id={c_id}&response_type=code&redirect_uri={r_uri}&approval_prompt=force&scope=read,activity:read_all"
        
        st.markdown(f'<a href="{strava_url}" target="_self" class="strava-link">Strava Yetkisi Ver</a>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Sırlar (Secrets) okunamadı kanka: {e}")

# --- KARTLAR ---
c1, c2 = st.columns(2)
with c1:
    st.markdown('<div class="metric-card"><h3><i class="fa-solid fa-bolt"></i> Durum</h3>Bağlantı Bekleniyor...</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="metric-card"><h3><i class="fa-solid fa-clock"></i> Zaman</h3>'+datetime.now().strftime("%H:%M")+'</div>', unsafe_allow_html=True)
    
